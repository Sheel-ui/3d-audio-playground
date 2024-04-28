from setupHRTF import setupHRTF

class Variables:
    def __init__(self,distance,selectedhrtf):
        self.tetraCoordinates, self.tetrahedronInverse, self.delaunayTriangulation, self.hrtfData, self.maxR = setupHRTF(selectedhrtf)
        self.azimuth = 0
        self.elevation = 0
        self.dist = 3
        self.speakerAzimuth= self.azimuth
        self.speakerElevation = self.elevation
        self.speakerDistance = self.dist
        self.distance = distance
class SpeakerVar:
    def __init__(self):
        self.speaker_var = {}
        self.streams = {}
        
speakerVar = SpeakerVar()