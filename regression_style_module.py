from parameter_editor import *

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

# These objects are created in the parameter editor. get them from there (they are used as arguments)
ramp = bpy.data.linestyles[0].color_modifiers[0].color_ramp
blend = bpy.data.linestyles[0].color_modifiers[0].blend
curve = bpy.data.linestyles[0].alpha_modifiers[0].curve
target = bpy.data.objects[0]

# list of all testable types (somewhat complete)
types = (
    pyChainSilhouetteIterator(),                                                # 0
    pyChainSilhouetteGenericIterator(),                                         # 1
    pyExternalContourChainingIterator(),                                        # 2
    pySketchyChainSilhouetteIterator(),                                         # 3
    pySketchyChainingIterator(),                                                # 4
    pyFillOcclusionsRelativeChainingIterator(.2),                               # 5
    pyFillOcclusionsAbsoluteChainingIterator(20),                               # 6
    pyFillOcclusionsAbsoluteAndRelativeChainingIterator(.2, 20),                # 7
    pyFillQi0AbsoluteAndRelativeChainingIterator(.2, 20),                       # 8
    pyNoIdChainSilhouetteIterator(),                                            # 9
    pyDepthDiscontinuityThicknessShader(3, 5),                                  # 10
    pyConstantThicknessShader(5),                                               # 11
    pyFXSVaryingThicknessWithDensityShader(5, 3, 5, 3, 5),                      # 12
    pyIncreasingThicknessShader(2, 5),                                          # 13
    pyConstrainedIncreasingThicknessShader(3, 5, .5),                           # 14
    pyDecreasingThicknessShader(3, 5),                                          # 15
    pyNonLinearVaryingThicknessShader(10, 5, 3),                                # 16
    pySLERPThicknessShader(3, 5),                                               # 17
    pyTVertexThickenerShader(),                                                 # 18
    pyImportance2DThicknessShader(1, 2, 3, 3, 5),                               # 19
    pyImportance3DThicknessShader(1, 2, 3, 4, 3, 5),                            # 20
    pyZDependingThicknessShader(3, 5),                                          # 21
    pyConstantColorShader(1, 0, 0),                                             # 22
    pyIncreasingColorShader(1, 0, 0, 1, 0, 1, 0, 1),                            # 23
    pyInterpolateColorShader(1, 0, 0, 1, 0, 1, 0, 1),                           # 24
    pyMaterialColorShader(),                                                    # 25
    pyRandomColorShader(s=5),                                                   # 26
    py2DCurvatureColorShader(),                                                 # 27
    pyTimeColorShader(),                                                        # 28
    pySamplingShader(10),                                                       # 29
    pyBackboneStretcherShader(20),                                              # 30
    pyLengthDependingBackboneStretcherShader(1),                                # 31
    pyGuidingLineShader(),                                                      # 32
    pyBackboneStretcherNoCuspShader(20),                                        # 33
    pyDiffusion2Shader(.3, 4),                                                  # 34
    pyTipRemoverShader(5),                                                      # 35
    pyTVertexRemoverShader(),                                                   # 36
    pyHLRShader(),                                                              # 37
    pySinusDisplacementShader(20, 17),                                          # 38
    pyPerlinNoise1DShader(seed=2),                                              # 39
    pyPerlinNoise2DShader(seed=2),                                              # 40
    pyBluePrintCirclesShader(turns=4, random_radius=0, random_center=0),        # 41
    pyBluePrintEllipsesShader(turns=4, random_radius=0, random_center=0),       # 42
    pyBluePrintSquaresShader(),                                                 # 43
    pyBluePrintDirectedSquaresShader(),                                         # 44
    pyModulateAlphaShader(),                                                    # 45
    RoundCapShader(),                                                           # 46
    SquareCapShader(),                                                          # 47
    BaseThicknessShader(5, 'CENTER', .5),                                       # 48
    ColorAlongStrokeShader(blend, 1.0, ramp),                                   # 49
    AlphaAlongStrokeShader(blend, 1.0, 'CURVE', False, curve),                  # 50
    ThicknessAlongStrokeShader('CENTER', .5, blend, 1.0, 'CURVE', False, curve, 0.0, 1.0), # 51
    ColorDistanceFromCameraShader(blend, 1.0, ramp, 0.1, 3),                    # 52
    AlphaDistanceFromCameraShader(blend, 1.0, 'CURVE', False, curve, 0.1, 3),   # 53
    ThicknessDistanceFromCameraShader('CENTER', 0.5, blend, 1.0, 'CURVE', False, curve, .1, 3, 2, 10), # 54
    ColorDistanceFromObjectShader(blend, 1.0, ramp, target, .1, 3),             # 55
    AlphaDistanceFromObjectShader(blend, 1.0, 'CURVE', False, curve, target, .1, 3), # 56
    ThicknessDistanceFromObjectShader('CENTER', 0.5, blend, 1.0, 'CURVE', False, curve, target, .1, 3, 2, 10), # 57
    ColorMaterialShader(blend, 1.0, ramp, 'DIFF', False),                       # 58
    ColorMaterialShader(blend, 1.0, ramp, 'DIFF', True),                        # 59
    AlphaMaterialShader(blend, 1.0, 'CURVE', False, curve, 'DIFF'),             # 60
    ThicknessMaterialShader('CENTER', 0.5, blend, 1.0, 'CURVE', False, curve, 'DIFF', 2, 10), # 61
    CalligraphicThicknessShader('CENTER', 0.5, blend, 1.0, 60, 2, 10),          # 62
    SinusDisplacementShader(20, 5, 1),                                          # 63
    PerlinNoise1DShader(seed=5),                                                # 64
    PerlinNoise2DShader(seed=5),                                                # 65
    Offset2DShader(5, 10, 30, 40),                                              # 66
    Transform2DShader('START', 1.5, 1.5, 180, 10, 10, 10),                      # 67
    Transform2DShader('END', 1.5, 1.5, 180, 10, 10, 10),                        # 68
    Transform2DShader('PARAM', 1.5, 1.5, 180, 10, 10, 10),                      # 69
    Transform2DShader('CENTER', 1.5, 1.5, 180, 10, 10, 10),                     # 70
    Transform2DShader('ABSOLUTE', 1.5, 1.5, 180, 10, 10, 10),                   # 71
    DashedLineShader(pattern=[5,5,5,5,5,5]),                                    # 72
    pyHigherCurvature2DAngleUP0D(5),                                            # 73
    pyUEqualsUP0D(3, 5),                                                        # 74
    pyVertexNatureUP0D(Nature.T_VERTEX),                                        # 75
    pyBackTVertexUP0D(),                                                        # 76
    pyParameterUP0DGoodOne(3, 5),                                               # 77
    pyParameterUP0D(3, 5),                                                      # 78
    AndUP1D(pyUEqualsUP0D(3, 5), pyUEqualsUP0D(3, 5)),                          # 79
    OrUP1D(pyUEqualsUP0D(3, 5), pyUEqualsUP0D(3, 5)),                           # 80
    NotUP1D(pyUEqualsUP0D(3, 5)),                                               # 81
    pyNFirstUP1D(5),                                                            # 82
    pyHigherLengthUP1D(20),                                                     # 83
    pyNatureUP1D(Nature.SILHOUETTE),                                            # 84
    pyHigherNumberOfTurnsUP1D(3, 5),                                            # 85
    pyDensityUP1D(3, 5),                                                        # 86
    pyZSmallerUP1D(.5),                                                         # 87
    pyZBP1D(),                                                                  # 88
    pyZDiscontinuityBP1D(),                                                     # 89
    pyLengthBP1D(),                                                             # 90
    pyShuffleBP1D(),                                                            # 91
    #AngleLargerThanBP1D(90),
    LengthThresholdUP1D(30),
    #FaceMarkBothUP1D(),
    #FaceMarkOneUP1D(),
    MaterialBoundaryUP0D(),
    Curvature2DAngleThresholdUP0D(30, 120),
    Length2DThresholdUP0D(50),
)


