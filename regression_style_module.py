from parameter_editor import RoundCapShader, SquareCapShader

from freestyle.predicates import *
from freestyle.shaders import *
from freestyle.types import *
from freestyle.functions import * 
from freestyle.chainingiterators import *
from freestyle.utils import * 

import mathutils, bpy, time, sys, cProfile, pstats
from mathutils import Vector, Color 
from contextlib import contextmanager

# output cProfile profiling information into seperate files
with_cProfile = True 

# logs freestyle rendertimes and other data
bpy.app.debug_freestyle = True

Operators.select(QuantitativeInvisibilityUP1D(0))

frame = bpy.data.scenes['Scene'].frame_current

# list of all testable types (somewhat complete)
types = (
    pyChainSilhouetteIterator(),                                             # 0
    pyChainSilhouetteGenericIterator(),                                      # 1
    pyExternalContourChainingIterator(),                                     # 2
    pySketchyChainSilhouetteIterator(),                                      # 3
    pySketchyChainingIterator(),                                             # 4
    pyFillOcclusionsRelativeChainingIterator(.2),                            # 5
    pyFillOcclusionsAbsoluteChainingIterator(20),                            # 6
    pyFillOcclusionsAbsoluteAndRelativeChainingIterator(.2, 20),             # 7
    pyFillQi0AbsoluteAndRelativeChainingIterator(.2, 20),                    # 8
    pyNoIdChainSilhouetteIterator(),                                         # 9
    pyDepthDiscontinuityThicknessShader(3, 5),                               # 10
    pyConstantThicknessShader(5),                                            # 11
    pyFXSVaryingThicknessWithDensityShader(5, 3, 5, 3, 5),                   # 12
    pyIncreasingThicknessShader(2, 5),                                       # 13
    pyConstrainedIncreasingThicknessShader(3, 5, .5),                        # 14
    pyDecreasingThicknessShader(3, 5),                                       # 15
    pyNonLinearVaryingThicknessShader(10, 5, 3),                             # 16
    pySLERPThicknessShader(3, 5),                                            # 17
    pyTVertexThickenerShader(),                                              # 18
    pyImportance2DThicknessShader(1, 2, 3, 3, 5),                            # 19
    pyImportance3DThicknessShader(1, 2, 3, 4, 3, 5),                         # 20
    pyZDependingThicknessShader(3, 5),                                       # 21
    pyConstantColorShader(1, 0, 0),                                          # 22
    pyIncreasingColorShader(1, 0, 0, 1, 0, 1, 0, 1),                         # 23
    pyInterpolateColorShader(1, 0, 0, 1, 0, 1, 0, 1),                        # 24
    pyMaterialColorShader(),                                                 # 25
    pyRandomColorShader(),                                                   # 26
    py2DCurvatureColorShader(),                                              # 27
    pyTimeColorShader(),                                                     # 28
    pySamplingShader(10),                                                    # 29
    pyBackboneStretcherShader(20),                                           # 30
    pyLengthDependingBackboneStretcherShader(1),                             # 31
    pyGuidingLineShader(),                                                   # 32
    pyBackboneStretcherNoCuspShader(20),                                     # 33
    pyDiffusion2Shader(.3, 4),                                               # 34
    pyTipRemoverShader(5),                                                   # 35
    pyTVertexRemoverShader(),                                                # 36
    pyHLRShader(),                                                           # 37
    pySinusDisplacementShader(20, 17),                                       # 38
    pyPerlinNoise1DShader(seed=2),                                           # 39
    pyPerlinNoise2DShader(seed=2),                                           # 40
    pyBluePrintCirclesShader(turns=4, random_radius=0, random_center=0),     # 41
    pyBluePrintEllipsesShader(turns=4, random_radius=0, random_center=0),    # 42
    pyBluePrintSquaresShader(),                                              # 43
    pyBluePrintDirectedSquaresShader(),                                      # 44
    pyModulateAlphaShader(),                                                 # 45
    pyHigherCurvature2DAngleUP0D(5),                                         # 46
    pyUEqualsUP0D(3, 5),                                                     # 47
    pyVertexNatureUP0D(Nature.T_VERTEX),                                     # 48
    pyBackTVertexUP0D(),                                                     # 49
    pyParameterUP0DGoodOne(3, 5),                                            # 50
    pyParameterUP0D(3, 5),                                                   # 51
    AndUP1D(pyUEqualsUP0D(3, 5), pyUEqualsUP0D(3, 5)),                       # 52
    OrUP1D(pyUEqualsUP0D(3, 5), pyUEqualsUP0D(3, 5)),                        # 53
    NotUP1D(pyUEqualsUP0D(3, 5)),                                            # 54
    pyNFirstUP1D(5),                                                         # 55
    pyHigherLengthUP1D(20),                                                  # 56
    pyNatureUP1D(Nature.SILHOUETTE),                                         # 57
    pyHigherNumberOfTurnsUP1D(3, 5),                                         # 58
    pyDensityUP1D(3, 5),                                                     # 59
    pyZSmallerUP1D(.5),                                                      # 60
    pyZBP1D(),                                                               # 61
    pyZDiscontinuityBP1D(),                                                  # 62
    pyLengthBP1D(),                                                          # 63
    pyShuffleBP1D(),                                                         # 64
    RoundCapShader(),                                                        # 66
    SquareCapShader(),                                                       # 67
)


