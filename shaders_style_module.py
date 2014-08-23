from parameter_editor import *

from freestyle.predicates import *
from freestyle.shaders import *
from freestyle.types import *
from freestyle.functions import *
from freestyle.chainingiterators import *
from freestyle.utils import *

# from _freestyle import LengthDependingThicknessShader

import mathutils, bpy, time, sys, cProfile, pstats
from mathutils import Vector, Color
from contextlib import contextmanager


bpy.app.debug_freestyle = True
frame = bpy.data.scenes['Scene'].frame_current

@contextmanager
def duration(*args):
    """ Context Manager for measuring execution time """
    start = time.time()
    yield
    end = time.time()
    print("regtest: ", types[frame].__class__.__name__, end - start)

# output cProfile profiling information into seperate files
with_cProfile = False

# logs freestyle rendertimes and other data
bpy.app.debug_freestyle = True



# fake classes to seperate the different versions of this shader
class Transform2DShaderStart(Transform2DShader): pass
class Transform2DShaderEnd(Transform2DShader): pass
class Transform2DShaderParam(Transform2DShader): pass
class Transform2DShaderCenter(Transform2DShader): pass
class Transform2DShaderAbsolute(Transform2DShader): pass

frame = bpy.data.scenes['Scene'].frame_current

# These objects are created in the parameter editor. they are used as arguments.
ramp = bpy.data.linestyles[0].color_modifiers[0].color_ramp
blend = bpy.data.linestyles[0].color_modifiers[0].blend
curve = bpy.data.linestyles[0].alpha_modifiers[0].curve
target = bpy.data.objects[0]