@contextmanager
def duration(*args):
    """ Context Manager for measuring execution time """
    start = time.time()
    yield
    end = time.time()
    print("regtest: ", types[frame].__class__.__name__, end - start)


class predicateTestShader(StrokeShader):
    """ Strokeshader that translates predicates into colors, for easier regression testing """
    def __init__(self, pred):
        self.pred = pred
        StrokeShader.__init__(self)

    # def shade(self, stroke):
    #     # distinct between arguments for __call__
    #     # some expect Interface1D, others Interface0D
    #     try:
    #         it = Interface0DIterator(stroke)
    #         for svert in it:
    #             c = self.pred(it)
    #             svert.attribute.color = (c, c, c)  
    #         # done, so return
    #         return 
    #     except (TypeError, AttributeError):
    #         raise 
            
    #     try:
    #         for svert in stroke:
    #             c = float(self.pred(stroke))
    #             svert.attribute.color = (c, c, c)
    #         return
    #     except (TypeError, AttributeError):
    #         pass 

    #     try:
    #         for svert in stroke:
    #             c = float(self.pred(stroke, stroke))
    #             svert.attribute.color = (c, c, c)
    #         return 
    #     except:
    #         print(types[frame], " has issues")
    #         pass
    def shade(self, stroke):
        # distinct between arguments for __call__
        # some expect Interface1D, others Interface0D
        name = type(self.pred).__name__
        if "0D" in name:
            it = Interface0DIterator(stroke)
            for svert in it:
                c = self.pred(it)
                svert.attribute.color = (c, c, c)

        elif "1D" in name:
            try:
                for svert in stroke:
                    c = float(self.pred(stroke))
                    svert.attribute.color = (c, c, c)
            except AttributeError:
                it = Interface0DIterator(stroke)
                for svert in it:
                    c = self.pred(it)
                    svert.attribute.color = (c, c, c)
            except TypeError: #__call__() missing 1 required positional argument: 'i2'
                for svert in stroke:
                        c = float(self.pred(stroke, stroke))
                        svert.attribute.color = (c, c, c)


# actual setup for the render
current = types[frame]

cit = current if current.name.endswith("Iterator") else types[0]
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
elif current.name.endswith(("Shader", "Modifier")):
    shaders_list = [
        SamplingShader(10),
        # this shader causes various StrokeAttribute objects per stroke
        # to make sure no mistakes have been made
        pyNonLinearVaryingThicknessShader(30, 10, 5),
        current,
    ]

# predicates
elif current.name.endswith(("BP1D", "UP1D", "UP0D", "BP0D")):
    shaders_list = [
        SamplingShader(10),
        ConstantThicknessShader(10),
        predicateTestShader(current),
    ]
else:
    raise RuntimeError("unexpected type: " + current.name)

# start timing
if with_cProfile:
    if "new" in sys.argv[0]:
        path = "C:/tmp/regression_tests/cprofile_new/" + current.name + "_new.txt"
    else:
        path = "C:/tmp/regression_tests/cprofile_old/" + current.name + "_old.txt"


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