from pysofaconventions import *
from scipy.spatial import Delaunay
import numpy as np

def setupHRTF(selectedhrtf):
    folderPath = 'hrtf/'
    fileNames = {"1":'HRIR_L2354',"2":'HRIR_L2702', "3": 'ARI_NH2',"4":'ARI_NH104' }
    
    print(fileNames[selectedhrtf])
    sofaFiles = [SOFAFile(folderPath+fileNames[selectedhrtf]+'.sofa','r')]
    sourcePositions = np.concatenate([sofaFile.getVariableValue('SourcePosition')
        for sofaFile in sofaFiles])

    sourcePositions[:,:2] *= np.pi/180
    cullAmount = 3
    meanFreePath = 4*max(sourcePositions[:,2])/np.sqrt(len(sourcePositions)/cullAmount)
    sourcePositions[len(sourcePositions)//2:,2] += meanFreePath

    maxR = max(sourcePositions[:,2])-meanFreePath/2

    FIRs = np.concatenate([sofaFile.getDataIR()
        for sofaFile in sofaFiles])

    az = np.array(sourcePositions[:,0])
    el = np.array(sourcePositions[:,1])
    r = np.array(sourcePositions[:,2]) 

    xs = np.sin(az)*np.cos(el)*r
    ys = np.cos(az)*np.cos(el)*r
    zs = np.sin(el)*r

    points = np.array([xs, ys, zs]).transpose()    
    sourcePositions = sourcePositions[::cullAmount]
    FIRs = FIRs[::cullAmount]
    points = points[::cullAmount]
    tri = Delaunay(points, qhull_options="QJ Pp")
    tetraCoords = points[tri.simplices]

    T = np.transpose(np.array((tetraCoords[:,0]-tetraCoords[:,3],
                tetraCoords[:,1]-tetraCoords[:,3],
                tetraCoords[:,2]-tetraCoords[:,3])), (1,0,2))

    def fast_inverse(A):
        identity = np.identity(A.shape[2], dtype=A.dtype)
        Ainv = np.zeros_like(A)
        planarCount=0
        for i in range(A.shape[0]):
            try:
                Ainv[i] = np.linalg.solve(A[i], identity)
            except np.linalg.LinAlgError:
                planarCount += 1
        return Ainv

    Tinv = fast_inverse(T)
    return(tetraCoords, Tinv, tri, FIRs, maxR)


