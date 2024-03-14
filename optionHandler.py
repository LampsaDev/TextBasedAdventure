"""
Classes for converting inputs to actions
"""


class Generic:
    def __init__(self, gui):
        self.options = {"w": self.moveUp, "s": self.moveDown, " ": self.select}
        self.gameStatus = True
        self.selection = 0
        self.gui = gui
        self.currentView = MainMenu(self)
        self.fps = 24

    def getGameStatus(self):
        return self.gameStatus

    def getFPS(self):
        return self.fps

    def forceQuit(self):
        self.gui.setContent()
        self.gameStatus = False

    def checkInput(self, input):
        if input in self.options:
            self.options[input]()

    def setView(self, viewClass):
        self.currentView = viewClass

    def moveUp(self):
        if self.selection > 0:
            self.selection -= 1
            self.gui.setSelection(self.selection)

    def moveDown(self):
        if self.selection < len(self.options) - 1:
            self.selection += 1
            self.gui.setSelection(self.selection)

    def select(self):
        optionKey = str(self.selection)
        if optionKey in self.currentView.options:
            action = self.currentView.options[optionKey][1]
            action()


class ViewBuilder:
    def __init__(self, parent):
        self.parent = parent
        self.title = "Title"
        self.options = {}
        self.gui = parent.gui

    def getGuiFormat(self):
        options = []
        for key, value in self.options.items():
            options.append(value[0])
        return [self.title, options]


class MainMenu(ViewBuilder):
    def __init__(self, parent):
        super().__init__(parent)
        self.title = "Main Menu"
        self.options = {
            "0": ["New Game", self.newGame],
            "1": ["Load Save", self.loadGame],
            "2": ["Exit", self.quitGame],
        }

    def checkInput(self, input):
        if input in self.options:
            self.options[input][1]()

    def newGame(self):
        pass

    def loadGame(self):
        pass

    def quitGame(self):
        confirm = ConfirmClass(self)
        self.gui.setQuestion(confirm.getGuiFormat())
        self.gui.setSelection(0)
        self.options = confirm.options
        # self.parent.forceQuit()


class ConfirmClass(ViewBuilder):
    def __init__(self, parent):
        super().__init__(parent)
        self.title = "Are you sure you want to quit?"
        self.options = {"0": ["Yes", self.confirm], "1": ["Cancel", self.cancel]}

    def confirm(self):
        pass

    def cancel(self):
        pass
