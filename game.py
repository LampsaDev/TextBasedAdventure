import time
import screenUpdater

welcomePage = "jee", "juu", ["Main Menu", ["New Game", "Load Save", "Quit"]]

gui = screenUpdater.screenUpdater(64, 24)
gui.setScene("Main Menu")
gui.setContent(welcomePage)
gui.setStats("")
gui.setTimerLength(0)
gui.updateFrame()


def timerFunction(timeInSeconds):
    time.sleep(timeInSeconds)
    return True


while True:
    update = timerFunction(1)
    if update:
        gui.updateFrame()
        update = False
