import time
from screenUpdater import buffer
import optionHandler
import gameObjects.entity as Entity
import gameObjects.items as Item
import os

"""
Initialize the default view that will be opened when launching the app.
"""

player = Entity.Character("", "Elf", "Farmer", "Vindurvik")
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
print(player.getInfo())
dagger = Item.Weapon("IronDagger")
player.addToInv(dagger)
player.equipItem(dagger)
print(player.getInfo())


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
        gameLogic.checkInput()
        if elapsedSecondTime >= 1:
            gameLogic.secondPassed()
            secondStartTime = None
        if elapsedFrameTime >= (1 / gameLogic.getFPS()):
            gui.updateFrame()
            frameStartTime = None
    os.system("clear")
