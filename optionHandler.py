import time

"""
Classes for converting inputs to actions
"""


class Generic:
    def __init__(self, gui):
        self.options = {
            "w": self.moveUp,
            "s": self.moveDown,
            " ": self.select,
            "y": self.yes,
            "n": self.no,
        }
        self.gameStatus = True
        self.selection = 0
        self.gui = gui
        self.currentView = MainMenu(self)
        self.fps = 60

    def getGameStatus(self):
        return self.gameStatus

    def getFPS(self):
        return self.fps

    def forceQuit(self):
        print("quit")
        self.gameStatus = False

    def checkInput(self, input):
        if input.isnumeric():
            self.numberInput(input)
            return
        if input in self.options:
            self.options[input]()

    def setView(self, viewClass):
        self.currentView = viewClass
        question = self.currentView.getGuiFormat()
        self.gui.setQuestion(question)

    def moveUp(self):
        if self.selection > 0:
            self.selection -= 1
            self.gui.setSelection(self.selection)

    def moveDown(self):
        if self.selection < len(self.currentView.options) - 1:
            self.selection += 1
            self.gui.setSelection(self.selection)

    def select(self):
        optionKey = str(self.selection + 1)
        self.doAction(optionKey)

    def yes(self):
        self.doAction("y")

    def no(self):
        self.doAction("n")

    def numberInput(self, number):
        self.doAction(number)

    def doAction(self, key):
        if str(key) in self.currentView.options:
            action = self.currentView.options[key][1]
            action()
        elif str(key) in self.currentView.hiddenOptions:
            action = self.currentView.hiddenOptions[key]
            action()


class ViewBuilder:
    def __init__(self, parent):
        self.parent = parent
        self.title = "Title"
        self.options = {}
        self.options = {}
        self.gui = parent.gui

    def getGuiFormat(self):
        options = []
        for key, value in self.options.items():
            options.append(f"{key}: {value[0]}")
        return [self.title, options]


class ConfirmView(ViewBuilder):
    def __init__(self, parent, previousView, action):
        super().__init__(parent)
        self.action = action
        self.previousView = previousView
        self.title = "Are you sure you want to quit?"
        self.options = {
            "y": ["Confirm", self.confirm],
            "n": ["Cancel", self.goBack],
        }
        self.hiddenOptions = {"1": self.confirm, "2": self.goBack}

    def goBack(self):
        newView = self.previousView
        self.parent.selection = 0
        self.parent.setView(newView)

    def confirm(self):
        self.action()


class MainMenu(ViewBuilder):
    def __init__(self, parent):
        super().__init__(parent)
        self.title = "Main Menu"
        self.options = {
            "1": ["New Game", self.newGame],
            "2": ["Load Save", self.loadGame],
            "3": ["Exit", self.quitGame],
        }

    def checkInput(self, input):
        if input in self.options:
            self.options[input][1]()

    def newGame(self):
        pass

    def loadGame(self):
        pass

    def quitGame(self):
        newView = ConfirmView(self.parent, self, self.parent.forceQuit)
        self.parent.selection = -1
        self.parent.setView(newView)
