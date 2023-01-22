class UserPreferences:
    dictoftemps = {'Scorching': 90, 'Hot': 84, 'Warm': 78, 'Mild': 72, 'Cool': 65,
                    'Chilly': 60, 'Cold': 50, 'Really Cold': 45, 'Freezing': 39, 'Frostbite': 32}

    def __init__(self):
        ""

    def getTemp(self, key):
        return self.dictoftemps[key]

    def setTemp(self, key, value):
        self.dictoftemps[key] = value

    def checkTemp(self, value):
        # loop through a dictionary and compare the value to the key
        for key, temp in self.dictoftemps.items():
            if value >= temp:
                return key
        return "Absolute Zero"
