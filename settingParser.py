class SettingParser:
    def __init__(self):
        pass

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
                line = line.split("#")[0]
                if len(line) == 0:
                    continue

                line = (
                    line if "name" in line or "desc" in line else line.replace(
                        " ", "")
                )

                if ":" in line:
                    currentItem = str(line.replace(":", ""))
                    itemList[currentItem] = {}
                elif "=" in line:
                    if ";" in line:
                        line = line.replace(";", "")
                        end = True
                    else:
                        end = False
                    splitted = line.split("=")
                    itemList[currentItem][splitted[0]] = splitted[1].lstrip()
                    if end:
                        currentItem = None
                elif ";" in line:
                    currentItem = None

        return itemList

    def getItems(self, id, fileName):
        file = self.parseFile(fileName)
        if str(id) in file:
            return file[id]
        elif str(id) in [None, "", "all", "-1"]:
            return file
        else:
            return None