@contextmanager
def duration(*args):
    start = time.time()
    yield
    end = time.time()
    print("regtest: ", types[frame].__class__.__name__, end - start)


class predicateTestShader(StrokeShader):
    """ Strokeshader that translates predicates into colors, for easier regression testing """
    def __init__(self, pred):
        self.pred = pred
        StrokeShader.__init__(self)

    def shade(self, stroke):
        it = Interface0DIterator(stroke)
        try: 
            for svert, _ in zip(stroke, it):
                c = float(self.pred(it))
                svert.attribute.color = (c, c, c) 
        # distinct between arguments for __call__
        # some expect Interface1D, others Interface0D
        except (TypeError, AttributeError):
            try:
                for svert in stroke:
                    c = float(self.pred(stroke))
                    svert.attribute.color = (c, c, c)
            except TypeError:
                try:
                    for svert in stroke:
                        c = float(self.pred(stroke, stroke))
                        svert.attribute.color = (c, c, c)
                except:
                    print(types[frame], " has issues")
                    pass

# 
current = types[frame]

# select chainingiterator
cit = types[frame] if frame <= 9 else types[0]
Operators.bidirectional_chain(cit, NotUP1D(QuantitativeInvisibilityUP1D(0)))

 
func = pyInverseCurvature2DAngleF0D()
Operators.recursive_split(func, pyParameterUP0D(0.2, 0.8), NotUP1D(pyHigherNumberOfTurnsUP1D(3, .5)), 2)
Operators.sort(pyLengthBP1D())

# chaining iterators
if current.name.endswith("Iterator"):
    shaders_list = [   
        SamplingShader(10), 
        ConstantThicknessShader(10),
    ]

# stroke shaders
elif current.name.endswith("Shader"):
    shaders_list = [
        SamplingShader(10), 
        ConstantThicknessShader(10),
        types[frame],
    ]

# predicates
elif current.name.endswith(("BP1D", "UP1D", "UP0D", "BP0D")):
    shaders_list = [
        SamplingShader(10),
        ConstantThicknessShader(10),
        predicateTestShader(types[frame]),
    ]
else:
    if current.name == "pyParameterUP0DGoodOne": # exceptions ...
        shaders_list = [
            SamplingShader(10),
            ConstantThicknessShader(10),
            predicateTestShader(types[frame]),
        ]
    else:
        raise RuntimeError("unexpected type: " + current.name)
# start timing
if with_cProfile:
    if "new" in sys.argv[0]:
        path = "C:/tmp/regression_tests/cprofile_new/" + types[frame].__class__.__name__ + "_new.txt"
    else:
        path = "C:/tmp/regression_tests/cprofile_old/" + types[frame].__class__.__name__ + "_old.txt"


with duration():
    if with_cProfile:
        with open(path, 'w') as f:
            pr = cProfile.Profile()
            pr.enable()
            ##
            Operators.create(DensityLowerThanUP1D(8, 0.4), shaders_list)
            ##
            pr.disable()
            ps = pstats.Stats(pr, stream=f).sort_stats('cumulative')
            ps.print_stats()
    else:
        Operators.create(DensityLowerThanUP1D(8, 0.4), shaders_list)