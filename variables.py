from setupHRTF import setupHRTF

class Variables:
    def __init__(self,distance,selectedhrtf):
        self.tetraCoords, self.Tinv, self.tri, self.FIRs, self.maxR = setupHRTF(selectedhrtf)
        self.azimuth = 0
        self.elevation = 0
        self.dist = 3
        self.paz = self.azimuth
        self.pel = self.elevation
        self.pr = self.dist
        self.distance = distance
class SpeakerVar:
    def __init__(self):
        self.speaker_var = {}
        self.streams = {}
        
speakerVar = SpeakerVar()