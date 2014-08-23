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

types = (
    BackboneStretcherShader(amount=20),                     # 0
    BezierCurveShader(error=10),                            # 1
    CalligraphicShader(15, 30, Vector((1, 1)), True),       # 2
    ColorNoiseShader(amplitude=12, period=31),              # 3
    ConstantColorShader(0.050876, 0.050876, 0.050876),      # 4
    ConstantThicknessShader(thickness=10),                  # 5
    ConstrainedIncreasingThicknessShader(5, 10, .45),       # 6
    GuidingLinesShader(offset=.1),                          # 7
    pyGuidingLineShader(),                                  # 8
    IncreasingColorShader(1., 0, 0, .2, 0, 1, 0, 1.0),      # 9
    IncreasingThicknessShader(5, 10),                       # 10
    PolygonalizationShader(10),                             # 11
    SmoothingShader(),                                      # 12
    SpatialNoiseShader(10, 20, 4, True, True),              # 13
    ThicknessNoiseShader(10, 20),                           # 14
    TipRemoverShader(20),                                   # 15
    )



current = types[frame]
name = current.name

@contextmanager
def duration(*args):
    """ Context Manager for measuring execution time """
    start = time.time()
    yield
    end = time.time()
    print("regtest: ", types[frame].__class__.__name__, end - start)

upred = QuantitativeInvisibilityUP1D(0)
Operators.select(upred)

cit = pyChainSilhouetteIterator()
Operators.bidirectional_chain(cit, NotUP1D(QuantitativeInvisibilityUP1D(0)))

func = pyInverseCurvature2DAngleF0D()
Operators.recursive_split(func, pyParameterUP0D(0.2, 0.8), NotUP1D(pyHigherNumberOfTurnsUP1D(3, .5)), 2)
Operators.sort(pyLengthBP1D())

shaders_list = [
        SamplingShader(5),
        #pyIncreasingColorShader(1, 0, 0, 0.5, 0, 1, 0, 0.9),
        current,
        #ConstantColorShader(0.050876, 0.050876, 0.050876),
    ]

with duration():
    Operators.create(DensityLowerThanUP1D(8, 0.4), shaders_list)

