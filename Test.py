from abaqus import *
from abaqusConstants import *
from caeModules import *

if mdb.models.has_key('myModel'):
    m = mdb.models['myModel']
else:
    m = mdb.Model(name='myModel')

Sr = m.ConstrainedSketch(name='Revolve',sheetSize=200.0)        #生成一个新的草绘对象
g = Sr.geometry
Sr.setPrimaryObject(option=SUPERIMPOSE)                         #将当前草绘图设置为窗口的初始显示对象，SUPERIMPOSE:在原窗口上叠加显示草绘图状态
cline = Sr.ConstructionLine((0,20),(0,-20))                     #利用两点生成辅助线元素
Sr.assignCenterline(line=cline)                                 #指定某个辅助线作为旋转轴
line1 = Sr.Line(point1=(0.0,15.0),point2=(15.0,15.0))
line2 = Sr.Line(point1=(15.0,15.0),point2=(15.0,0.0))
line3 = Sr.Line(point1=(15.0,0.0),point2=(0.0,0.0))
line4 = Sr.Line(point1=(5.0,0.0),point2=(5.0,15.0))           
Sr.autoTrimCurve(curve1=line1,point1=(0.0,15.0))                 #将选择的元素的特定部分删去
Sr.autoTrimCurve(curve1=line3,point1=(0.0,0.0))               
Sr.unsetPrimaryObject()                                          #取消当前草绘图的初始显示对象

Se = m.ConstrainedSketch(name='Extrude',sheetSize=200.0)        
g, c = Se.geometry, Se.constraints                             
Se.setPrimaryObject(option=STANDALONE)                           #将当前草绘图设置为窗口的初始显示对象，STABDALONE:清空原窗口再显示草绘状态
line1 = Se.Line(point1=(0.0,15.0),point2=(15.0,15.0))            
line2 = Se.Line(point1=(15.0,15.0),point2=(15.0,0.0))
line3 = Se.Line(point1=(15.0,0.0),point2=(0.0,0.0))
line4 = Se.Line(point1=(5.0,0.0),point2=(5.0,15.0))           
Se.PerpendicularConstraint(entity1=line3,entity2=line4)           #约束两个元素垂直
Se.autoDimension(objectList=(line4,))                             #将某个几何元素施加尺寸位置约束
Se.unsetPrimaryObject()

p1 = mdb.models['myModel'].Part(name='Part-1',dimensionality=THREE_D,type=DEFORMABLE_BODY)   #创建一个新的零件对象 
p1.BaseSolidExtrude(sketch=Se,depth=10.0)                                                    #创建一个feature对象，其作用是通过拉伸给定的草绘图生成体

p2 = mdb.models['myModel'].Part(name='Part-2',dimensionality=THREE_D,type=DEFORMABLE_BODY)   #创建一个新的零件对象
p2.BaseSolidRevolve(sketch=Sr,angle=360.0)                                                   #创建一个feature对象，其作用是通过旋转给定的草绘图生成体


#定义材料属性
mdb.models['myModel'].Material(name='Steel')
mdb.models['myModel'].materials['Steel'].Density(table=((7.85e-09, ), ))         #Debsity:密度
mdb.models['myModel'].materials['Steel'].Elastic(table=((200000.0, 0.3), ))      #Elastic:弹性
mdb.models['myModel'].materials['Steel'].Plastic(table=((450.0,0.0),(480.0,0.05),(490.0,0.15),(500.0,0.3)))  #Plastic:塑性
mdb.models['myModel'].materials['Steel'].Expansion(table=((1.0e-05, ), ))        #Expansion:膨胀

#定义截面属性
mdb.models['myModel'].HomogeneousSolidSection(name='Section-Steel',material='Steel',thickness=None)   #创建一个新的截面对象,均质实体截面

