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


bpy.app.debug_freestyle = True
frame = bpy.data.scenes['Scene'].frame_current

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



types = (
    pyHigherCurvature2DAngleUP0D(5),                                       # 0
    pyUEqualsUP0D(3, 5),                                                   # 1
    pyVertexNatureUP0D(Nature.T_VERTEX),                                   # 2
    pyBackTVertexUP0D(),                                                   # 3
    pyParameterUP0DGoodOne(3, 5),                                          # 4
    pyParameterUP0D(3, 5),                                                 # 5
    AndUP1D(pyUEqualsUP0D(3, 5), pyUEqualsUP0D(3, 5)),                     # 6
    OrUP1D(pyUEqualsUP0D(3, 5), pyUEqualsUP0D(3, 5)),                      # 7
    NotUP1D(pyUEqualsUP0D(3, 5)),                                          # 8
    pyNFirstUP1D(5),                                                       # 9
    pyHigherLengthUP1D(20),                                                # 10
    pyNatureUP1D(Nature.SILHOUETTE),                                       # 11
    pyHigherNumberOfTurnsUP1D(3, 5),                                       # 12
    pyDensityUP1D(3, 5),                                                   # 13
    pyZSmallerUP1D(.5),                                                    # 14
    pyZBP1D(),                                                             # 15
    pyZDiscontinuityBP1D(),                                                # 16
    pyLengthBP1D(),                                                        # 17
    pyShuffleBP1D(),                                                       # 18
    LengthThresholdUP1D(30),                                               # 19
    MaterialBoundaryUP0D(),                                                # 20
    Curvature2DAngleThresholdUP0D(30, 120),                                # 21
    Length2DThresholdUP0D(50),                                             # 22
    )

# actual setup for the render
current = types[frame]
name = current.name

upred = QuantitativeInvisibilityUP1D(0)
Operators.select(upred)

cit = cit = pyChainSilhouetteIterator()
Operators.bidirectional_chain(cit, NotUP1D(QuantitativeInvisibilityUP1D(0)))

func = pyInverseCurvature2DAngleF0D()
Operators.recursive_split(func, pyParameterUP0D(0.2, 0.8), NotUP1D(pyHigherNumberOfTurnsUP1D(3, .5)), 2)
Operators.sort(pyLengthBP1D())

if name.endswith(("BP1D", "UP1D", "UP0D", "BP0D")) or name == 'pyParameterUP0DGoodOne':
    shaders_list = [
        SamplingShader(10),
        ConstantThicknessShader(10),
        predicateTestShader(current),
    ]
else:
    raise RuntimeError("unexpected type: " + current.name)

def create():
    Operators.create(DensityLowerThanUP1D(8, 0.4), shaders_list)

with duration():
    create()