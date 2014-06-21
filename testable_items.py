# list of all freestyle python functions we can test

items = (
        "pyChainSilhouetteIterator",                            #  0
        "pyChainSilhouetteGenericIterator",                     #  1
        "pyExternalContourChainingIterator",                    #  2
        "pySketchyChainSilhouetteIterator",                     #  3
        "pySketchyChainingIterator",                            #  4
        "pyFillOcclusionsRelativeChainingIterator",             #  5
        "pyFillOcclusionsAbsoluteChainingIterator",             #  6
        "pyFillOcclusionsAbsoluteAndRelativeChainingIterator",  #  7
        "pyFillQi0AbsoluteAndRelativeChainingIterator",         #  8
        "pyNoIdChainSilhouetteIterator",                        #  9
        "pyDepthDiscontinuityThicknessShader",                  #  10
        "pyConstantThicknessShader",                            #  11
        "pyFXSVaryingThicknessWithDensityShader",               #  12
        "pyIncreasingThicknessShader",                          #  13
        "pyConstrainedIncreasingThicknessShader",               #  14
        "pyDecreasingThicknessShader",                          #  15
        "pyNonLinearVaryingThicknessShader",                    #  16
        "pySLERPThicknessShader",                               #  17
        "pyTVertexThickenerShader",                             #  18
        "pyImportance2DThicknessShader",                        #  19
        "pyImportance3DThicknessShader",                        #  20
        "pyZDependingThicknessShader",                          #  21
        "pyConstantColorShader",                                #  22
        "pyIncreasingColorShader",                              #  23
        "pyInterpolateColorShader",                             #  24
        "pyMaterialColorShader",                                #  25
        "pyRandomColorShader",                                  #  26
        "py2DCurvatureColorShader",                             #  27
        "pyTimeColorShader",                                    #  28
        "pySamplingShader",                                     #  29
        "pyBackboneStretcherShader",                            #  30
        "pyLengthDependingBackboneStretcherShader",             #  31
        "pyGuidingLineShader",                                  #  32
        "pyBackboneStretcherNoCuspShader",                      #  33
        "pyDiffusion2Shader",                                   #  34
        "pyTipRemoverShader",                                   #  35
        "pyTVertexRemoverShader",                               #  36
        "pyHLRShader",                                          #  37
        "pySinusDisplacementShader",                            #  38
        "pyPerlinNoise1DShader",                                #  39
        "pyPerlinNoise2DShader",                                #  40
        "pyBluePrintCirclesShader",                             #  41
        "pyBluePrintEllipsesShader",                            #  42
        "pyBluePrintSquaresShader",                             #  43
        "pyBluePrintDirectedSquaresShader",                     #  44
        "pyModulateAlphaShader",                                #  45
        "pyHigherCurvature2DAngleUP0D",                         #  46
        "pyUEqualsUP0D",                                        #  47
        "pyVertexNatureUP0D",                                   #  48
        "pyBackTVertexUP0D",                                    #  49
        "pyParameterUP0DGoodOne",                               #  50
        "pyParameterUP0D",                                      #  51
        "AndUP1D",                                              #  52
        "OrUP1D",                                               #  53
        "NotUP1D",                                              #  54
        "pyNFirstUP1D",                                         #  55
        "pyHigherLengthUP1D",                                   #  56
        "pyNatureUP1D",                                         #  57
        "pyHigherNumberOfTurnsUP1D",                            #  58
        "pyDensityUP1D",                                        #  59
        "pyZSmallerUP1D",                                       #  60
        "pyZBP1D",                                              #  61
        "pyZDiscontinuityBP1D",                                 #  62
        "pyLengthBP1D",                                         #  63
        "pyShuffleBP1D",                                        #  64
        "pyIsOccludedByUP1D",                                   #  65
        "RoundCapShader",                                       #  66
        "SquareCapShader",                                      #  67
)

# code used to generate above sequence
#for i, item in enumerate(items): _ = '"' + str(item) + '"' + ",";print(_.ljust(54), " # ", i)


