from abaqus import *
from abaqusConstants import *

session.Viewport(name='Viewport:1', origin=(0.0, 0.0), width=200,
    height=150)
session.viewports['Viewport:1'].makeCurrent()
session.viewports['Viewport:1'].maximize()

# Create a model.
from caeModules import *
from driverUtils import executeOnCaeStartup
executeOnCaeStartup()
session.viewports['Viewport:1'].partDisplay.geometryOptions.setValues(
    referenceRepresentation=ON)
import os
os.chdir(r"E:\FEM\Abaqus\2023-11-30")
mdb.saveAs(pathName=r'E:\FEM\Abaqus\2023-11-30\lesson1.cae')

s = mdb.models['Model-1'].ConstrainedSketch(name='__profile__',
    sheetSize=200.0)
g, v, d, c = s.geometry, s.vertices, s.dimensions, s.constraints
s.setPrimaryObject(option=STANDALONE)
s.Arc3Points(point1=(-75.0, 0.0), point2=(75.0, 0.0), point3=(0.0, 3))#三点画圆弧
s.HorizontalDimension(vertex1=v[0],vertex2=v[1],textPoint=(18,-18),value=150) #水平尺寸
s.ConstructionLine(point1=(-75.0,0.0),point2=(75.0,0.0))  #绘制参考线
s.CoincidentConstraint(entity1=v[0], entity2=g[3], addUndoState=False)
s.CoincidentConstraint(entity1=v[1], entity2=g[3], addUndoState=False)
s.Line(point1=(-75.0,0.0),point2=(-75.0,-4.0))
s.Line(point1=(75.0,0.0),point2=(75.0,-4.0))
s.Arc3Points(point1=(-75.0,-4.0),point2=(75.0,-4.0),point3=(0.0,1.0))

p = mdb.models['Model-1'].Part(name='siding', dimensionality=THREE_D, type=DEFORMABLE_BODY)
p = mdb.models['Model-1'].parts['siding']
p.BaseSolidExtrude(sketch=s,depth=80.0)
session.viewports['Viewport: 1'].view.setValues(nearPlane=294.031,
    farPlane=449.115, width=391.064, height=162.768, cameraPosition=(-25.6663,
    303.717, 251.81), cameraUpVector=(0.0277351, 0.22993, -0.972812),
    cameraTarget=(4.54303, -1.65753, 55.7106), viewOffsetX=16.094,
    viewOffsetY=4.40983)
mdb.save()

session.viewports['Viewport: 1'].partDisplay.setValues(sectionAssignments=ON,
    engineeringFeatures=ON)
session.viewports['Viewport: 1'].partDisplay.geometryOptions.setValues(
    referenceRepresentation=OFF)
mdb.models['Model-1'].Material(name='T300/M18')
mdb.models['Model-1'].materials['T300/M18'].Elastic(type=LAMINA, table=((
    170000.0, 9000.0, 0.34, 4800.0, 4800.0, 4500.0), ))
layupOrientation = None

p = mdb.models['Model-1'].parts['siding']
c = p.cells
cells = c.getSequenceFromMask(mask=('[#1 ]', ), )
region1=regionToolset.Region(cells=cells)
p = mdb.models['Model-1'].parts['siding']
c = p.cells
cells = c.getSequenceFromMask(mask=('[#1 ]', ), )
region2=regionToolset.Region(cells=cells)
p = mdb.models['Model-1'].parts['siding']
c = p.cells
cells = c.getSequenceFromMask(mask=('[#1 ]', ), )
region3=regionToolset.Region(cells=cells)
p = mdb.models['Model-1'].parts['siding']
c = p.cells
cells = c.getSequenceFromMask(mask=('[#1 ]', ), )
region4=regionToolset.Region(cells=cells)
p = mdb.models['Model-1'].parts['siding']
c = p.cells
cells = c.getSequenceFromMask(mask=('[#1 ]', ), )
region5=regionToolset.Region(cells=cells)

compositeLayup = mdb.models['Model-1'].parts['siding'].CompositeLayup(
    name='CompositeLayup-1', description='', elementType=CONTINUUM_SHELL,
    symmetric=False)
compositeLayup.Section(preIntegrate=OFF, integrationRule=SIMPSON,
    poissonDefinition=DEFAULT, thicknessModulus=None, temperature=GRADIENT,
    useDensity=OFF)
