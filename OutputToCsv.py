import os,os.path
import sys
from odbAccess import *
import numpy as np

o = openOdb(path='E:/Abaqus/Job-0.odb', readOnly=True)

assembly = o.rootAssembly
part = assembly.instances['SIDING-1']
print(len(part.nodes))
coordinates_bending = []
print()
for node in part.nodes:
    coordinates_bending.append(node.coordinates)
np.savetxt('E:/Abaqus/coordinates_bending.csv', coordinates_bending, delimiter=',')

step1 = o.steps['Step-1']
frame = step1.frames[-1]
displacement_last = frame.fieldOutputs['U']
displacementValues_last = displacement_last.values

DISP = []
for v in displacementValues_last:
    DISP.append(v.data)
np.savetxt('E:/Abaqus/DISP.csv', DISP, delimiter=',')

temp_coordinates = np.array(coordinates_bending)
temp_DISP = np.array(DISP)
coordinates_springback = temp_coordinates + temp_DISP
np.savetxt('E:/Abaqus/coordinates_springback.csv', coordinates_springback, delimiter=',')

o.close()