#将截面属性分配给零件
c2 = p2.cells                                         #C2包含P2的所有体元素
region2 = regionToolset.Region(cells=c2)              #选择部件P2的所有单元
p2.SectionAssignment(region=region2,sectionName='Section-Steel',offset=0.0,
                     offsetType=MIDDLE_SURFACE,offsetField='',thicknessAssignment=FROM_SECTION)  #


#定义装配环境
a = mdb.models['myModel'].rootAssembly
p11 = a.Instance(name='Part-1-1',part=p1,dependent=ON)   #创建一个新的实例对象，非独立实例
p12 = a.Instance(name='Part-1-2',part=p1,dependent=ON)   #创建一个新的实例对象，非独立实例
p21 = a.Instance(name='Part-2-1',part=p2,dependent=ON)   #创建一个新的实例对象，非独立实例
a.translate(instanceList=('Part-1-2', ), vector=(0.0, 15.0, 0.0))   #将名称为Part-1-2的实例对象沿着指定的矢量平移
a.translate(instanceList=('Part-2-1', ), vector=(0.0, -15.0, 0.0))  #将名称为Part-2-1的实例对象沿着指定的矢量平移

p11.translate(vector=(0.0, 15.0,0.0))                    #平移当前对象p11
p12.translate(vector=(0.0, -15.0,0.0))                    #平移当前对象p12


#创建分析步
mdb.models['myModel'].StaticStep(name='myStep1', previous='Initial',
                                 maxNumInc=1000, initialInc=0.1, minInc=1e-05, maxInc=0.3, nlgeom=ON) #定义静力分析步
FRes = mdb.models['myModel'].fieldOutputRequests
FRes[FRes.keys()[0]].setValues(numIntervals=10, variables=('S', 'U'))  #使用FRes.keys()[0]获取第一个fieldOutputRequests对象的名称               
                                                                       #利用函数setValues()修改fieldOutputRequests对象的属性值

#Region对象
#个人理解：Region对象是一个集合，包含了所有的单元、面、边、节点等，可以通过Region对象来选择这些对象

f12 = p12.faces
f11 = p11.faces
f21 = p21.faces
f1 = f12.getByBoundingBox(xMin=-1, xMax=1, yMin=-20, yMax=40, zMin=-1, zMax=25)
f2 = f11.getByBoundingBox(xMin=-1, xMax=1, yMin=-40, yMax=20, zMin=-1, zMax=25)
f3 = f21.getByBoundingBox(xMin=-1, xMax=1, yMin=-40, yMax=40, zMin=-1, zMax=25)
setX = a.Set(faces=f1+f2+f3, name='Set-X')
regionX = regionToolset.Region(faces=setX.faces)
surfaceX = a.Surface(name='surfaceX', side1Faces=f1+f2+f3)


#创建接触和相互作用关系
mdb.models['myModel'].ContactProperty('IntProp-1')                                                    #创建一个新的接触属性对象
mdb.models['myModel'].interactionProperties['IntProp-1'].TangentialBehavior(formulation=FRICTIONLESS) #设置“切向属性”
mdb.models['myModel'].ContactStd(name='Int-1', createStepName='Initial')                              #创建通用接触对象，从Initial步开始
mdb.models['myModel'].interactions['Int-1'].includedPairs.setValuesInStep(stepName='Initial', useAllstar=ON)  #设置接触对
mdb.models['myModel'].interactions['Int-1'].contactPropertyAssignments.appendInStep(                     #将接触属性分配给接触对象
    assignments=((GLOBAL, SELF, 'IntProp-1'), ), stepName='Initial')


#网格划分
elemType1 = mesh.ElemType(elemCode=C3D8R, elemLibrary=Standard,
                          kinematticSplit=AVERAGE_STRAIN, secondOrderAccuracy=OFF, 
                          hourglassControl=DEFAULT, distortionControl=DEFAULT)              #定义单元类型为一阶缩减积分单元C3D8R
