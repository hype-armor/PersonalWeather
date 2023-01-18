import math, json

RADEG = 180.0 / math.pi
DEGRAD = math.pi / 180.0
INV360 = 1.0 / 360.0
def daysSince2000Jan0(y, m, d):
    return (367 * (y) - ((7 * ((y) + (((m) + 9) / 12))) / 4) + ((275 * (m)) / 9) + (d) - 730530)

def sind(x):
    return math.sin(x * DEGRAD)

def cosd(x):
    return math.cos(x * DEGRAD)

def tand(x):
    return math.tan(x * DEGRAD)

def atand(x):
    return math.atan(x) * RADEG

def asind(x):
    return math.asin(x) * RADEG

def acosd(x):
    return math.acos(x) * RADEG

def atan2d(y, x):
    return math.atan2(y, x) * RADEG

def dayLength(year, month, day, lon, lat):
    return daylen(year, month, day, lon, lat, -35.0 / 60.0, 1)

def dayCivilTwilightLength(year, month, day, lon, lat):
    return daylen(year, month, day, lon, lat, -6.0, 0)

def dayNauticalTwilightLength(year, month, day, lon, lat):
    return daylen(year, month, day, lon, lat, -12.0, 0)

def dayAstronomicalTwilightLength(year, month, day, lon, lat):
    return daylen(year, month, day, lon, lat, -18.0, 0)

def sunRiseSet(year, month, day, lon, lat):
    return sunriset(year, month, day, lon, lat, -35.0 / 60.0, 1)

def civilTwilight(year, month, day, lon, lat):
    return sunriset(year, month, day, lon, lat, -6.0, 0)

def nauticalTwilight(year, month, day, lon, lat):
    return sunriset(year, month, day, lon, lat, -12.0, 0)

def astronomicalTwilight(year, month, day, lon, lat):
    return sunriset(year, month, day, lon, lat, -18.0, 0)

def sunriset(year, month, day, lon, lat, altit, upper_limb):
    # Compute d of 12h local mean solar time
    d = daysSince2000Jan0(year, month, day) + 0.5 - (lon / 360.0)

    # Compute local sidereal time of this moment
    sidtime = revolution(GMST0(d) + 180.0 + lon)

    # Compute Sun's RA + Decl at this moment
    res = sunRADec(d)
    sRA = res[0]
    sdec = res[1]
    sr = res[2]

    #Compute time when Sun is at south - in hours UT
    tsouth = 12.0 - rev180(sidtime - sRA) / 15.0

    #Compute the Sun's apparent radius, degrees
    sradius = 0.2666 / sr

    #Do correction to upper limb, if necessary
    if (upper_limb):
        altit = altit - sradius

    # Compute the diurnal arc that the Sun traverses to reach
    # the specified altitude altit:

    cost = (sind(altit) - sind(lat) * sind(sdec)) / (cosd(lat) * cosd(sdec))

    if (cost >= 1.0):
        rc = -1
        t = 0.0
    elif (cost <= -1.0):
        rc = +1
        t = 12.0
    else:
        t = acosd(cost) / 15.0

    return [tsouth - t, tsouth + t]

def daylen(year, month, day, lon, lat, altit, upper_limb):
    # Compute d of 12h local mean solar time
    d = daysSince2000Jan0(year, month, day) + 0.5 - (lon / 360.0)

    # Compute obliquity of ecliptic (inclination of Earth's axis)
    obl_ecl = 23.4393 - 3.563E-7 * d

    # Compute Sun's position
    res = sunpos(d)
    slon = res[0]
    sr = res[1]

    # Compute sine and cosine of Sun's declination
    sin_sdecl = sind(obl_ecl) * sind(slon)
    cos_sdecl = math.sqrt(1.0 - sin_sdecl * sin_sdecl)

    # Compute the Sun's apparent radius, degrees
    sradius = 0.2666 / sr

    # Do correction to upper limb, if necessary
    if (upper_limb):
        altit = altit - sradius


    cost = (sind(altit) - sind(lat) * sin_sdecl) / (cosd(lat) * cos_sdecl)
    if (cost >= 1.0):
        t = 0.0

    elif (cost <= -1.0):
        t = 24.0

    else:
        t = (2.0 / 15.0) * acosd(cost)

    return t


def sunpos(d):

    # Compute mean elements
    M = revolution(356.0470 + 0.9856002585 * d)
    w = 282.9404 + 4.70935E-5 * d
    e = 0.016709 - 1.151E-9 * d

    # Compute true longitude and radius vector
    E = M + e * RADEG * sind(M) * (1.0 + e * cosd(M))
    x = cosd(E) - e
    y = math.sqrt(1.0 - e * e) * sind(E)
    r = math.sqrt(x * x + y * y)
    v = atan2d(y, x)
    lon = v + w
    if lon >= 360.0:
        lon = lon - 360.0


    return [lon, r]


