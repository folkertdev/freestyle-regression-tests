import os
import sys
import subprocess
from contextlib import contextmanager, suppress, redirect_stdout
from functools import namedtuple, partial
from itertools import chain, starmap


class files():
    """Object holding files to render and the amount of valid frames they have """
    class testfile(str):
        max_range = (0, 0)
        pass

    shaders = testfile("shaders.blend")
    shaders.max_range = (0, 62)
    predicates = testfile("predicates.blend")
    predicates.max_range = (0, 22)
    modifiers = testfile("modifiers.blend")
    modifiers.max_range = (0, 15)
    chainingiterators = testfile("chainingiterators.blend")
    chainingiterators.max_range = (0, 9)
files = files()


def flatten(listOfLists):
    "Flatten one level of nesting"
    return chain.from_iterable(listOfLists)


class CONFIG:
    # start and end frame (both inclusive)
    start = 0
    end = 0

    def get_rendering(self):
        return (self.start, self.end)

    def set_rendering(self, value):
        self.start, self.end = value

    rendering = property(get_rendering, set_rendering)

    
    # locations of the blender.exe's to test
    blender_dir_old = "C:\Downloads/blender-regression/old"
    blender_dir_new = "C:/bsvn/vc13x86/bin/Release"
    # path to the file to render
    file = "C:/bsvn/regression_test.blend"
    # folder to store output, creates ./orig, ./new and ./comp
    output = "c:/tmp/regression_tests"
    version = "new"
CONFIG = CONFIG()


class RenderResult(object):
    """Object holding data for specific frames."""
    def __init__(self, name, shadertime, filename, totaltime):
        self.name = name
        self.shadertime = round(float(shadertime), 5)
        self.filename = filename
        self.totaltime = totaltime
        self.proc = round(self.shadertime / totaltime, 2) if totaltime else 0.0
        self.index = int(filename.split(".")[0])

    def process(self, output_dir, version, fmt_str):
        # path to the resulting render
        inputname = os.path.join(output_dir, self.filename)
        # path to the renamed file
        version = "orig" if version == "old" else version
        filename = os.path.join(output_dir, version, fmt_str.format(self.name, version))
        self.filename = filename
        cmd = """convert {file} -font source-code-pro -pointsize 20 label:"{name} rendered in {time} msecs {proc:.2%}" \
                -gravity Center -append {filename}""".format(filename=filename,
                                                             time=self.shadertime,
                                                             file=inputname,
                                                             name=self.name,
                                                             proc=self.proc)
        with suppress(FileNotFoundError, PermissionError):
            os.remove(filename)
        os.system(cmd)
        with suppress(FileNotFoundError, PermissionError):
            os.remove(inputname)

    def check(self, output_dir):
        old = os.path.join(output_dir,"orig" , self.name + "_orig.png")
        comp = os.path.join(output_dir, "comp", self.name + ".png")

        cmd = 'compare -extract 480x350+240+135 -metric MAE "{old}" "{new}" "{result}"'.format(old=old, new=self.filename, result=comp)
        with subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT) as p:
            line = str(p.stdout.readline(), 'utf-8')
            size = float(line.split("(")[-1].split(")")[0])
            if len(line) > 5 and size > 1e-5:
                print(self.name, " has regressions, size: ", line)       


def render(cmd):
    """Renders the frames and filters output."""
    with subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT) as p:
        it = iter(p.stdout.readline, b'')
        # get all lines with data we'll want
        data = tuple(str(line, 'utf-8') for line in it if line.startswith((b"regtest", b"Saved:")))
        # tuple of lists of format ["name", "time"]
        times = tuple(line.split()[1:] for line in data if line.startswith("regtest"))
        # tuple of tuples of format ("filename", total_render_time)
        extract = lambda line: (line.split("\\")[-1].split()[0], float(line.split(":")[-3][0:4]))
        files = (extract(line) for line in data if line.startswith("Saved:"))

        return starmap(RenderResult, map(flatten, zip(times, files)))

def checkpaths():
    """Verifies the existence of the necessary paths, creates them if necessary."""
    for folder in ("orig", "new", "comp"):
        path = os.path.join(CONFIG.output, folder)
        if not os.path.isdir(path):
            os.mkdir(path)


def create_command(blender_path, file, output_dir, render_range):
    """Creates the shell command that'll render the frames.""" 
    return """{blender}/blender.exe "{blendfile}" -b -o \
             "{output_dir}/" -F PNG -s {start} -e {end} -a""".format(blender=blender_path,
                                                                     blendfile=file,
                                                                     output_dir=output_dir,
                                                                     start=render_range[0],
                                                                     end=render_range[1])


def main():
    # assure paths for output are valid
    checkpaths()
    # setup the config
    CONFIG.rendering = (0,  9)
    CONFIG.version = "new"
    CONFIG.file = files.shaders
    CONFIG.rendering = CONFIG.file.max_range
    cmd = create_command(CONFIG.blender_dir_new, CONFIG.file, CONFIG.output, CONFIG.rendering)
    fmt_str = "{}_{}.png"
    for result in render(cmd):
        #print(result.index, result.name, result.shadertime)
        result.process(os.path.join(CONFIG.output), CONFIG.version, fmt_str)
        if CONFIG.version == "new":
                result.check(CONFIG.output)

    

if __name__ == '__main__':
    sys.exit(main())