p1.seedPat(size=1.5, deviationFactor=0.1)                                                   #为对象P1布置大小为1.5的全局种子
c1 = p1.cells                                                                               #C1包含P1的所有体元素
p1.setElementType(regions=(c1, ), elemTypes=(elemType1, ))                                  #将单元类型elemType1分配给对象P1的所有单元
p1.generateMesh()                                                                           #生成网格
p2.seedPart(size=1.5, deviationFactor=0.1)                                                  #为对象P2布置大小为1.5的全局种子
c2 = p2.cells                                                                               #C2包含P2的所有体元素
p2.setMeshControls(regions=c2, technique=SWEEP, algorithm=ADVANCING_FRONT)                  #
p2.generateMesh()                                                                           #生成网格
a.rergenerate()                                                                             #重新生成装配体的网格

p2.verifyMeshQuality(criterion=ASPECT_RATIO)


#施加边界和载荷
f12 = p12.faces
f11 = p11.faces
f21 = p21.faces
f1x = f12.getByBoundingBox(xMin=-1, xMax=1, yMin=-20, yMax=40, zMin=-1, zMax=25)
f2x = f11.getByBoundingBox(xMin=-1, xMax=1, yMin=-20, yMax=40, zMin=-1, zMax=25)
f3x = f21.getByBoundingBox(xMin=-1, xMax=1, yMin=-20, yMax=40, zMin=-1, zMax=25)
regionX = regionToolset.Region(faces=f1x+f2x+f3x)

f1z = f12.getByBoundingBox(xMin=-1, xMax=1, yMin=-20, yMax=40, zMin=-1, zMax=25)
f2z = f11.getByBoundingBox(xMin=-1, xMax=1, yMin=-20, yMax=40, zMin=-1, zMax=25)
f3z = f21.getByBoundingBox(xMin=-1, xMax=1, yMin=-20, yMax=40, zMin=-1, zMax=25)
regionZ = regionToolset.Region(faces=f1z+f2z+f3z)

f4 = f12.getByBoundingBox(xMin=-1, xMax=25, yMin=-20, yMax=-10, zMin=-1, zMax=25)
regionY = regionToolset.Region(faces=f4)
f5 = f12.getByBoundingBox(xMin=-1, xMax=25, yMin=25, yMax=40, zMin=-1, zMax=25)
regionYP = regionToolset.Region(faces=f5)

#以上几行语句都是为边界条件选择加权区域

mdb.models['myModel'].XsymmBC(name='BC-X', createStepName='Initial', region=regionX) #为名为myModel的模型对象在区域regionX上创建YZ对称边界
mdb.models['myModel'].ZsymmBC(name='BC-Z', createStepName='Initial', region=regionZ)


#为名为myModel的模型对象在区域regionY上创建固定边界
mdb.models['myModel'].DisplacementBC(name='BC-YFix', createStepName='Initial', region=regionY, 
                                     u1=UNSET, u2=SET, u3=SET, ur1=UNSET, ur2=UNSET, ur3=UNSET,
                                     amplitude=UNSET, distributionType=UNIFORM, fieldName='', localCsys=None)

#为名为myModel的模型对象在区域regionYP上创建面压力载荷对象
mdb.models['myModel'].Pressure(name='Pressure', createStepName='myStep1', region=regionYP,
                               distributionType=UNIFORM, field='', magnitude=10.0, amplitude=UNSET) 


#Job命令
mdb.Job(name='Job-1', model='myModel', description='', type=ANALYSIS, atTime=None, waitMinutes=0, waitHours=0, queue=None, memory=50,
        memoryUnits=PERCENTAGE, getMemoryFromAnalysis=True, explicitPrecision=SINGLE, nodalOutputPrecision=SINGLE, echoPrint=OFF,
        modelPrint=OFF, contactPrint=OFF, historyPrint=OFF, userSubroutine='', scratch='', multiprocessingMode=DEFAULT, numCpus=1)
mdb.jobs['Job-1'].submit()