def sunRADec(d):
    # Compute Sun's ecliptical coordinates
    res = sunpos(d)
    lon = res[0]
    r = res[1]

    # Compute ecliptic rectangular coordinates (z=0)
    x = r * cosd(lon)
    y = r * sind(lon)

    # Compute obliquity of ecliptic (inclination of Earth's axis)
    obl_ecl = 23.4393 - 3.563E-7 * d

    # Convert to equatorial rectangular coordinates - x is unchanged
    z = y * sind(obl_ecl)
    y = y * cosd(obl_ecl)

    # Convert to spherical coordinates
    RA = atan2d(y, x)
    dec = atan2d(z, math.sqrt(x * x + y * y))

    return [RA, dec, r]

def zenith(year, month, day, hour, minute, lon, lat, timeshiftHr, jDay):
    rdat = []
    rdat = sunRADec(jDay)
    ra = rdat[0]
    dec = rdat[1]
    r = rdat[2]

    # Compute d of 12h local mean solar time
    d = daysSince2000Jan0(year, month, day) + 0.5 - (lon / 360.0)

    # Compute obliquity of ecliptic (inclination of Earth's axis)
    obl_ecl = 23.4393 - 3.563E-7 * d

    # Compute sine and cosine of Sun's declination
    sin_sdecl = sind(dec)
    cos_sdecl = cosd(dec)

    # sin cos of lat
    sin_lat = sind(lat)
    cos_lat = cosd(lat)

    sdat = []
    sdat = sunRiseSet(year, month, day, lon, lat)
    srise = sdat[0]
    sset = sdat[1]
    daylen = sset - srise
    solarNoon = srise + 0.5 * daylen
    solarNoon = solarNoon + timeshiftHr
    currentTime = hour + (minute / 60.)
    deltaNoon = currentTime - solarNoon
    degsHour = 180. / daylen
    solarHourDeg = math.abs(deltaNoon * degsHour)
    cos_hr = cosd(solarHourDeg)

    n = sin_sdecl * sin_lat + cos_sdecl * cos_lat * cos_hr
    if (n > 1):
        n = 1

    zenith = acosd(n)
    return [solarHourDeg, zenith]


def revolution(x):
    return (x - 360.0 * math.floor(x * INV360))


def rev180(x):
    return (x - 360.0 * math.floor(x * INV360 + 0.5))


def GMST0(d):
    sidtim0 = revolution((180.0 + 356.0470 + 282.9404) + (0.9856002585 + 4.70935E-5) * d)
    return sidtim0

def solar_altitude(latitude, year, month, day):
    N = daysSince2000Jan0(year, month, day)
    res = sunRADec(N)
    declination = res[1]
    sr = res[2]
    altitude = 90.0 - latitude + declination
    if (altitude > 90):
        altitude = 90 - (altitude - 90)
    if (altitude < 0):
        altitude = 0
    return altitude




def get_max_solar_flux(latitude, year, month, day):

    edat = []
    edat = equation_of_time(year, month, day, latitude)
    fEot = edat[0]
    fR0r = edat[1]
    tDeclsc = []
    tDeclsc = edat[2]
    fSF = (tDeclsc[0] + tDeclsc[1]) * fR0r



    # In the case of a negative declinaison, solar flux is null
    if (fSF < 0):
        fCoeff = 0
    else:
        fCoeff = -1.56e-12 * math.pow(fSF, 4) + 5.972e-9 * math.pow(fSF, 3) - 8.364e-6 * math.pow(fSF, 2) + 5.183e-3 * fSF - 0.435

    fSFT = fSF * fCoeff

    if (fSFT < 0):
        fSFT = 0

    return fSFT

def isleap(year):
    if (year % 4 == 0 and year % 10 != 0):
        return True
    return False

