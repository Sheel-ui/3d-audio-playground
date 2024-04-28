from pysofaconventions import *
from scipy.spatial import Delaunay
import numpy as np

def setupHRTF(selectedhrtf):
    folderPath = 'hrtf/'
    fileNames = {"1":'HRIR_L2354',"2":'HRIR_L2702', "3": 'ARI_NH2',"4":'ARI_NH104' }

    files = [SOFAFile(folderPath+fileNames[selectedhrtf]+'.sofa','r')]
    positionArrays = np.concatenate([sofaFile.getVariableValue('SourcePosition')
        for sofaFile in files])

    cullingFactor = 3
    positionArrays[:,:2] *= np.pi/180
    averageFreePath = 4*max(positionArrays[:,2])/np.sqrt(len(positionArrays)/cullingFactor)
    positionArrays[len(positionArrays)//2:,2] += averageFreePath

    maxR = max(positionArrays[:,2])-averageFreePath/2

    hrtfData = np.concatenate([sofaFile.getDataIR()
        for sofaFile in files])

    azimuth = np.array(positionArrays[:,0])
    elevation = np.array(positionArrays[:,1])
    dist = np.array(positionArrays[:,2]) 

    xCoordinate = np.sin(azimuth)*np.cos(elevation)*dist
    yCoordinate = np.cos(azimuth)*np.cos(elevation)*dist
    zCoordinate = np.sin(elevation)*dist

    points = np.array([xCoordinate, yCoordinate, zCoordinate]).transpose()   
    hrtfData = hrtfData[::cullingFactor] 
    points = points[::cullingFactor]
    positionArrays = positionArrays[::cullingFactor]
    delaunayTriangulation = Delaunay(points, qhull_options="QJ Pp")
    tetraCoordinates = points[delaunayTriangulation.simplices]

    transposeCoordinates = np.transpose(np.array((tetraCoordinates[:,0]-tetraCoordinates[:,3],
                tetraCoordinates[:,1]-tetraCoordinates[:,3],
                tetraCoordinates[:,2]-tetraCoordinates[:,3])), (1,0,2))

    def inverse(array):
        identity = np.identity(array.shape[2], dtype=array.dtype)
        arrayInverse = np.zeros_like(array)
        planarCount=0
        for i in range(array.shape[0]):
            try:
                arrayInverse[i] = np.linalg.solve(array[i], identity)
            except np.linalg.LinAlgError:
                planarCount += 1
        return arrayInverse

    tetrahedronInverse = inverse(transposeCoordinates)
    return(tetraCoordinates, tetrahedronInverse, delaunayTriangulation, hrtfData, maxR)


