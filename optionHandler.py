"""
Classes for converting inputs to actions
"""


class generic:
    def __init__(self, gui):
        self.options = {"w": self.moveUp, "s": self.moveDown, " ": self.select}
        self.gameStatus = True
        self.selection = 0
        self.gui = gui
        self.currentView = mainMenu(self)
        self.fps = 30

    def getGameStatus(self):
        return self.gameStatus

    def getFPS(self):
        return self.fps

    def forceQuit(self):
        self.gameStatus = False

    def checkInput(self, input):
        if input in self.options:
            self.options[input]()

    def setView(self, viewClass):
        self.currentView = viewClass

    def moveUp(self):
        if self.selection > 0:
            self.selection -= 1
            self.gui.setSelection = self.selection

    def moveDown(self):
        if self.selection < len(self.options):
            self.selection += 1
            self.gui.setSelection = self.selection

    def select(self):
        self.currentView.options[str(self.selection)]


class mainMenu:
    def __init__(self, parent):
        self.parent = parent
        self.title = "Main Menu"
        self.options = {
            "0": ["New Game", self.newGame],
            "1": ["Load Save", self.loadGame],
            "2": ["Exit", self.quitGame],
        }

    def checkInput(self, input):
        if input in self.options:
            self.options[input][1]()

    def getGuiFormat(self):
        options = []
        for key, value in self.options.items():
            options.append(value[0])  # Append the option name to the list
        return [self.title, options]

    def newGame(self):
        pass

    def loadGame(self):
        pass

    def quitGame(self):
        self.parent.forceQuit()