# list of all testable types (somewhat complete)
# some arguments are difficult to 'fake', other types just crash (the viewmap-dependent ones)
types = (
    pyDepthDiscontinuityThicknessShader(3, 5),                             # 0
    pyConstantThicknessShader(5),                                          # 1
    pyFXSVaryingThicknessWithDensityShader(5, 3, 5, 3, 5),                 # 2
    pyIncreasingThicknessShader(2, 5),                                     # 3
    pyConstrainedIncreasingThicknessShader(3, 5, .5),                      # 4
    pyDecreasingThicknessShader(3, 5),                                     # 5
    pyNonLinearVaryingThicknessShader(10, 5, 3),                           # 6
    pySLERPThicknessShader(3, 5),                                          # 7
    pyTVertexThickenerShader(),                                            # 8
    pyImportance2DThicknessShader(1, 2, 3, 3, 5),                          # 9
    pyImportance3DThicknessShader(1, 2, 3, 4, 3, 5),                       # 10
    pyZDependingThicknessShader(3, 5),                                     # 11
    pyConstantColorShader(1, 0, 0),                                        # 12
    pyIncreasingColorShader(1, 0, 0, 1, 0, 1, 0, 1),                       # 13
    pyInterpolateColorShader(1, 0, 0, 1, 0, 1, 0, 1),                      # 14
    pyMaterialColorShader(),                                               # 15
    pyRandomColorShader(s=5),                                              # 16
    py2DCurvatureColorShader(),                                            # 17
    pyTimeColorShader(),                                                   # 18
    pySamplingShader(10),                                                  # 19
    pyBackboneStretcherShader(20),                                         # 20
    pyLengthDependingBackboneStretcherShader(1),                           # 21
    pyGuidingLineShader(),                                                 # 22
    pyBackboneStretcherNoCuspShader(20),                                   # 23
    pyDiffusion2Shader(.3, 4),                                             # 24
    pyTipRemoverShader(5),                                                 # 25
    pyTVertexRemoverShader(),                                              # 26
    pyHLRShader(),                                                         # 27
    pySinusDisplacementShader(20, 17),                                     # 28
    pyPerlinNoise1DShader(seed=2),                                         # 29
    pyPerlinNoise2DShader(seed=2),                                         # 30
    pyBluePrintCirclesShader(turns=4, random_radius=0, random_center=0),   # 31
    pyBluePrintEllipsesShader(turns=4, random_radius=0, random_center=0),  # 32
    pyBluePrintSquaresShader(),                                            # 33
    pyBluePrintDirectedSquaresShader(),                                    # 34
    pyModulateAlphaShader(),                                               # 35
    RoundCapShader(),                                                      # 36
    SquareCapShader(),                                                     # 37
    BaseThicknessShader(5, 'CENTER', .5),                                  # 38
    ColorAlongStrokeShader(blend, 1.0, ramp),                              # 39
    AlphaAlongStrokeShader(blend, 1.0, 'CURVE', False, curve),             # 40
    ThicknessAlongStrokeShader('CENTER', .5, blend, 1.0, 'CURVE', False, curve, 0.0, 1.0), # 41
    ColorDistanceFromCameraShader(blend, 1.0, ramp, 0.1, 3),               # 42
    AlphaDistanceFromCameraShader(blend, 1.0, 'CURVE', False, curve, 0.1, 3), # 43
    ThicknessDistanceFromCameraShader('CENTER', 0.5, blend, 1.0, 'CURVE', False, curve, .1, 3, 2, 10), # 44
    ColorDistanceFromObjectShader(blend, 1.0, ramp, target, .1, 3),        # 45
    AlphaDistanceFromObjectShader(blend, 1.0, 'CURVE', False, curve, target, .1, 3), # 46
    ThicknessDistanceFromObjectShader('CENTER', 0.5, blend, 1.0, 'CURVE', False, curve, target, .1, 3, 2, 10), # 47
    ColorMaterialShader(blend, 1.0, ramp, 'DIFF', False),                  # 48
    ColorMaterialShader(blend, 1.0, ramp, 'DIFF', True),                   # 49
    AlphaMaterialShader(blend, 1.0, 'CURVE', False, curve, 'DIFF'),        # 50
    ThicknessMaterialShader('CENTER', 0.5, blend, 1.0, 'CURVE', False, curve, 'DIFF', 2, 10), # 51
    CalligraphicThicknessShader('CENTER', 0.5, blend, 1.0, 60, 2, 10),     # 52
    SinusDisplacementShader(20, 5, 1),                                     # 53
    PerlinNoise1DShader(seed=5),                                           # 54
    PerlinNoise2DShader(seed=5),                                           # 55
    Offset2DShader(5, 10, 30, 40),                                         # 56
    Transform2DShaderStart('START', 1.5, 1.5, 180, 10, 10, 10),            # 57
    Transform2DShaderEnd('END', 1.5, 1.5, 180, 10, 10, 10),                # 58
    Transform2DShaderParam('PARAM', 1.5, 1.5, 180, 10, 10, 10),            # 59
    Transform2DShaderCenter('CENTER', 1.5, 1.5, 180, 10, 10, 10),          # 60
    Transform2DShaderAbsolute('ABSOLUTE', 1.5, 1.5, 180, 10, 10, 10),      # 61
    DashedLineShader(pattern=[1,5,2,5,5,10]),                              # 62
    )

# actual setup for the render
current = types[frame]
name = current.name

upred = QuantitativeInvisibilityUP1D(0)
Operators.select(upred)

cit = pyChainSilhouetteIterator()
Operators.bidirectional_chain(cit, NotUP1D(QuantitativeInvisibilityUP1D(0)))

func = pyInverseCurvature2DAngleF0D()
Operators.recursive_split(func, pyParameterUP0D(0.2, 0.8), NotUP1D(pyHigherNumberOfTurnsUP1D(3, .5)), 2)
Operators.sort(pyLengthBP1D())


if "Shader" in name or "Modifier" in name:
    shaders_list = [
        SamplingShader(5),
        current,
    ]
else:
    shaders_list = [
        SamplingShader(5),
    ]

# start timing
if with_cProfile:
    if "new" in sys.argv[0]:
        path = "C:/tmp/regression_tests/cprofile_new/" + name + "_new.txt"
    else:
        path = "C:/tmp/regression_tests/cprofile_old/" + name + "_old.txt"


def create():
    Operators.create(DensityLowerThanUP1D(8, 0.4), shaders_list)

with duration():
    if with_cProfile:
        with open(path, 'w') as f:
            pr = cProfile.Profile()
            pr.enable()
            ##
            create()
            ##
            pr.disable()
            ps = pstats.Stats(pr, stream=f).strip_dirs().sort_stats('cumulative')
            ps.print_stats()

    else:
        create()