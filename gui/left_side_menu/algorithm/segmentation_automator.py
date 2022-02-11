import os
from gui.canvas.plotting_options.plotting_option import PlottingOption
import gui.left_side_menu.algorithm.automator as automator
from logger import log

class SegmentationAutomator(automator.Automator):

    def __init__(self, parentFolder:str, chartId:int):
        self.chartId = chartId
        name = parentFolder + "/" + str(chartId)
        super().__init__(os.getcwd() + "/" + name + ".obj", name)

    def calculate(self):
        self.read()
        pointsBefore, facesBefore, pointsAfter, facesAfter = self.flatten()
        self.calcDistortions(pointsBefore, facesBefore, pointsAfter, facesAfter)

        log("chart " + self.folderPath + " angularDist: " + str(self.angularDist))
        log("chart " + self.folderPath + " isometricDist: " + str(self.isometricDist))
        log("chart " + self.folderPath + " max angular dist: " + str(self.maxAngularDist))
        log("chart " + self.folderPath + " max isometric dist: " + str(self.maxIsometricDist))
        #Todo: check overlapping
        if self.shouldSegment():
            faceToChart, data = self.segmentAndProcess()
            return faceToChart, data
        else: 
            return [1]*len(self.faces), [(1, pointsBefore, facesBefore, pointsAfter, facesAfter)]
