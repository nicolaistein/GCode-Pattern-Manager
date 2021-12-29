from tkinter import *
import gui.canvas.translator as translator
from patterns.gcode_cmd import GCodeCmd
from gui.pattern_model import PatternModel

M = 4  
W = 900
H = 900
xmin = 0
xmax = 900
ymin = 0
ymax = 900    

def P(x,y):
    """
    Transform point from cartesian (x,y) to Canvas (X,Y)
    """
    X = M + (x/xmax) * (W-2*M)
    Y = M + (1-(y/ymax)) * (H-2*M)
    return (X,Y)

class CanvasManager:

    plotFaces:bool = False
    plotDistortion:str = "none"

    def __init__(self, master: Frame, initSize: int):
        self.master = master
        self.size = initSize
        self.points = []
        self.faces = []
        self.patterns = {}
        self.flatObjectOnCanvas = []
        self.distortionOnCanvas = []
        self.selectedPattern = None

    def plot(self, points, faces, distortions):
        self.distortions = distortions
        self.faces = faces    
        pointsNew = translator.moveToPositiveArea(points)
        self.scale, self.points = translator.scale(pointsNew, self.size)
        self.plotDistortion = "none"
        self.plotFaces = False
        self.show()

    def selectPattern(self, pattern: PatternModel):
        selected = self.selectedPattern
        if selected is None or not selected == pattern:
            self.selectedPattern = pattern

            if not selected is None:
                self.refreshPattern(selected)
        else:
            self.selectedPattern = None
        self.refreshPattern(pattern)

    def createLine(self, x1, x2):
        self.flatObjectOnCanvas.append(
            self.canvas.create_line(x1[0], x1[1], x2[0], x2[1]))

    def onFaces(self):
        self.plotFaces = not self.plotFaces
        self.clear(True, False)
        self.showFlatObject()
        

    def onDistortionPress(self, distortion:str = "none"):
        if self.plotDistortion == distortion: 
            self.plotDistortion = "none"
        else:
            self.plotDistortion = distortion
        self.show()

    def show(self):
        self.clear(True, True)
        self.showDistortion()
        self.showFlatObject()
        
    def showDistortion(self):
        if self.plotDistortion == "area": self.showAreaDistortion()
        if self.plotDistortion == "angle": self.showAngleDistortion()
            
    def showFlatObject(self):
        if self.plotFaces:
            for face in self.faces:
                x = list(self.points[face[0]-1])
                y = list(self.points[face[1]-1])
                z = list(self.points[face[2]-1])

                #Border
                self.createLine(x, y)
                self.createLine(y, z)
                self.createLine(z, x)

        else:
            for point in self.points:
                x = point[0]
                y = point[1]
                r = 0
                self.flatObjectOnCanvas.append(self.canvas.create_oval(x - r, y - r, x + r, y + r))


    def showAreaDistortion(self):
        for index, face in enumerate(self.faces):
            x = list(self.points[face[0]-1])
            y = list(self.points[face[1]-1])
            z = list(self.points[face[2]-1])
            maxDistort = 1

            distFac = self.distortions[index]-maxDistort
            if distFac > maxDistort:
                distFac = maxDistort
            if distFac < 0:
                distFac = 0

            distFac = distFac/maxDistort
            distFac = 1-distFac

            colorFac = int(round(distFac * 255, 0))
            color = '#%02x%02x%02x' % (255, colorFac, colorFac)
            
            self.distortionOnCanvas.append(
            self.canvas.create_polygon(x, y, z, fill=color))

    def showAngleDistortion():
        pass

    def build(self):
        canvasFrame = Frame(self.master, height=self.size, width=self.size)
        self.canvas = Canvas(canvasFrame, height=self.size, width=self.size)
        canvasFrame.pack(side=LEFT, anchor=N)
        self.canvas.pack(side=LEFT)

    def clear(self, object:bool, distortion:bool):
        if distortion:
            for point in self.distortionOnCanvas:
                self.canvas.delete(point)
            self.distortionOnCanvas.clear()

        if object:
            for point in self.flatObjectOnCanvas:
                self.canvas.delete(point)
            self.flatObjectOnCanvas.clear()

    def deletePattern(self, pattern:PatternModel):
        self.removePatternFromCanvas(pattern)
        if self.selectedPattern == pattern:
            self.selectedPattern = None

    def removePatternFromCanvas(self, pattern:PatternModel):
        for shape in self.patterns[pattern]:
            self.canvas.delete(shape)
        self.patterns[pattern] = []


    def refreshPattern(self, pattern:PatternModel):
        self.removePatternFromCanvas(pattern)
        self.addPattern(pattern)

    def addPattern(self, pattern:PatternModel):
        result, commands = pattern.getGcode()
        color = "blue"
        #Change color to red if selected
        if not self.selectedPattern is None:
            color = "red" if self.selectedPattern == pattern else "blue"

        shapes = []
        for cmd in commands:
            s = []
            if(cmd.prefix == "G1"):
                s = self.canvas.create_line(cmd.previousX, 900-cmd.previousY, cmd.x, 900-cmd.y, fill=color, width=1)

            if(cmd.prefix == "G02"):
                s = self.computeArc(cmd, color)

            if(cmd.prefix == "G03"):
                s = self.computeArc(cmd, color)
            shapes.append(s)

        self.patterns[pattern] = shapes

    def computeArc(self, cmd:GCodeCmd, color:str):
        points = [P(cmd.previousX, cmd.previousY)]

        cornerPoints = self.getCornerPoints(cmd.prefix=="G02", cmd.arcDegrees, cmd.previousX, cmd.previousY, cmd.x, cmd.y)
        points.append(cornerPoints)

        points.append(P(cmd.x, cmd.y))
        return self.canvas.create_line(points, smooth=True, fill=color, width=1)
        

    def getCornerPoints(self, clockwise:bool, degrees:float, x:float, y:float, x2:float, y2:float):
        #Compute orthogonal vector to v2-v vector
        xOrtho = halfY = (y2 - y) / 2
        yOrtho = halfX = (x2 - x) / 2

        if clockwise: xOrtho *= -1
        else: yOrtho *= -1

        if degrees == 180:
            return [P(x + xOrtho, y + yOrtho), P(x2 + xOrtho, y2 + yOrtho)]
        if degrees == 90:
            return [P(x + + halfX + xOrtho, y + halfY + yOrtho)]

