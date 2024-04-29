from setupHRTF import setupHRTF

# Class to store variables related to spatial audio
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
        
# Class to manage speaker variables and audio streams
class SpeakerVar:
    def __init__(self):
        self.speaker_var = {}
        self.streams = {}
        
speakerVar = SpeakerVar()