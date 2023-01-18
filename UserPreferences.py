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


""" userperfs = UserPreferences()
print(userperfs.checkTemp(90)) # returns "Too hot"
print(userperfs.checkTemp(75)) # returns "Warm"
print(userperfs.checkTemp(72)) # returns "Just right"
print(userperfs.checkTemp(65)) # returns "Cool"
print(userperfs.checkTemp(60)) # returns "Too cold"
print(userperfs.checkTemp(59)) # returns "Error" """