from odbAccess import *
import numpy as np
from abaqus import *
from abaqusConstants import *
import __main__
import random

'''
x = 500.0
h = 30.0
d = 6.0
w = 400.0
R = (x*x - h*h)/(2*h)
'''

out_node_label = random.sample(range(1, 15000), 1000)
out_node_label = tuple(out_node_label)
coordinate = []
for numodb in range(0, 50):
    odb = openOdb(path='E:/FEM/Abaqus/2023-12-6/Job-' + str(numodb) + '.odb')
    instance = odb.rootAssembly.instances
    try:
        #删除节点集合
        del instance['SIDING-1'].nodeSets['out_node']
        out_node = instance['SIDING-1'].NodeSetFromNodeLabels(name='out_node', nodeLabels=out_node_label)
    except:
        print('out_node has been created!')
    for i in out_node_label:
        if numodb == 0:
            coordinate.append(instance['SIDING-1'].nodes[i].coordinates)

    # setoninstance = instance['SIDING-1'].NodeSet(name='setoninstance', nodes=out_node)

    step1 = odb.steps['Step-1']
    lastFrame = step1.frames[-1]

    coord = lastFrame.fieldOutputs['U'].getSubset(region=instance['SIDING-1'].nodeSets['out_node']).bulkDataBlocks[0]
    # displace = lastFrame.fieldOutputs['U'].getSubset(region=setoninstance).bulkDataBlocks[0]

    fieldValues = coord.data
    # dis = displace.data

    if numodb == 0:
        np.savetxt('E:/FEM/Abaqus/output/coordinate.txt', coordinate)

    with open('E:/FEM/Abaqus/output/Uoutput-' + str(numodb) + '.txt', 'w') as fp1:
        for v in fieldValues:
            fp1.write(str(v[0]) + ' , ' + str(v[1]) + ' , ' + str(v[2]) + '\n')
    odb.close()
