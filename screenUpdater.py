"""
This class is used for updating whats shown on screen.
drawFrame() is run everytime when update is required.
Has methods for drawing different objects on screen.
"""

import os
import math


class buffer:
    def __init__(self, xSize, ySize):
        self.horizontalSize = xSize - 3
        self.verticalSize = ySize

    timerLengthInSeconds = 0
    currentTimeInSeconds = 0
    scene = None
    content = None
    question = None
    stats = None

    updateRequest = False

    selection = 0

    """
    Updates scene
    """

    def setScene(self, newScene):
        self.scene = newScene
        self.updateRequest = True

    def setContent(self, newContent):
        self.content = newContent
        self.updateRequest = True

    def setQuestion(self, newQuestion):
        self.question = newQuestion
        self.updateRequest = True

    def setStats(self, newStats):
        self.stats = newStats
        self.updateRequest = True

    def setTimerLength(self, newTimerLength):
        self.timerLengthInSeconds = newTimerLength
        self.setTimerSeconds(0)
        self.updateRequest = True

    def setTimerSeconds(self, newTime):
        self.currentTimeInSeconds = newTime
        self.updateRequest = True

    def setSelection(self, newSelection):
        self.selection = newSelection
        self.updateRequest = True

    """
    Updates the frame.
    Must be called everytime when change is wanted.
    """

    def updateFrame(self):
        if not self.updateRequest:
            return
        terminalHeight, terminalWidth = self.getTerminalSize()
        os.system("clear")

        self.horizontalSize = terminalWidth - 3
        self.verticalSize = terminalHeight - 2

        if terminalWidth < 64:
            self.drawTitleBar(
                "Terminal must be atleast 64 columns. Now: " + str(terminalWidth)
            )
            self.updateRequest = False
            return
        elif terminalHeight < 24:
            self.drawTitleBar(
                "Terminal must be atleast 24 rows. Now: " + str(terminalHeight)
            )
            self.updateRequest = False
            return

        sceneHeight = 0
        if self.scene == "Inventory":
            pass
        elif self.scene == "Map":
            pass
        elif self.scene == "Stats":
            pass
        elif self.scene == "Main Menu":
            titleHeight = self.drawTitleBar("Epic CLI Adventure")
            sceneHeight = self.drawOptions()
            sceneHeight += self.drawHelperText(
                "'W' = Up, 'S' = Down, 'Space' = Confirm", True, True
            )
        else:  # "story"-scene
            titleHeight = self.drawTitleBar(self.scene)
            sceneHeight += self.drawOptions()
            sceneHeight += self.drawStatBar()
            sceneHeight += self.drawHelperText("Press 'Space' to confirm", True, True)
        # Fill the empty lines
        for line in range(self.verticalSize - sceneHeight - titleHeight):
            self.drawLine("")
        self.updateRequest = False

    """
    Draws text container with current actions
    """

    def drawTextBox(self):
        if not self.content:
            return 0
        # Split text into smaller chuncks
        self.drawLineCentered(self.content[0])
        textArr = self.splitTextToArray(self.content[1])
        textHeight = 1
        for line in textArr:
            text = ""
            for word in line:
                text = text + word + " "
            textHeight += 1
            self.drawLine(text)
        return textHeight

    """
    Draws available actions, timer and help text
    """

    def drawOptions(self):
        if not self.question:
            return 0
        question = self.question[0]
        options = []
        for option in self.question[1]:
            options.append(option)
        self.drawHLine()
        lineAmount = 1
        lineAmount += self.drawLine("")
        lineAmount += self.drawLineCentered(question)
        lineAmount += self.drawLine("")
        longestWordWidth = self.longestStringLength(options)

        for index, option in enumerate(options):
            filler = ""
            for i in range(longestWordWidth - len(option)):
                filler += " "
            if self.selection == index:
                lineAmount += self.drawLineCentered("> " + option + " <" + filler)
            else:
                lineAmount += self.drawLineCentered("  " + option + "  " + filler)
        lineAmount += self.drawLine("")
        lineAmount += self.drawTimer()
        lineAmount += 1
        self.drawHLine()

        return lineAmount

    def drawHelperText(self, helperText, drawDecorators, isFlipped):
        if drawDecorators:
            text = self.drawDecorators(helperText, isFlipped)
        else:
            text = helperText

        lineAmount = self.drawLineCentered(text)
        return lineAmount

    """
    Draws timer that updates the screen after few seconds
    """

    def drawTimer(self):
        timerLength = self.timerLengthInSeconds
        time = self.currentTimeInSeconds
        if timerLength == 0:
            timer = "\u221e"
        else:
            timer = ""
            for index, second in enumerate(range(timerLength)):
                if index == time:
                    timer += "¤"
                else:
                    timer += "~"
        return self.drawLineCentered(timer)

    def drawDecorators(self, text, flip):
        if not text:
            return 0
        if flip:
            beg = "\u203e" + "\\/\\/ "
            end = " \\/\\/" + "\u203e"
        else:
            beg = "_/\\/\\ "
            end = " /\\/\\_"

        return beg + text + end

    """
    Find longest string in array and return its length
    """

    def longestStringLength(self, words):
        longest = 0
        for word in words:
            if len(word) > longest:
                longest = len(word)
        return longest

    """
    Draws a title box
    """

    def drawTitleBar(self, title):
        self.drawHLine()
        chars = self.drawDecorators(title, False)
        titleHeight = self.drawLineCentered(chars) + 1
        self.drawHLine()
        return titleHeight + 1

    """
    Draws stats bar at bottom
    """

    def drawStatBar(self):
        self.drawHLine()
        height = 2
        height += self.drawLine(self.stats)
        self.drawHLine()
        return height

    """
    Draws one text line
    :return amount of lines taken by the text
    """

    def drawLine(self, chars):
        if chars is None:
            return 0
        line = "| "
        splitLine = False
        filler = self.horizontalSize - len(chars)
        height = 1

        if filler < 0:
            leftOvers = chars[self.horizontalSize :]
            chars = chars[: self.horizontalSize]
            splitLine = True

        for char in chars:
            line += char

        for blank in range(filler):
            line += " "

        line += "|"
        print(line)

        if splitLine:
            height += self.drawLine(leftOvers)

        return height

    """
    Draws line with centered text.
    :return amount of lines taken by the text
    """

    def drawLineCentered(self, chars):
        line = "| "
        chars = str(chars)
        filler = self.horizontalSize - len(chars)
        height = 1
        if filler < 0:
            leftOvers = chars[self.horizontalSize :]
            chars = chars[: self.horizontalSize]
            self.drawLine(chars)
            height += self.drawLineCentered(leftOvers)
            return height
        elif filler % 2 == 0:
            leftFill = int(filler / 2)
            rightFill = int(filler / 2)
        else:
            leftFill = int(math.floor(filler / 2))
            rightFill = int(math.ceil(filler / 2))

        for blank in range(leftFill):
            line += " "

        for char in chars:
            line += char

        for blank in range(rightFill):
            line += " "

        line += "|"
        print(line)
        return height

    """
    Text splitter that split the text so it fits on the screen
    """

    def splitTextToArray(self, text):
        words = text.split(" ")
        lines = []
        currentLine = 0
        currentLineLength = 0
        lines.append([])
        for word in words:
            currentLineLength += len(word) + 1
            if currentLineLength > self.horizontalSize:
                currentLineLength = len(word) + 1
                lines.append([])
                currentLine += 1
            lines[currentLine].append(word)
        return lines

    """
    Draws horizontal divider line.
    """

    def drawHLine(self):
        # Draw horizontal line across the "screen"
        line = "+-"
        for x in range(self.horizontalSize):
            line += "-"
        line += "+"
        print(line)

    """
    :return size of the terminal
    """

    def getTerminalSize(self):
        rows, columns = os.popen("stty size", "r").read().split()
        return int(rows), int(columns)


# Todo changing the screen size should update the screen