# the types used in `regression_test.py`
types = (
    "pyChainSilhouetteIterator()",                                            #  0
    "pyChainSilhouetteGenericIterator()",                                     #  1
    "pyExternalContourChainingIterator()",                                    #  2
    "pySketchyChainSilhouetteIterator()",                                     #  3
    "pySketchyChainingIterator()",                                            #  4
    "pyFillOcclusionsRelativeChainingIterator(.2)",                           #  5
    "pyFillOcclusionsAbsoluteChainingIterator(20)",                           #  6
    "pyFillOcclusionsAbsoluteAndRelativeChainingIterator(.2, 20)",            #  7
    "pyFillQi0AbsoluteAndRelativeChainingIterator(.2, 20)",                   #  8
    "pyNoIdChainSilhouetteIterator()",                                        #  9
    "pyDepthDiscontinuityThicknessShader(3, 5)",                              #  10
    "pyConstantThicknessShader(5)",                                           #  11
    "pyFXSVaryingThicknessWithDensityShader(5, 3, 5, 3, 5)",                  #  12
    "pyIncreasingThicknessShader(2, 5)",                                      #  13
    "pyConstrainedIncreasingThicknessShader(3, 5, .5)",                       #  14
    "pyDecreasingThicknessShader(3, 5)",                                      #  15
    "pyNonLinearVaryingThicknessShader(10, 5, 3)",                            #  16
    "pySLERPThicknessShader(3, 5)",                                           #  17
    "pyTVertexThickenerShader()",                                             #  18
    "pyImportance2DThicknessShader(1, 2, 3, 3, 5)",                           #  19
    "pyImportance3DThicknessShader(1, 2, 3, 4, 3, 5)",                        #  20
    "pyZDependingThicknessShader(3, 5)",                                      #  21
    "pyConstantColorShader(1, 0, 0)",                                         #  22
    "pyIncreasingColorShader(1, 0, 0, 1, 0, 1, 0, 1)",                        #  23
    "pyInterpolateColorShader(1, 0, 0, 1, 0, 1, 0, 1)",                       #  24
    "pyMaterialColorShader()",                                                #  25
    "pyRandomColorShader()",                                                  #  26
    "py2DCurvatureColorShader()",                                             #  27
    "pyTimeColorShader()",                                                    #  28
    "pySamplingShader(10)",                                                   #  29
    "pyBackboneStretcherShader(20)",                                          #  30
    "pyLengthDependingBackboneStretcherShader(1)",                            #  31
    "pyGuidingLineShader()",                                                  #  32
    "pyBackboneStretcherNoCuspShader(20)",                                    #  33
    "pyDiffusion2Shader(.3, 4)",                                              #  34
    "pyTipRemoverShader(5)",                                                  #  35
    "pyTVertexRemoverShader()",                                               #  36
    "pyHLRShader()",                                                          #  37
    "pySinusDisplacementShader(20, 17)",                                      #  38
    "pyPerlinNoise1DShader(seed=2)",                                          #  39
    "pyPerlinNoise2DShader(seed=2)",                                          #  40
    "pyBluePrintCirclesShader(turns=4, random_radius=0, random_center=0)",    #  41
    "pyBluePrintEllipsesShader(turns=4, random_radius=0, random_center=0)",   #  42
    "pyBluePrintSquaresShader()",                                             #  43
    "pyBluePrintDirectedSquaresShader()",                                     #  44
    "pyModulateAlphaShader()",                                                #  45
    "pyHigherCurvature2DAngleUP0D(5)",                                        #  46
    "pyUEqualsUP0D(3, 5)",                                                    #  47
    "pyVertexNatureUP0D(Nature.T_VERTEX)",                                    #  48
    "pyBackTVertexUP0D()",                                                    #  49
    "pyParameterUP0DGoodOne(3, 5)",                                           #  50
    "pyParameterUP0D(3, 5)",                                                  #  51
    "AndUP1D(pyUEqualsUP0D(3, 5), pyUEqualsUP0D(3, 5))",                      #  52
    "OrUP1D(pyUEqualsUP0D(3, 5), pyUEqualsUP0D(3, 5))",                       #  53
    "NotUP1D(pyUEqualsUP0D(3, 5))",                                           #  54
    "pyNFirstUP1D(5)",                                                        #  55
    "pyHigherLengthUP1D(20)",                                                 #  56
    "pyNatureUP1D(Nature.SILHOUETTE)",                                        #  57
    "pyHigherNumberOfTurnsUP1D(3, 5)",                                        #  58
    "pyDensityUP1D(3, 5)",                                                    #  59
    "pyZSmallerUP1D(.5)",                                                     #  60
    "pyZBP1D()",                                                              #  61
    "pyZDiscontinuityBP1D()",                                                 #  62
    "pyLengthBP1D()",                                                         #  63
    "pyShuffleBP1D()",                                                        #  64
    "pyIsOccludedByUP1D(0)",                                                  #  65
    "RoundCapShader()",                                                       #  66
    "SquareCapShader()",                                                      #  67
)




# predicates not currently used (they lead to crashes or)
# are difficult to test. 


# not present in old version of predicates.py
#ObjectNamesUP1D(("Plane", "a")),
#QuantitativeInvisibilityRangeUP1D(3, 5),
## viewmap stuff; doesn't work and leads to crashes
# pyLowSteerableViewMapDensityUP1D(3, 5),
# pyLowDirectionalViewMapDensityUP1D(3, 5, 2),
# pyHighSteerableViewMapDensityUP1D(3, 2),
# pyHighDirectionalViewMapDensityUP1D(3, 5, 2),
# pyHighViewMapDensityUP1D(3, 5),
#pyDensityFunctorUP1D(), #just difficult
#occlusion also seems buggy
#pyIsOccludedByUP1D(1), 
#pyIsInOccludersListUP1D(1),
#pyIsOccludedByItselfUP1D(),
#pyIsOccludedByIdListUP1D((0, 1, 2)),
#pyShapeIdListUP1D((0, 1, 2)),
#pyShapeIdUP1D(1), # deprecated?
#pyHighDensityAnisotropyUP1D(5, 2),
#pyHighViewMapGradientNormUP1D(3, 5),
#pyDensityVariableSigmaUP1D(), difficult
#pyClosedCurveUP1D(),
#pySilhouetteFirstBP1D(),
#pyNatureBP1D(),
#pyViewMapGradientNormBP1D(5),