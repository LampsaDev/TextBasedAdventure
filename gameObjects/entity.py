from settingParser import SettingParser
import random


"""
Class for different npc and playable characters
"""


class Entity:
    def __init__(self, name):
        self.name = name
        self.stats = {
            "str": 0,
            "agi": 0,
            "int": 0,
            "vit": 0,
            "hp": 0,
            "fame": 0,
            "repu": 0,
        }
        self.invStats = {
            "blunt": 0,
            "cut": 0,
            "pierce": 0,
            "plate": 0,
            "padding": 0,
            "weight": 0,
            "posh": 0,
            "speed": 0,
            "invSize": 0,
        }
        self.invSize = 1
        self.inv = {
            "head": None,
            "torso": None,
            "legs": None,
            "feet": None,
            "hands": None,
            "bag": None,
            "amulet": None,
            "ring": None,
            "belt": None,
            "left": None,
            "right": None,
            "inv": [],
        }

    def _initStat(self, file):
        for stat in self.stats:
            if self.stats[stat] == 0:
                self.stats[stat] = int(file[stat]) if stat in file else 1
            else:
                self.stats[stat] += int(file[stat]) if stat in file else 0

    def getStats(self):
        return self.stats

    def addToInv(self, item):
        if len(self.inv["inv"]) < self.invSize:
            self.inv["inv"].append(item)
            return True
        return False

    def equipItem(self, item):
        self.inv["inv"].remove(item)
        if self.inv[item.slot]:
            self.unequipItem(self.inv[item.slot])
        self.inv[item.slot] = item
        self.countStats()

    def unequipItem(self, item):
        if self.equipItem(item):
            self.inv[item.slot].remove(item)
            self.countStats()

    def countStats(self):
        for stat in self.invStats:
            self.invStats[stat] = 0
        for slot in self.inv:
            if self.inv[slot] is None or slot == "inv":
                continue
            for stat in self.inv[slot].stats:
                self.invStats[stat] += self.inv[slot].stats[stat]


class Character(Entity):
    def __init__(self, name, race="", occupation="", faction=""):
        super().__init__(name)
        self.giveName()
        self.race = race
        self.occupation = occupation
        self.faction = faction
        self.initStats()
        self.initInv()

    """
    Takes base stats from race and then adds whatever bonus stats that
    occupation and faction etc. gives
    """

    def giveName(self):
        # Used for giving random name that fits for the race and faction
        if len(self.name) == 0 or self.name is None:
            names = ["Seppo", "Ismo", "Lasse", "Aaro", "Aki", "Kari"]
            self.name = random.choice(names)

    def initStats(self):
        parser = SettingParser()
        dir = "setting/"

        races = parser.getItems("all", dir + "races.md")
        if self.race in races:
            race = races[self.race]
        else:
            race = races["Default"]
        self._initStat(race)

        occupations = parser.getItems("all", dir + "occupations.md")
        if self.occupation in occupations:
            occupation = occupations[self.occupation]
        else:
            occupation = occupations["Default"]
        self._initStat(occupation)

        factions = parser.getItems("all", dir + "factions.md")
        if self.faction in factions:
            faction = factions[self.faction]
        else:
            faction = factions["Default"]
        self._initStat(faction)

    def initInv(self):
        # inits inventory based on status, occupation and faction
        pass
        # Todo

    def getInfo(self):
        return [
            self.name,
            self.race,
            self.occupation,
            self.faction,
            self.stats,
            self.inv,
        ]
