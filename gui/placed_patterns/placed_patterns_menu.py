from tkinter import *
from tkinter import messagebox
from tkinter.filedialog import askdirectory
from gui.button import TkinterCustomButton
from gui.canvas.canvas_manager import CanvasManager
from gui.pattern_model import PatternModel
from gui.pattern_input.pattern_input_window import PatternInputWindow
from gui.placed_patterns.placed_patterns_item import PlacedPatternsItem
from gui.listview import ListView
from gui.numeric_text import NumericText
from logger import log
import os


class PlacedPatternsMenu:

    def __init__(self, master: Frame, canvasManager:CanvasManager, mainColor: str):
        self.mainFrame = Frame(master, bg=mainColor)
        self.canvasManager = canvasManager
        canvasManager.placedPatternsMenu = self
        self.placedPatternItems = {}

    def deleteAll(self):
        for p in self.placedPatternItems.values():
            p.delete()
        self.placedPatternItems.clear()
        self.build()

    def delete(self, placedPatternItem):
        self.canvasManager.patternPlotter.deletePattern(placedPatternItem.pattern)

    def onCheckBoundaries(self):
        log("Checking boundaries")
        for p in self.placedPatternItems.values():
            p.checkBoundaries()

    def onPlacedPatternItemClick(self, pattern):
        self.canvasManager.patternPlotter.selectPattern(pattern)

    def onEditFinished(self, pattern:PatternModel):
        self.canvasManager.patternPlotter.refreshPattern(pattern)
        self.placedPatternItems[pattern].refreshValues()
        self.placedPatternItems[pattern].checkBoundaries()
#        self.build()

    def edit(self, patternItem:PlacedPatternsItem):
        PatternInputWindow(self.mainFrame, patternItem.pattern, patternItem.onEdit,
                           self.onEditFinished, self.canvasManager, True).openWindow()

    def addPattern(self, pattern: PatternModel):
        self.canvasManager.patternPlotter.addPattern(pattern)
        pat = PlacedPatternsItem(self.innerContent, pattern, self, self.canvasManager)
        self.placedPatternItems[pattern] = pat
        pat.build()
        pat.checkBoundaries()

    def generateGCode(self):
        if len(self.placedPatternItems) == 0: return
        filename = askdirectory()
        log("direcory: " + str(filename))
        if not os.path.isdir(filename): return
        file = open(filename + "/result.gcode", "w")
        workHeight = self.workHeightText.getNumberInput()
        freeMoveHeight = self.freeMoveHeightText.getNumberInput()
        eFactor = self.eFactorText.getNumberInput()
        fFactor = self.fFactorText.getNumberInput()

        file.write("G90\n")
        file.write("G0 Z" + str(freeMoveHeight) + " F" + str(fFactor) + "\n\n")
        for pattern in self.placedPatternItems.keys():
            result, commands = pattern.getGcode(workHeight,freeMoveHeight, eFactor, fFactor)
            file.write(result)
            file.write("\n")
        file.close()
        
        length = len(self.placedPatternItems)
        text = "pattern" if length == 1 else "patterns"
        messagebox.showinfo("Export", "Successfully exported "
         + str(length) + " " + text + " to " + file.name)

    def getKeyValueFrame(self, parent: Frame, key: str, value:str, padx:bool=False):
        keyValFrame = Frame(parent)
        keyLabel = Label(keyValFrame, text=key, width=12,
                            anchor=W, justify=LEFT)
        keyLabel.pack(side=LEFT)
        valText = NumericText(keyValFrame, width=4, initialText=value, floatingPoint=True)
        valText.build().pack(side=LEFT, padx=(2,0))

        keyValFrame.pack(side=LEFT, pady=(5,0), padx=(30 if padx else 0, 0))
        return valText

    def build(self):
        for widget in self.mainFrame.winfo_children():
            widget.destroy()

        self.content = Frame(self.mainFrame)

        title = Label(self.content, text="Placed Patterns")
        title.configure(font=("Helvetica", 12, "bold"))
        title.pack(fill='both', side=TOP, pady=(20,15))

        self.innerContent = ListView(self.content, 310, 670).build()

        self.placedPatternItems.clear()
        self.content.pack(side=TOP, anchor=N)

        generationFrame = Frame(self.mainFrame, width=323, height=170, pady=20)
        generationFrame.pack_propagate(0)
        inputParentFrame = Frame(generationFrame)
        InputFrame1 = Frame(inputParentFrame)
        self.workHeightText = self.getKeyValueFrame(InputFrame1, "Print height", "2.3")
        self.freeMoveHeightText = self.getKeyValueFrame(InputFrame1, "Move height", "10", padx=True)
        InputFrame1.pack(side=TOP, anchor=W)
        
        InputFrame2 = Frame(inputParentFrame)
        self.eFactorText = self.getKeyValueFrame(InputFrame2, "E Factor", "4")
        self.fFactorText = self.getKeyValueFrame(InputFrame2, "F Value", "250", padx=True)
        InputFrame2.pack(side=TOP, anchor=W, pady=(5,0))
        
        InputFrame2 = Frame(inputParentFrame)
        self.overrunBefore = self.getKeyValueFrame(InputFrame2, "Overrun Before", "2")
        self.overrunAfter = self.getKeyValueFrame(InputFrame2, "Overrun After", "1", padx=True)
        InputFrame2.pack(side=TOP, anchor=W, pady=(5,0))
        inputParentFrame.pack(side=TOP, padx=(20,20))

        TkinterCustomButton(master=generationFrame, text="Generate GCode", command=self.generateGCode,
                            corner_radius=60, height=25, width=160).pack(side=TOP, pady=(15, 0))
#        TkinterCustomButton(master=generationFrame, text="Check Boundaries", command=self.onCheckBoundaries,
#                            corner_radius=60, height=25, width=160).pack(side=TOP, pady=(10, 0))

        generationFrame.pack(side=TOP)
        self.mainFrame.pack(side=LEFT, padx=(20, 0), anchor=N)
