import inputManager as input
import gameObjects.entity as entity

"""
Classes for converting inputs to actions
"""


class Generic:
    def __init__(self, gui):
        self.options = {
            "w": self.moveUp,
            "s": self.moveDown,
            "a": self.moveLeft,
            "d": self.moveRight,
            " ": self.select,
            "y": self.yes,
            "n": self.no,
            "q": self.quit,
        }
        self.typing = False
        self.gameStatus = True
        self.selection = 0
        self.gui = gui
        self.currentView = MainMenu(self)
        self.fps = 60
        self.timerLength = self.currentView.timer
        self.timerSecond = 0
        self.input = input.inputManager()

    def secondPassed(self):
        if self.timerLength == 0:
            return
        if self.timerSecond < self.timerLength:
            print(self.timerSecond)
            self.timerSecond += 1
            self.gui.setTimerSeconds(self.timerSecond)
        else:
            self.timerFinished()
            self.timerLength = 0
            self.timerSecond = 0
            self.gui.setTimerLength(self.timerLength)

    def getGameStatus(self):
        return self.gameStatus

    def getFPS(self):
        return self.fps

    def forceQuit(self):
        print("quit")
        self.gameStatus = False

    def checkInput(self):
        input = self.input.getChar()
        if input.isnumeric():
            self.numberInput(input)
        elif input in self.options:
            self.options[input]()

    def checkInputText(self, length, title):
        return self.input.getText(length, title)

    def setView(self, viewClass):
        self.currentView = viewClass
        question = self.currentView.getGuiFormat()
        text = self.currentView.getTextFormat()
        self.gui.setQuestion(question)
        self.gui.setContent(text)
        self.timerSecond = 0
        self.selection = 0
        self.timerLength = self.currentView.timer
        self.gui.setTimerLength(self.timerLength)

    def moveUp(self):
        if self.selection > 0:
            self.selection -= 1
            self.gui.setSelection(self.selection)

    def moveDown(self):
        if self.selection < len(self.currentView.options) - 1:
            self.selection += 1
            self.gui.setSelection(self.selection)

    def moveLeft(self):
        pass

    def moveRight(self):
        pass

    def select(self):
        optionKey = str(self.selection + 1)
        self.doAction(optionKey)

    def yes(self):
        self.doAction("y")

    def no(self):
        self.doAction("n")

    def quit(self):
        self.doAction("q")

    def numberInput(self, number):
        self.doAction(number)

    def timerFinished(self):
        self.doAction("Timer")

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
        self.hiddenOptions = {}
        self.gui = parent.gui
        self.timer = 0
        self.previousView = None
        self.textField = ["", ""]

    def goBack(self):
        print(self.previousView)
        if self.previousView is None:
            return
        newView = self.previousView
        self.parent.setView(newView)
        self.parent.gui.setSelection(self.parent.selection)

    def checkInput(self, input):
        if input in self.options:
            self.options[input][1]()

    def getGuiFormat(self):
        options = []
        for key, value in self.options.items():
            options.append(f"{key}: {value[0]}")
        return [self.title, options]

    def getTextFormat(self):
        text = ["", ""]
        if self.textField[0] != "":
            text[0] = self.textField[0]
        if self.textField[1] != "":
            text[1] = self.textField[1]
        return text


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
        self.hiddenOptions = {"1": self.confirm,
                              "2": self.goBack, "Timer": self.goBack}
        self.timer = 15

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

    def newGame(self):
        newView = SetName(self.parent, self)
        self.parent.setView(newView)
        self.parent.selection = -1

    def loadGame(self):
        pass

    def quitGame(self):
        newView = ConfirmView(self.parent, self, self.parent.forceQuit)
        self.parent.setView(newView)
        self.parent.selection = -1


class SetName(ViewBuilder):
    def __init__(self, parent, previousView):
        super().__init__(parent)
        self.previousView = previousView
        self.title = "Choose your name."
        self.name = ""
        self.setName()
        self.options = {
            "y": [f"Select {self.name} as your name", self.confirm],
            "n": ["Cancel", self.goBack],
        }
        self.hiddenOptions = {}

    def confirm(self):
        player = entity.Character(self.name)

    def setName(self):
        self.name = self.parent.checkInputText(15, "Set firstname:")
