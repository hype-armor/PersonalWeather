class UserPreferences:
    dict = {'Burning': 90, 'warm': 75, 'justright': 72, 'cool': 65, 'toocold': 60}
    
    def __init__(self):
        print("UserPreferences.__init__")
    
    def getTemp(self, key):
        return self.dict[key]

    def setTemp(self, key, value):
        self.dict[key] = value
    
    def checkTemp(self, value):
        if value >= self.dict["Burning"]:
            return "Burning"
        elif value >= self.dict["warm"]:
            return "Warm"
        elif value >= self.dict["justright"]:
            return "Just right"
        elif value >= self.dict["cool"]:
            return "Cool"
        elif value >= self.dict["toocold"]:
            return "Too cold"
        else:
            return "Freezing"