compositeLayup.ReferenceOrientation(orientationType=GLOBAL, localCsys=None,
    fieldName='', additionalRotationType=ROTATION_NONE, angle=0.0, axis=AXIS_3,
    stackDirection=STACK_3)
compositeLayup.CompositePly(suppressed=False, plyName='layup-1', region=region1,
    material='T300/M18', thicknessType=SPECIFY_THICKNESS, thickness=1.0,
    orientationType=SPECIFY_ORIENT, orientationValue=45.0,
    additionalRotationType=ROTATION_NONE, additionalRotationField='',
    axis=AXIS_3, angle=0.0, numIntPoints=3)
compositeLayup.CompositePly(suppressed=False, plyName='layup-2', region=region2,
    material='T300/M18', thicknessType=SPECIFY_THICKNESS, thickness=1.0,
    orientationType=SPECIFY_ORIENT, orientationValue=-45.0,
    additionalRotationType=ROTATION_NONE, additionalRotationField='',
    axis=AXIS_3, angle=0.0, numIntPoints=3)
compositeLayup.CompositePly(suppressed=False, plyName='layup-3', region=region3,
    material='T300/M18', thicknessType=SPECIFY_THICKNESS, thickness=1.0,
    orientationType=SPECIFY_ORIENT, orientationValue=0.0,
    additionalRotationType=ROTATION_NONE, additionalRotationField='',
    axis=AXIS_3, angle=0.0, numIntPoints=3)
compositeLayup.CompositePly(suppressed=False, plyName='layup-4', region=region4,
    material='T300/M18', thicknessType=SPECIFY_THICKNESS, thickness=1.0,
    orientationType=SPECIFY_ORIENT, orientationValue=90.0,
    additionalRotationType=ROTATION_NONE, additionalRotationField='',
    axis=AXIS_3, angle=0.0, numIntPoints=3)
compositeLayup.CompositePly(suppressed=False, plyName='layup-5', region=region5,
    material='T300/M18', thicknessType=SPECIFY_THICKNESS, thickness=1.0,
    orientationType=SPECIFY_ORIENT, orientationValue=0.0,
    additionalRotationType=ROTATION_NONE, additionalRotationField='',
    axis=AXIS_3, angle=0.0, numIntPoints=3)
p = mdb.models['Model-1'].parts['siding']
a = mdb.models['Model-1'].rootAssembly
session.viewports['Viewport:1'].setValues(displayedObject=a)
session.viewports['Viewport: 1'].assemblyDisplay.setValues(
    optimizationTasks=OFF, geometricRestrictions=OFF, stopConditions=OFF)
a = mdb.models['Model-1'].rootAssembly
a.DatumCsysByDefault(CARTESIAN)
p = mdb.models['Model-1'].parts['siding']
a.Instance(name='siding-1', part=p, dependent=ON)
session.viewports['Viewport: 1'].assemblyDisplay.setValues(
    adaptiveMeshConstraints=ON)

mdb.models['Model-1'].StaticStep(name='Step-1', previous='Initial',
    maxNumInc=10000, maxInc=1.0)
session.viewports['Viewport: 1'].assemblyDisplay.setValues(step='Step-1')
mdb.models['Model-1'].steps['Step-1'].setValues(initialInc=0.1)
session.viewports['Viewport: 1'].assemblyDisplay.setValues(interactions=ON,
    constraints=ON, connectors=ON, engineeringFeatures=ON,
    adaptiveMeshConstraints=OFF)
session.viewports['Viewport: 1'].assemblyDisplay.setValues(loads=ON, bcs=ON,
    predefinedFields=ON, interactions=OFF, constraints=OFF,
    engineeringFeatures=OFF)
mdb.save()

elemType = mesh.ElemType(elemCode=C3D8R, elemLibrary=STANDARD,
                          kinematicSplit=AVERAGE_STRAIN, secondOrderAccuracy=OFF,
                            hourglassControl=DEFAULT, distortionControl=DEFAULT)
p.seedPart(size=1.0, deviationFactor=0.1, minSizeFactor=0.1)
c = p.cells
p.setElementType(regions=(c,), elemTypes=(elemType,))
p.generateMesh()
v=p.vertices
print(v)
a.regenerate()
