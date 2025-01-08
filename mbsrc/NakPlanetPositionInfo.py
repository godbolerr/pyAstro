from pytz import timezone
from skyfield import almanac
from skyfield import api
from skyfield.api import GREGORIAN_START
from skyfield.api import N, E, wgs84, load
from skyfield.toposlib import Topos
from skyfield import eclipselib
from skyfield.framelib import ecliptic_frame
import datetime as dt
from skyfield.api import Star, load
from skyfield.data import hipparcos
import datetime as dt
from ntpath import sep
from NakPlanet import NakPlanetInfo
import pandas as pd
import math


''' 
Ravi - Magha, mangal - jeshtha/anuradha , shani -  rohini

h4- a11 s18 

mangal , budha = magha
shukra = jeshtha

h3 - a3 s28-32

ravi = magha/jeshtha
chandra = magha
guru = vishakha
shani  = rohini / vishakha

h4 = a11 s18

mangal = magha
budha = magha
shukra = jeshtha

h2 a3 s11 15,18

ravi = magha
chndra
mangal
budh
guru
shukra

shani = rohini


'''
ts = api.load.timescale()
ts.julian_calendar_cutoff = GREGORIAN_START
eph = load('../de422.bsp')

ist = timezone('Asia/Kolkata')
kuruKshetra = wgs84.latlon(29.9695 * N, 76.8783 * E)
kuruKshetraObserver = eph['Earth'] + kuruKshetra


ravi, chandra, earth, mangal,budh,shukra,shani,guru = eph['sun'], eph['moon'], eph['earth'], eph['mars'],eph['mercury'],eph['venus'],eph['SATURN BARYCENTER'],eph['JUPITER BARYCENTER']

sepAngles = [1,2,3,4,5]

nakshatras = {  "magha" : 49669 ,
               "jeshtha" : 80112 ,
                "vishaka" : 72622 ,
               "anuradha" : 78265 ,
               "rohini" : 21421 
             }  




grahas = {    
    
    'shani' : shani,
    "guru" : guru ,
    "mangal" : mangal ,
    "ravi" : ravi ,
    "shukra" : shukra ,
    "budh" : budh ,
    "chandra" : chandra 
    }  




with load.open(hipparcos.URL) as f:
    df = hipparcos.load_dataframe(f) 
    


totalYears = 1000
 #'',   
#stars=['jeshtha','vishaka','anuradha','rohini']
stars=['magha']

planets=['ravi','budh','shukra','chandra']
sepAngle = 6


for star in stars:
    for planetName in planets:

        hip = nakshatras[star]
        
        planet = grahas[planetName]
        totalYears = 1000
        t = ts.utc(-2999,1, 1)
        count=0
        
        nakPlanetInfos = []

        csvFileName = str(planetName) + "_" + str(star) + "_" + str(totalYears) + ".csv"
        
        print(csvFileName)
        
        for counter in range(0, 365*totalYears, 1):
            barnards_star = Star.from_dataframe(df.loc[hip])
            position_star = kuruKshetraObserver.at(t).observe(barnards_star)
            position_planet = kuruKshetraObserver.at(t).observe(planet)
            sepDegrees = position_star.separation_from(position_planet).degrees
            year, month, day, hour, minute, second = t.tai_calendar()
            if ( sepDegrees < sepAngle ) : 
                nakPlanetInfos.append(NakPlanetInfo(year,month,day,math.trunc(t.tt),math.trunc(sepDegrees)))
         
            t = t + dt.timedelta(days=1)
            
        dff = pd.DataFrame([vars(s) for s in nakPlanetInfos], columns=['year', 'month','day','tt','angle'])
        
        print(dff)
        
        
        
        dff.to_csv(csvFileName, sep=',' , encoding='utf-8', index=False)