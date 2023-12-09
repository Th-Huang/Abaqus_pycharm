import random

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

os.chdir(r"E:\FEM\Abaqus\2023-12-6")
mdb.saveAs(pathName=r'E:\FEM\Abaqus\2023-12-6\lesson4.cae')

# draw a sketch
s = mdb.models['Model-1'].ConstrainedSketch(name='__profile__',
                                            sheetSize=200.0)
g, v, d, c = s.geometry, s.vertices, s.dimensions, s.constraints
s.setPrimaryObject(option=STANDALONE)
s.Arc3Points(point1=(-500.0, 0.0), point2=(500.0, 0.0), point3=(0.0, 30))  # 三点画圆弧
s.HorizontalDimension(vertex1=v[0], vertex2=v[1], textPoint=(18, -18), value=1000)  # 水平尺寸
s.ConstructionLine(point1=(-500.0, 0.0), point2=(500.0, 0.0))  # 绘制参考线
s.CoincidentConstraint(entity1=v[0], entity2=g[3], addUndoState=False)
s.CoincidentConstraint(entity1=v[1], entity2=g[3], addUndoState=False)
s.Line(point1=(-500.0, 0.0), point2=(-500.0, 6.0))
s.Line(point1=(500.0, 0.0), point2=(500.00, 6.0))
s.Arc3Points(point1=(-500.0, 6.0), point2=(500.0, 6.0), point3=(0.0, 36.0))

p = mdb.models['Model-1'].Part(name='siding', dimensionality=THREE_D, type=DEFORMABLE_BODY)
p = mdb.models['Model-1'].parts['siding']
p.BaseSolidExtrude(sketch=s, depth=400.0)
mdb.save()

# 六个参考点的初始坐标
pt1 = mdb.models['Model-1'].parts['siding'].DatumPointByCoordinate(coords=(300, 18.0, 50))
pt2 = mdb.models['Model-1'].parts['siding'].DatumPointByCoordinate(coords=(-300, 18.0, 50))
pt3 = mdb.models['Model-1'].parts['siding'].DatumPointByCoordinate(coords=(-300, 18.0, 350))
pt4 = mdb.models['Model-1'].parts['siding'].DatumPointByCoordinate(coords=(300, 18.0, 350))
pt5 = mdb.models['Model-1'].parts['siding'].DatumPointByCoordinate(coords=(0, 29.5, 50.5))
pt6 = mdb.models['Model-1'].parts['siding'].DatumPointByCoordinate(coords=(0, 29.5, 350.5))  # 以坐标的方式创建参考点们

datumpoint = []
datumpoint.append(pt1)
datumpoint.append(pt2)
datumpoint.append(pt3)
datumpoint.append(pt4)
datumpoint.append(pt5)
datumpoint.append(pt6)

