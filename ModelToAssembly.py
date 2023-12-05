from abaqus import *
from abaqusConstants import *
import math

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
os.chdir(r"E:\FEM\Abaqus\2023-12-5")
mdb.saveAs(pathName=r'E:\FEM\Abaqus\2023-12-4\lesson1.cae')

# draw a sketch
s = mdb.models['Model-1'].ConstrainedSketch(name='__profile__',
    sheetSize=200.0)
g, v, d, c = s.geometry, s.vertices, s.dimensions, s.constraints
s.setPrimaryObject(option=STANDALONE)
s.Arc3Points(point1=(-500.0, 0.0), point2=(500.0, 0.0), point3=(0.0, 30))#三点画圆弧
s.HorizontalDimension(vertex1=v[0],vertex2=v[1],textPoint=(18,-18),value=1000) #水平尺寸
s.ConstructionLine(point1=(-500.0,0.0),point2=(500.0,0.0))  #绘制参考线
s.CoincidentConstraint(entity1=v[0], entity2=g[3], addUndoState=False)
s.CoincidentConstraint(entity1=v[1], entity2=g[3], addUndoState=False)
s.Line(point1=(-500.0,0.0),point2=(-500.0,-4.0))
s.Line(point1=(500.0,0.0),point2=(500.00,-4.0))
s.Arc3Points(point1=(-500.0,-4.0),point2=(500.0,-4.0),point3=(0.0,26.0))

p = mdb.models['Model-1'].Part(name='siding', dimensionality=THREE_D, type=DEFORMABLE_BODY)
p = mdb.models['Model-1'].parts['siding']
p.BaseSolidExtrude(sketch=s,depth=400.0)
mdb.save()

#Segmentation
#按照YZ平面切割
a = mdb.models['Model-1'].parts['siding'].DatumAxisByPrincipalAxis(principalAxis=XAXIS)
aid = a.id
for i in range (1,1000):
    d = mdb.models['Model-1'].parts['siding'].DatumPointByCoordinate(coords=(-500 + i, 0.0, 0.0))  # 以坐标的方式创建参考点们
    did = d.id  # 参考点的id号
    p = mdb.models['Model-1'].parts['siding'].DatumPlaneByPointNormal(
        normal=mdb.models['Model-1'].parts['siding'].datums[aid],
        point=mdb.models['Model-1'].parts['siding'].datums[did])  # 创建参考平面,将用来切割模型
    pid = p.id  # 参考平面的id号
    mdb.models['Model-1'].parts['siding'].PartitionCellByDatumPlane(cells=mdb.models['Model-1'].parts['siding'].cells[:],
                                                                    datumPlane=mdb.models['Model-1'].parts['siding'].datums[
                                                                    pid])
    if(i%100==0):
        print("segmentByXAxis:", i)

#按照XY平面切割
a = mdb.models['Model-1'].parts['siding'].DatumAxisByPrincipalAxis(principalAxis=ZAXIS)
aid = a.id
for i in range (1,400):
    d = mdb.models['Model-1'].parts['siding'].DatumPointByCoordinate(coords=(0.0, 0.0, i))  # 以坐标的方式创建参考点们
    did = d.id  # 参考点的id号
    p = mdb.models['Model-1'].parts['siding'].DatumPlaneByPointNormal(
        normal=mdb.models['Model-1'].parts['siding'].datums[aid],
        point=mdb.models['Model-1'].parts['siding'].datums[did])  # 创建参考平面,将用来切割模型
    pid = p.id  # 参考平面的id号
    mdb.models['Model-1'].parts['siding'].PartitionCellByDatumPlane(cells=mdb.models['Model-1'].parts['siding'].cells[:],
                                                                    datumPlane=mdb.models['Model-1'].parts['siding'].datums[
                                                                    pid])
    if(i%100==0):
        print("SegmentByZAxis:", i)


#create material
session.viewports['Viewport: 1'].partDisplay.setValues(sectionAssignments=ON,
    engineeringFeatures=ON)
session.viewports['Viewport: 1'].partDisplay.geometryOptions.setValues(
    referenceRepresentation=OFF)
mdb.models['Model-1'].Material(name='T300/M18')
mdb.models['Model-1'].materials['T300/M18'].Elastic(type=LAMINA, table=((
    170000.0, 9000.0, 0.34, 4800.0, 4800.0, 4500.0), ))
layupOrientation = None


p = mdb.models['Model-1'].parts['siding']
c = p.cells[:]
region1=regionToolset.Region(cells=c)
p = mdb.models['Model-1'].parts['siding']
c = p.cells[:]
region2=regionToolset.Region(cells=c)
p = mdb.models['Model-1'].parts['siding']
c = p.cells[:]
region3=regionToolset.Region(cells=c)
p = mdb.models['Model-1'].parts['siding']
c = p.cells[:]
region4=regionToolset.Region(cells=c)
p = mdb.models['Model-1'].parts['siding']
c = p.cells[:]
region5=regionToolset.Region(cells=c)


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

# create assembly
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