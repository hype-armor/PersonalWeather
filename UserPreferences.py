class UserPreferences:
    dictoftemps = {'Burning': 90, 'warm': 75, 'justright': 72, 'cool': 65, 'toocold': 60,
                   'Freezing': 50, 'arctic': 40, 'polar': 30, 'frozen': 20, 'ice': 10, 'frostbite': 0}

    def __init__(self):
        print("UserPreferences.__init__")

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
