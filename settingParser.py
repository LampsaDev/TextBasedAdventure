class settingParser:
    def __init__(self, fileName):
        self.parsedFile = self.parseFile(file)

    def openFile(self, fileName):
        try:
            file = open(fileName)
            return file
        except FileExistsError:
            print(f"File: {fileName} not found")

    def parseFile(self, fileName):
        with open(fileName, "r") as file:
            itemList = {}
            currentItem = None
            for currentLine in file:
                line = currentLine.replace("\n", "")

                line = (
                    line
                    if "d" in line or "desc" in line or "description" in line
                    else line.replace(" ", "")
                )
                if "#" in line:
                    continue
                elif ":" in line:
                    currentItem = str(line.replace(":", ""))
                    itemList[currentItem] = {}
                elif "=" in line:
                    if ";" in line:
                        line = line.replace(";", "")
                        end = True
                    else:
                        end = False
                    splitted = line.split("=")
                    itemList[currentItem][splitted[0]] = splitted[1]
                    if end:
                        currentItem = None
                elif ";" in line:
                    currentItem = None

        return itemList

    def getItems(self, id):
        if str(id) in self.parsedFile:
            return self.parsedFile[id]
        elif str(id) in [None, "", "all", "-1"]:
            return self.parsedFile
        else:
            return None


file = "setting/races.md"
parser = settingParser(file)
item1 = parser.getItems("Seppo")
item2 = parser.getItems("Ismo")
print(item1)
print(item2)
print(parser.getItems("all"))
