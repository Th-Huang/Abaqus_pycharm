from odbAccess import *
import numpy as np
from abaqus import *
from abaqusConstants import *
import __main__

x = 500.0
h = 30.0
d = 6.0
R = (x^2 - h^2)/(2*h)


odb = openOdb(path='E:/Abaqus/Job-0.odb')
instance = odb.rootAssembly.instances['SIDING-1']

step1 = odb.steps['Step-1']
lastFrame = step1.frames[-1]
coord = lastFrame.fieldOutputs['COORD'].getByBoundingCylinder(center=(0.0, h-R, 0), radius=R, height=400.0)

fieldValue = coord.values
print(len(fieldValue))

with open('./output.txt','w') as fp1:
    for v in fieldValue:
        fp1.write(str(v.nodelabel) + ' , ' + str(v.data[0]) + ' , ' + str(v.data[1]) + ' , ' + str(v.data[2]) + '\n')
        print('Node Label: ', v.nodelabel)
        print('X: ', v.data[0])
        print('Y: ', v.data[1])
        print('Z: ', v.data[2])
