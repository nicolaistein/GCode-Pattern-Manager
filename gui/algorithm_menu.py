from ctypes import pointer, string_at
from tkinter import *
from tkinter.filedialog import askopenfilename
from gui.button import TkinterCustomButton
from algorithms.algorithms import *
from gui.plotting.canvas_manager import CanvasManager
from gui.file_menu import FileMenu


class AlgorithmMenu:

    points = []

    algorithms = [
        ("BFF", 1),
        ("LSCM", 2),
        ("ARAP", 3),
    ]

    def __init__(self, master: Frame, canvasManager: CanvasManager, fileMenu:FileMenu):
        self.mainFrame = Frame(
            master, width=220, height=250, padx=20, pady=20)
        self.canvasManager = canvasManager
        self.fileMenu = fileMenu
        self.v = IntVar()
        self.v.set(1)

    def calculate(self):
        file = self.fileMenu.path
        if not file:
            return

        if(self.v.get() == 1):
            coneCount = int(self.bffConeInput.get("1.0", END)[:-1])
            time, self.points = executeBFF(file, coneCount)
        if(self.v.get() == 2):
            time, self.points = executeLSCM(file)
        if(self.v.get() == 3):
            time, self.points = executeARAP(file)

        print("time: " + str(time) + ", points: " + str(len(self.points)))
        self.canvasManager.plot(self.points)


    def build(self):

        title = Label(self.mainFrame, text="Flatten Object")
        title.configure(font=("Helvetica", 12, "bold"))
        title.pack(fill='both', side=TOP, pady=(0, 20))

        self.mainFrame.pack_propagate(0)
        self.assembleAlgoChooserFrame()

        TkinterCustomButton(master=self.mainFrame, text="Calculate", command=self.calculate,
                            corner_radius=60, height=25, width=140).pack(side=TOP, pady=(20, 0))

        self.mainFrame.pack(side=TOP, pady=(20, 0))

    def ShowChoice(self):
        print(self.v.get())

    def cancelInput(self, event):
        return "break"

    def allowInput(self, event):
        pass

    def onKeyPress(self, event):
        if not event.char in "1234567890":
            return "break"

    def assembleAlgoChooserFrame(self):
        selectAlgoFrame = Frame(self.mainFrame)
        selectAlgoTitle = Label(selectAlgoFrame,
                                text="Choose Algorithm")

        selectAlgoTitle.configure(font=("Helvetica", 11, "bold"))
        selectAlgoTitle.pack(side=TOP, anchor=W)

        for txt, val in self.algorithms:
            optionFrame = Frame(selectAlgoFrame)
            Radiobutton(optionFrame,
                        text=txt,
                        height=1,
                        wrap=None,
                        variable=self.v,
                        command=self.ShowChoice,
                        value=val).pack(anchor=W, side=LEFT)

            if(txt == "BFF"):
                Label(optionFrame, text="with").pack(side=LEFT, anchor=W)
                self.bffConeInput = Text(optionFrame, height=1, width=3)
                self.bffConeInput.bind('<Return>', self.cancelInput)
                self.bffConeInput.bind('<Tab>', self.cancelInput)
                self.bffConeInput.bind('<BackSpace>', self.allowInput)
                self.bffConeInput.bind('<KeyPress>', self.onKeyPress)
                self.bffConeInput.insert(END, "10")
                self.bffConeInput.pack(side=LEFT, anchor=W, padx=10)
                Label(optionFrame, text="cones").pack(side=LEFT, anchor=W)
            optionFrame.pack(side=TOP, anchor=W)

        selectAlgoFrame.pack(side=TOP, anchor=W, pady=(10, 0))
