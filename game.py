import time
from screenUpdater import buffer
import inputManager as input
import optionHandler


gui = buffer(64, 24)
gui.setScene("Main Menu")
gui.setStats("")
gui.setTimerLength(5)

gameLogic = optionHandler.generic(gui)

welcomePage = ["jee", "juu"]
question = [gameLogic.currentView.getGuiFormat()]

gui.setContent(welcomePage)
gui.setQuestion(question)

input = input.inputManager()

gui.updateFrame()
print(question)
fps = 60
gameOn = True


def getInput():
    char = input.getChar()
    gameLogic.checkInput(char)


frameStartTime = None
secondStartTime = None
while gameOn:
    if frameStartTime is None:
        frameStartTime = time.time()
    if secondStartTime is None:
        secondStartTime = time.time()

    elapsedFrameTime = time.time() - frameStartTime
    elapsedSecondTime = time.time() - secondStartTime
    getInput()
    if elapsedSecondTime >= 1:
        gui.setTimerSeconds(2)
    if elapsedFrameTime >= (1 / fps):
        gui.updateFrame()
        frameStartTime = None
