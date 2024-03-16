import time
from screenUpdater import buffer
import inputManager as input
import optionHandler
from settingParser import SettingParser
import os

"""
Initialize the default view that will be opened when launching the app.
"""
races = SettingParser("setting/races.md").getItems("all")
gui = buffer(64, 24)
gui.setScene("Main Menu")
gui.setStats("")
gui.setTimerLength(10)
gameLogic = optionHandler.Generic(gui)
welcomePage = ["jee", "juu"]
question = gameLogic.currentView.getGuiFormat()
gui.setContent(welcomePage)
gui.setQuestion(question)
gui.updateFrame()
gui.setTimerLength(0)
input = input.inputManager()
print(races)


if True:
    frameStartTime = None
    secondStartTime = None
    while gameLogic.getGameStatus():
        if frameStartTime is None:
            frameStartTime = time.time()
        if secondStartTime is None:
            secondStartTime = time.time()

        elapsedFrameTime = time.time() - frameStartTime
        elapsedSecondTime = time.time() - secondStartTime
        gameLogic.checkInput(input.getChar())
        if elapsedSecondTime >= 1:
            gameLogic.secondPassed()
            secondStartTime = None
        if elapsedFrameTime >= (1 / gameLogic.getFPS()):
            gui.updateFrame()
            frameStartTime = None

os.system("clear")