def equation_of_time(year, month, day, latitude):

    nJulianDate = Julian(year, month, day)

    if (isleap(year)):
        fDivide = 366.0
    else:
        fDivide = 365.0


    fA = nJulianDate / fDivide * 2 * math.pi
    fR0r = Solcons(fA) * 0.1367e4
    fRdecl = 0.412 * math.cos((nJulianDate + 10.0) * 2.0 * math.pi / fDivide - math.pi)
    fDeclsc1 = sind(latitude) * math.sin(fRdecl)
    fDeclsc2 = cosd(latitude) * math.cos(fRdecl)
    tDeclsc = [fDeclsc1, fDeclsc2]

    fEot = 0.002733 - 7.343 * math.sin(fA) + .5519 * math.cos(fA) - 9.47 * math.sin(2.0 * fA) - 3.02 * math.cos(2.0 * fA) - 0.3289 * math.sin(3.0 * fA) - 0.07581 * math.cos(3.0 * fA) - 0.1935 * math.sin(4.0 * fA) - 0.1245 * math.cos(4.0 * fA)

    fEot = fEot / 60.0

    fEot = fEot * 15 * math.pi / 180.0

    return [fEot, fR0r, tDeclsc]

def Solcons(dAlf):
    dVar = 1.0 / (1.0 - 9.464e-4 * math.sin(dAlf) - 0.01671 * math.cos(dAlf) -
        + 1.489e-4 * math.cos(2.0 * dAlf) - 2.917e-5 * math.sin(3.0 * dAlf) -
        + 3.438e-4 * math.pow(math.cos(4.0 * dAlf)), 2)
    return dVar

def Julian(year, month, day):

    if isleap(year):
        lMonth = [0, 31, 60, 91, 121, 152, 182, 213, 244, 274, 305, 335, 366]

    else:
        lMonth = [0, 31, 59, 90, 120, 151, 181, 212, 243, 273, 304, 334, 365]

    nJulian = lMonth[month - 1] + day
    return nJulian

def calcDwpt():
	T = (.556 * (iTemp - 32.0)) + 273.15
	a=0.0091379024*T + 6106.396/T - math.log(iRH/100.)
	b = math.sqrt((a*a) - 223.1986)
	DpT = (a-b)/0.0182758048
	DewPtF=(DpT-273.15)*1.8+32.
	return math.round(DewPtF)
  

def calcRH():
	Tc = .556 * (iTemp - 32.0)
	Tdc = .556 * (iDwpt - 32.0)
	Vt = 6.11 * math.pow(10,(Tc * 7.5 / (Tc + 237.3)))
	Vd = 6.11 * math.pow(10,(Tdc * 7.5 / (Tdc + 237.3)))
	RH = (Vd / Vt) * 100.0
	return math.round(RH)



def getNDFD(lonLat):
    ndfdAPI="https:#forecast.weather.gov/MapClick.php?w0=t&w1=td&w2=hi&w3=sfcwind&w3u=0&w4=sky&w5=pop&w6=rh&w7=rain&w8=thunder&pqpfhr=6&AheadHour=0&Submit=Submit&FcstType=json&textField1="+lonLat[1]+"&textField2="+lonLat[0]+"&site=all&unit=0&dd=&bw="

    latString=(data.location.latitude) 

    lonString=(data.location.longitude)
    elevationString=(data.location.elevation) 
    label0=(data.time.tempLabel[0])
    if(label0=="High"):
        maxPd=0
        maxDay="Today" 
    else:
        maxPd=1
        maxDay="Tomorrow" 
    maxT=(data.data.temperature[maxPd])
    if (maxT >= 40 and maxT <= 130):
        setTemp(maxT)
    
    sky=(data.data.weather[maxPd])
    if (sky=="Sunny"):
        setSky(0)
    elif (sky=="Hot" or sky=="Mostly Sunny" or sky=="Partly Cloudy" ):
        setSky(20)
    elif (sky=="Mostly Cloudy" or sky=="Partly Sunny" ):
        setSky(60)
    elif (sky=="Cloudy" ):
        setSky(100)
    else:
        setSky(50)
    dwpt=(data.currentobservation.Dewp)
    if (dwpt>=40 and dwpt<=130):
        setDwpt(dwpt)
    spd=(data.currentobservation.Winds)
    if (spd>=0 and spd<=100):
        setSpd(spd)
    pres=(data.currentobservation.Altimeter)
    if(pres>=26 and pres<=34):
        presMB=pres*33.8639
    else:
        presMB=1000
    
    slp=(data.currentobservation.SLP)
    console.log(maxDay+"- MaxT="+maxT+" dwpt="+dwpt+" spd="+spd+" pres="+pres+" slp="+slp+" sky="+sky)
    updateRH()
    document.getElementById("loading").src=""
    
    calcWBGT()

