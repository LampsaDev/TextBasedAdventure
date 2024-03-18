from settingParser import SettingParser


class Item:
    def __init__(self, name):
        self.name = name
        self.stats = {
            "blunt": 0,
            "cut": 0,
            "pierce": 0,
            "weight": 0,
            "speed": 0,
            "plate": 0,
            "padding": 0,
            "posh": 0,
        }
        self.buffs = []

    def _initStat(self, item):
        for stat in self.stats:
            if self.stats[stat] == 0:
                self.stats[stat] = int(item[stat]) if stat in item else 1
            else:
                self.stats[stat] += int(item[stat]) if stat in item else 0


class Weapon(Item):
    def __init__(self, name):
        super().__init__(name)
        self.initStats()
        self.slot = "right"

    def initStats(self):
        parser = SettingParser()
        dir = "setting/"

        weapons = parser.getItems("all", dir + "weapons.md")
        if self.name in weapons:
            item = weapons[self.name]
        else:
            item = weapons["Default"]
        self._initStat(item)