for i in range(0, 6):
    # 按照YZ平面切割
    a = mdb.models['Model-1'].parts['siding'].DatumAxisByPrincipalAxis(principalAxis=XAXIS)
    aid = a.id
    for j in range(0, 10):
        d = mdb.models['Model-1'].parts['siding'].DatumPointByCoordinate(coords=(
        math.floor(datumpoint[i].xValue - 5 + j), math.floor(datumpoint[i].yValue),
        math.floor(datumpoint[i].zValue)))  # 以坐标的方式创建参考点们
        did = d.id  # 参考点的id号
        px = mdb.models['Model-1'].parts['siding'].DatumPlaneByPointNormal(
            normal=mdb.models['Model-1'].parts['siding'].datums[aid],
            point=mdb.models['Model-1'].parts['siding'].datums[did])  # 创建参考平面,将用来切割模型
        pxid = px.id  # 参考平面的id号
        try:
            mdb.models['Model-1'].parts['siding'].PartitionCellByDatumPlane(
                cells=mdb.models['Model-1'].parts['siding'].cells[:],
                datumPlane=mdb.models['Model-1'].parts['siding'].datums[pxid])
        except:
            continue

    # 按照XY平面切割
    b = mdb.models['Model-1'].parts['siding'].DatumAxisByPrincipalAxis(principalAxis=ZAXIS)
    bid = b.id
    for j in range(0, 10):
        d = mdb.models['Model-1'].parts['siding'].DatumPointByCoordinate(coords=(
        math.floor(datumpoint[i].xValue), math.floor(datumpoint[i].yValue),
        math.floor(datumpoint[i].zValue - 5 + j)))  # 以坐标的方式创建参考点们
        did = d.id  # 参考点的id号
        pz = mdb.models['Model-1'].parts['siding'].DatumPlaneByPointNormal(
            normal=mdb.models['Model-1'].parts['siding'].datums[bid],
            point=mdb.models['Model-1'].parts['siding'].datums[did])  # 创建参考平面,将用来切割模型
        pzid = pz.id  # 参考平面的id号
        try:
            mdb.models['Model-1'].parts['siding'].PartitionCellByDatumPlane(
                cells=mdb.models['Model-1'].parts['siding'].cells[:],
                datumPlane=mdb.models['Model-1'].parts['siding'].datums[pzid])
        except:
            continue
mdb.save()

# create material
session.viewports['Viewport: 1'].partDisplay.setValues(sectionAssignments=ON,
                                                        engineeringFeatures=ON)
session.viewports['Viewport: 1'].partDisplay.geometryOptions.setValues(
    referenceRepresentation=OFF)
mdb.models['Model-1'].Material(name='T300/M18')
mdb.models['Model-1'].materials['T300/M18'].Elastic(type=LAMINA, table=((
                                                                            170000.0, 9000.0, 0.34, 4800.0, 4800.0,
                                                                            4500.0),))
layupOrientation = None

p = mdb.models['Model-1'].parts['siding']
c = p.cells[:]
region1 = regionToolset.Region(cells=c)
p = mdb.models['Model-1'].parts['siding']
c = p.cells[:]
region2 = regionToolset.Region(cells=c)
p = mdb.models['Model-1'].parts['siding']
c = p.cells[:]
region3 = regionToolset.Region(cells=c)
p = mdb.models['Model-1'].parts['siding']
c = p.cells[:]
region4 = regionToolset.Region(cells=c)
p = mdb.models['Model-1'].parts['siding']
c = p.cells[:]
region5 = regionToolset.Region(cells=c)

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

# create step
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

# create mesh
elemType = mesh.ElemType(elemCode=SC8R, elemLibrary=STANDARD,
                            kinematicSplit=AVERAGE_STRAIN, secondOrderAccuracy=OFF,
                            hourglassControl=DEFAULT, distortionControl=DEFAULT)
p.seedPart(size=3.0, deviationFactor=0.1, minSizeFactor=0.1)
c = p.cells
p.setElementType(regions=(c,), elemTypes=(elemType,))
p.generateMesh()
a.regenerate()