def calcWBGT():
    T=iTemp
    if(T<80):
        HeatIndex=T
    else:
        Tc = .556 * (iTemp - 32.0)
        Tdc = .556 * (iDwpt - 32.0)
        #Vt = 6.11 * pow(10,(Tc * 7.5 / (Tc + 237.3)))
        #Vd = 6.11 * pow(10,(Tdc * 7.5 / (Tdc + 237.3)))   
        RH = iRH
        A = -42.379
        B =  2.04901523 * T
        C = 10.14333127 * RH
        D = -0.22475541 * T * RH
        E = -0.00683783 * math.pow(T, 2)
        F = -0.05481717 * math.pow(RH, 2)
        G =  0.00122874 * math.pow(T, 2) * RH
        H =  0.00085282 * T * math.pow(RH, 2)
        I = -0.00000199 * math.pow(T, 2) * math.pow(RH, 2)
        HeatIndex = A + B + C + D + E + F + G + H + I

        if (RH<13 and T>=80 and T<=112):
            HeatIndex = HeatIndex - ( (13 - RH)/4.)* math.sqrt((17-math.abs(T-95))/17)  
            
        if (RH>85 and T>=80 and T<=87):
            HeatIndex = HeatIndex + ( ( (RH-85)/10)*((87-T)/5) )
    
    heat=math.round(HeatIndex)
    if (heat<100):
        backcolor="#00ff00"
    elif (heat<105):
        backcolor="#ffff00"
    elif (heat<110):
        backcolor="#ff561f"
    elif (heat<115):
        backcolor="#ff7ad2"
    else:
        backcolor="#c07aff"
    
    document.getElementById("hiValue").innerHTML=math.round(heat)
    (document.getElementById("hiValue")).style.backgroundColor=backcolor
    #wbgt
    maxFlux=get_max_solar_flux(lonLat[1],iYear,iMonth,iDay)
    cosz=0.707
    if(iWspd<4):
        spd=4
    else:
        spd=iWspd
    wspd=spd*1609 # m/hr
    t=(iTemp-32)*5/9 # c
    td=(iDwpt-32)*5/9 # c
    p=presMB
    fdb= iCloud/100. 
    fdif= 1.0 - fdb
    bc=5.67*math.pow(10,-8)
    h=0.315
    a=math.exp( (17.67*(td-t))/(td+243.5) )
    b=math.exp( (17.502*t)/(240.97+t) )
    ea=a*(1.0007+0.00000346*p)*(6.112*b)
    frac=1./7.
    ea2=math.pow(ea*0.575,frac)
    b1= fdb/(4*cosz*bc)+(1.2/bc)*fdif
    b2=ea2*math.pow(t,4)
    b=maxFlux*b1+b2
    c=(math.pow(wspd,0.58)*h)/(5.3865*math.pow(10,-8))
    tg=((b+c*t+7680000)/(c+256000))* 1.8 + 32

    c1 = 0.0091
    c2 = 6106.40
    f = 0.0006355
    
        
    fp = f * p
    es = 6.11 * math.pow(10,((t * 7.5) / (t + 237.3)))
    ed = 6.11 * math.pow(10,((td * 7.5) / (td + 237.3)))
    s1 = (es-ed)
    s2 = (t-td)
    
    if(s2==0):
        Twc=t
    else:
        Twc=((t)*(fp)+(td*(s1)/(s2) ))/(fp+(s1)/(s2))
    Tw = (1.8 * Twc) + 32 # wet bulf F	
    count=0 # adjust Tw
    while(count<5):
        Twk = Twc + 273.15
        ew = 6.11 * math.pow(10,((Twc*7.5) / (Twc + 237.3)))
        de1 = fp*(t-Twc)
        de = de1 - (ew-ed)
        der = ((ew*(c1-(c2/math.pow(Twk,2)))-fp))
        Twk = Twk - (de/der)
        Twc = Twk - 273.15
        Tw = (1.8 * Twc) + 32
        count = count + 1
    
    wms=iWspd * .4474 # mph to m/s
    ir=maxFlux
    nwb= Tw + (0.0021 * ir)  - (0.43 * wms) + 1.93
    if(nwb<Tw):
        nwb=Tw
    if(nwb<50):
        nwb=50
    if(nwb>85):
        nwb=85
            
    shady=0.3*T+0.7*nwb
    wbgt=0.2*tg+0.7*nwb+0.1*T

    wb=math.round(wbgt)
    if(wb<83):
        backcolor="#00ff00"
    elif(wb<86):
        backcolor="#ffff00"
    elif(wb<90):
        backcolor="#ff561f"
    elif(wb<93):
        backcolor="#ff7ad2"
    else:
        backcolor="#c07aff"
    document.getElementById("wbgtValue").innerHTML=wb
    (document.getElementById("wbgtValue")).style.backgroundColor=backcolor				
