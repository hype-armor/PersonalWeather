import math

windunit = [0, 0, 0, 1] # 0 = Knots, 1 = Meters/second, 2 = Kilometers/hour, 3 = Miles/hour
tempunit = [1, 0] # 0 = Fahrenheit, 1 = Celsius

def CalculateWindChill(temp, WindSpeed):
    temp = float(temp)
    WindSpeed = float(WindSpeed)
    global windspeed
    windspeed = ""
    global Fahr
    global Cels
    global Temp
    global Watts

    if windunit[0] == 1:
        WindSpeed = convertktstomph(WindSpeed)
        ws1 = convertktstomps(WindSpeed)

        if WindSpeed < 3:
            print(
                'A Wind Chill value cannot be calculated for wind speeds less than 2.6 Knots')
            windspeed = ""
            return 0

        if WindSpeed > 110:
            print(
                'A Wind Chill value cannot be calculated for wind speeds greater than 95.6 Knots')
            windspeed = ""
            return 0

    if windunit[1] == 1:
        WindSpeed = convertmpstomph(WindSpeed)
        ws1 = windunit[2]

        if WindSpeed < 3:
            print(
                'A Wind Chill value cannot be calculated for wind speeds less than 1.3 meters/second')
            windspeed = ""
            return 0

        if WindSpeed > 110:
            print(
                'A Wind Chill value cannot be calculated for wind speeds greater than 49.2 meters/second')
            windspeed = ""
            return 0

    if windunit[2] == 1:
        WindSpeed = convetkphtomph(WindSpeed)
        ws1 = convertkphtomps(WindSpeed)

        if WindSpeed < 3:
            print(
                'A Wind Chill value cannot be calculated for wind speeds less than 4.8 kilometers/hour')
            windspeed = ""
            return 0

        if WindSpeed > 110:
            print(
                'A Wind Chill value cannot be calculated for wind speeds greater than 177 kilometers/hour')
            windspeed = ""
            return 0

    if tempunit[0] == 1:
        ws1 = convertmphtomps(WindSpeed)
        temp1 = convertFtoC(temp)

        if WindSpeed < 3:
            print('A Wind Chill value cannot be calculated for wind speeds less than 3 miles/hour')
            windspeed = ""
            return 0

        if WindSpeed > 110:
            print(
                'A Wind Chill value cannot be calculated for wind speeds greater than 110 miles/hour')
            windspeed = ""
            return 0

        if temp > 50:
            print(
                'A Wind Chill value cannot be calculated for temperatures greater than 50 degrees Fahrenheit.')
            
            Fahr = ""
            Cels = ""
            Temp = ""
        else:
            Fahr = roundOff(windChill(temp, WindSpeed))
            C = float(Fahr)
            Cels = roundOff(convertFtoC(C))
            Watts = roundOff(WPM2(temp1, ws1))
            return Fahr, Cels, Watts

    if tempunit[1] == 1:
        F = convertCtoF(temp)
        ws1 = convertmphtomps(WindSpeed)

        if WindSpeed < 3:
            print('A Wind Chill value cannot be calculated for wind speeds less than 3 miles/hour')
            windspeed = ""
            return 0

        if WindSpeed > 110:
            print('A Wind Chill value cannot be calculated for wind speeds greater than 110 miles/hour')
            windspeed = ""
            return 0

        if F > 50:
            print('A Wind Chill value cannot be calculated for temperatures greater than 10.0 degrees Celsius.')
            Fahr = ""
            Cels = ""
            Temp = ""

        else:
            Fahr = roundOff(windChill(F, WindSpeed))
            Cels = roundOff((convertFtoC(windChill(F, WindSpeed))))
            Watts = roundOff(WPM2(temp, ws1))
            return Fahr, Cels, Watts
        


def convertFtoC(Fahr):
    Celsius = .55556 * (Fahr - 32)
    return Celsius


def convertCtoF(Cels):
    Fahr = 1.8 * Cels + 32
    return Fahr


def convertktstomph(knots):
    mph = 1.1507794 * knots
    return mph


def convertmpstomph(mps):
    mph = 2.23694 * mps
    return mph


def convertmphtomps(mph):
    ws1 = 0.44704 * mph
    return ws1


def convertktstomps(knots):
    ws1 = 0.5144444 * knots
    return ws1


def convetkphtomph(kph):
    mph = 0.621371 * kph
    return mph


def convertkphtomps(kph):
    ws1 = 0.277778 * kph
    return ws1


def windChill(F, mph):
    wChill = 35.74 + .6215 * F - 35.75 * \
    math.pow(mph, 0.16) + 0.4275 * F * math.pow(mph, 0.16)
    return wChill


def WPM2(C, mps):
    Watts = (12.1452 + 11.6222 * math.sqrt(mps) - 1.16222 * mps) * (33 - C)
    return Watts



def roundOff(value):
    value = round(10 * value) / 10
    return value