for numjob in range(0,50):
    randpt1 = mdb.models['Model-1'].parts['siding'].DatumPointByCoordinate(
        coords=(pt1.xValue + random.uniform(-0.5, 0.5), pt1.yValue + random.uniform(-0.5, 0.5), pt1.zValue + random.uniform(-0.5, 0.5)))
    randpt2 = mdb.models['Model-1'].parts['siding'].DatumPointByCoordinate(
        coords=(pt2.xValue + random.uniform(-0.5, 0.5), pt2.yValue + random.uniform(-0.5, 0.5), pt2.zValue + random.uniform(-0.5, 0.5)))
    randpt3 = mdb.models['Model-1'].parts['siding'].DatumPointByCoordinate(
        coords=(pt3.xValue + random.uniform(-0.5, 0.5), pt3.yValue + random.uniform(-0.5, 0.5), pt3.zValue + random.uniform(-0.5, 0.5)))
    randpt4 = mdb.models['Model-1'].parts['siding'].DatumPointByCoordinate(
        coords=(pt4.xValue + random.uniform(-0.5, 0.5), pt4.yValue + random.uniform(-0.5, 0.5), pt4.zValue + random.uniform(-0.5, 0.5)))
    randpt5 = mdb.models['Model-1'].parts['siding'].DatumPointByCoordinate(
        coords=(pt5.xValue + random.uniform(-0.5, 0.5), pt5.yValue + random.uniform(-0.5, 0.5), pt5.zValue + random.uniform(-0.5, 0.5)))
    randpt6 = mdb.models['Model-1'].parts['siding'].DatumPointByCoordinate(
        coords=(pt6.xValue + random.uniform(-0.5, 0.5), pt6.yValue + random.uniform(-0.5, 0.5), pt6.zValue + random.uniform(-0.5, 0.5)))

    print("The coordinate of random point1: ",randpt1.xValue,randpt1.yValue,randpt1.zValue)
    print("The coordinate of random point2: ",randpt2.xValue,randpt2.yValue,randpt2.zValue)
    print("The coordinate of random point3: ",randpt3.xValue,randpt3.yValue,randpt3.zValue)
    print("The coordinate of random point4: ",randpt4.xValue,randpt4.yValue,randpt4.zValue)
    print("The coordinate of random point5: ",randpt5.xValue,randpt5.yValue,randpt5.zValue)
    print("The coordinate of random point6: ",randpt6.xValue,randpt6.yValue,randpt6.zValue)


    # select the point origin
    a = mdb.models['Model-1'].rootAssembly
    v = a.instances['siding-1'].vertices
    verts1 = v.getByBoundingBox(xMin=randpt1.xValue - 5, yMin=randpt1.yValue - 5, zMin=randpt1.zValue - 5, xMax=randpt1.xValue + 5,
                                yMax=randpt1.yValue + 5, zMax=randpt1.zValue + 5)
    mindist1 = 1000000
    for i in range(len(verts1)):
        dist = math.sqrt((verts1[i].pointOn[0][0] - randpt1.xValue) ** 2 + (verts1[i].pointOn[0][1] - randpt1.yValue) ** 2 + (
                    verts1[i].pointOn[0][2] - randpt1.zValue) ** 2)
        if dist < mindist1:
            mindist1 = dist
            index1 = i
    print("The closest point of datums point1: ",verts1[index1].pointOn)
    findpt1 = v.findAt(verts1[index1].pointOn)
    point1set = a.Set(vertices=findpt1, name='Set-1')

    verts2 = v.getByBoundingBox(xMin=randpt2.xValue - 5, yMin=randpt2.yValue - 5, zMin=randpt2.zValue - 5, xMax=randpt2.xValue + 5,
                                yMax=randpt2.yValue + 5, zMax=randpt2.zValue + 5)
    mindist2 = 1000000
    for i in range(len(verts2)):
        dist = math.sqrt((verts2[i].pointOn[0][0] - randpt2.xValue) ** 2 + (verts2[i].pointOn[0][1] - randpt2.yValue) ** 2 + (
                    verts2[i].pointOn[0][2] - randpt2.zValue) ** 2)
        if dist < mindist2:
            mindist2 = dist
            index2 = i
    print("The closest point of datums point2: ",verts2[index2].pointOn)
    findpt2 = v.findAt(verts2[index2].pointOn)
    point2set = a.Set(vertices=findpt2, name='Set-2')

    verts3 = v.getByBoundingBox(xMin=randpt3.xValue - 5, yMin=randpt3.yValue - 5, zMin=randpt3.zValue - 5, xMax=randpt3.xValue + 5,
                                yMax=randpt3.yValue + 5, zMax=randpt3.zValue + 5)
    mindist3 = 1000000
    for i in range(len(verts3)):
        dist = math.sqrt((verts3[i].pointOn[0][0] - randpt3.xValue) ** 2 + (verts3[i].pointOn[0][1] - randpt3.yValue) ** 2 + (
                    verts3[i].pointOn[0][2] - randpt3.zValue) ** 2)
        if dist < mindist3:
            mindist3 = dist
            index3 = i
    print("The closest point of datums point3: ",verts3[index3].pointOn)
    findpt3 = v.findAt(verts3[index3].pointOn)
    point3set = a.Set(vertices=findpt3, name='Set-3')

    verts4 = v.getByBoundingBox(xMin=randpt4.xValue - 5, yMin=randpt4.yValue - 5, zMin=randpt4.zValue - 5, xMax=randpt4.xValue + 5,
                                yMax=randpt4.yValue + 5, zMax=randpt4.zValue + 5)
    mindist4 = 1000000
    for i in range(len(verts4)):
        dist = math.sqrt((verts4[i].pointOn[0][0] - randpt4.xValue) ** 2 + (verts4[i].pointOn[0][1] - randpt4.yValue) ** 2 + (
                    verts4[i].pointOn[0][2] - randpt4.zValue) ** 2)
        if dist < mindist4:
            mindist4 = dist
            index4 = i
    print("The closest point of datums point4: ",verts4[index4].pointOn)
    findpt4 = v.findAt(verts4[index4].pointOn)
    point4set = a.Set(vertices=findpt4, name='Set-4')

    verts5 = v.getByBoundingBox(xMin=randpt5.xValue - 5, yMin=randpt5.yValue - 5, zMin=randpt5.zValue - 5, xMax=randpt5.xValue + 5,
                                yMax=randpt5.yValue + 5, zMax=randpt5.zValue + 5)
    mindist5 = 1000000
    for i in range(len(verts5)):
        dist = math.sqrt((verts5[i].pointOn[0][0] - randpt5.xValue) ** 2 + (verts5[i].pointOn[0][1] - randpt5.yValue) ** 2 + (
                    verts5[i].pointOn[0][2] - randpt5.zValue) ** 2)
        if dist < mindist5:
            mindist5 = dist
            index5 = i
    print("The closest point of datums point5: ",verts5[index5].pointOn)
    findpt5 = v.findAt(verts5[index5].pointOn)
    point5set = a.Set(vertices=findpt5, name='Set-5')

    verts6 = v.getByBoundingBox(xMin=randpt6.xValue - 6, yMin=randpt6.yValue - 6, zMin=randpt6.zValue - 6, xMax=randpt6.xValue + 6,
                                yMax=randpt6.yValue + 6, zMax=randpt6.zValue + 6)
    mindist6 = 1000000
    for i in range(len(verts6)):
        dist = math.sqrt((verts6[i].pointOn[0][0] - randpt6.xValue) ** 2 + (verts6[i].pointOn[0][1] - randpt6.yValue) ** 2 + (
                    verts6[i].pointOn[0][2] - randpt6.zValue) ** 2)
        if dist < mindist6:
            mindist6 = dist
            index6 = i
    print("The closest point of datums point6: ",verts6[index6].pointOn)
    findpt6 = v.findAt(verts6[index6].pointOn)
    point6set = a.Set(vertices=findpt6, name='Set-6')

    # create boundary conditions
    a = mdb.models['Model-1'].rootAssembly
    region1 = a.sets['Set-1']
    up1 = pt1.xValue - verts1[index1].pointOn[0][0]
    up2 = pt1.yValue - verts1[index1].pointOn[0][1]
    up3 = pt1.zValue - verts1[index1].pointOn[0][2]
    mdb.models['Model-1'].DisplacementBC(name='BC-1', createStepName='Step-1',
                                            region=region1, u1=up1, u2=up2, u3=up3, ur1=UNSET, ur2=UNSET, ur3=UNSET,
                                            amplitude=UNSET, distributionType=UNIFORM, fieldName='', localCsys=None)

    a = mdb.models['Model-1'].rootAssembly
    region2 = a.sets['Set-2']
    up1 = pt2.xValue - verts2[index2].pointOn[0][0]
    up2 = pt2.yValue - verts2[index2].pointOn[0][1]
    up3 = pt2.zValue - verts2[index2].pointOn[0][2]
    mdb.models['Model-1'].DisplacementBC(name='BC-2', createStepName='Step-1',
                                            region=region2, u1=up1, u2=up2, u3=up3, ur1=UNSET, ur2=UNSET, ur3=UNSET,
                                            amplitude=UNSET, distributionType=UNIFORM, fieldName='', localCsys=None)

    a = mdb.models['Model-1'].rootAssembly
    region3 = a.sets['Set-3']
    up1 = pt3.xValue - verts3[index3].pointOn[0][0]
    up2 = pt3.yValue - verts3[index3].pointOn[0][1]
    up3 = pt3.zValue - verts3[index3].pointOn[0][2]
    mdb.models['Model-1'].DisplacementBC(name='BC-3', createStepName='Step-1',
                                            region=region3, u1=up1, u2=up2, u3=up3, ur1=UNSET, ur2=UNSET, ur3=UNSET,
                                            amplitude=UNSET, distributionType=UNIFORM, fieldName='', localCsys=None)

    a = mdb.models['Model-1'].rootAssembly
    region4 = a.sets['Set-4']
    up1 = pt4.xValue - verts4[index4].pointOn[0][0]
    up2 = pt4.yValue - verts4[index4].pointOn[0][1]
    up3 = pt4.zValue - verts4[index4].pointOn[0][2]
    mdb.models['Model-1'].DisplacementBC(name='BC-4', createStepName='Step-1',
                                            region=region4, u1=up1, u2=up2, u3=up3, ur1=UNSET, ur2=UNSET, ur3=UNSET,
                                            amplitude=UNSET, distributionType=UNIFORM, fieldName='', localCsys=None)

    a = mdb.models['Model-1'].rootAssembly
    region5 = a.sets['Set-5']
    up1 = pt5.xValue - verts5[index5].pointOn[0][0]
    up2 = pt5.yValue - verts5[index5].pointOn[0][1]
    up3 = pt5.zValue - verts5[index5].pointOn[0][2]
    mdb.models['Model-1'].DisplacementBC(name='BC-5', createStepName='Step-1',
                                            region=region5, u1=up1, u2=up2, u3=up3, ur1=UNSET, ur2=UNSET, ur3=UNSET,
                                            amplitude=UNSET, distributionType=UNIFORM, fieldName='', localCsys=None)

    a = mdb.models['Model-1'].rootAssembly
    region6 = a.sets['Set-6']
    up1 = pt6.xValue - verts6[index6].pointOn[0][0]
    up2 = pt6.yValue - verts6[index6].pointOn[0][1]
    up3 = pt6.zValue - verts6[index6].pointOn[0][2]
    mdb.models['Model-1'].DisplacementBC(name='BC-6', createStepName='Step-1',
                                            region=region6, u1=up1, u2=up2, u3=up3, ur1=UNSET, ur2=UNSET, ur3=UNSET,
                                            amplitude=UNSET, distributionType=UNIFORM, fieldName='', localCsys=None)



    # create job
    mdb.Job(name='Job-'+str(numjob), model='Model-1', description='', type=ANALYSIS,
            atTime=None, waitMinutes=0, waitHours=0, queue=None, memory=90,
            memoryUnits=PERCENTAGE, getMemoryFromAnalysis=True,
            explicitPrecision=SINGLE, nodalOutputPrecision=SINGLE, echoPrint=OFF,
            modelPrint=OFF, contactPrint=OFF, historyPrint=OFF, userSubroutine='',
            scratch='', resultsFormat=ODB, multiprocessingMode=DEFAULT, numCpus=1,
            numGPUs=4)
    mdb.jobs['Job-'+str(numjob)].submit()
    mdb.jobs['Job-'+str(numjob)].waitForCompletion()
    print('Job-'+str(numjob)+' is done!')
mdb.save()