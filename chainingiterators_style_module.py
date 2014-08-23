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
    )

# actual setup for the render
current = types[frame]
name = current.name 

upred = QuantitativeInvisibilityUP1D(0)
Operators.select(upred)

cit = current 
Operators.bidirectional_chain(cit, NotUP1D(QuantitativeInvisibilityUP1D(0)))

func = pyInverseCurvature2DAngleF0D()
Operators.recursive_split(func, pyParameterUP0D(0.2, 0.8), NotUP1D(pyHigherNumberOfTurnsUP1D(3, .5)), 2)
Operators.sort(pyLengthBP1D())

if name.endswith("Iterator"):
    shaders_list = [
        SamplingShader(10),
    ]
else:
    raise RuntimeError("unexpected type: " + current.name)

def create():
    Operators.create(DensityLowerThanUP1D(8, 0.4), shaders_list)

with duration():
    create()