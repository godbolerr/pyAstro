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
import NakPlanet


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


yogtaradic = {  "Magha" : 49669 ,
               "Jeshtha" : 80112 ,
                "Vishakha" : 72622 ,
               "Anuradha" : 78265 ,
               "Rohini" : 21421 
             }  

graha = { "ravi" : ravi ,
               "chandra" : chandra ,
               "mangal" : mangal ,
               "budh" : budh ,
               "guru" : guru ,
               
               "shukra" : shukra ,
               'shani' : shani
             }  




with load.open(hipparcos.URL) as f:
    df = hipparcos.load_dataframe(f) 
    
# Magha, Jeshtha, Vishakha, Anuradha, Rohini

stars=['Jeshtha','Vishakha','Anuradha','Rohini']
planets=['ravi','chandra','mangal','budh','shukra','shani','guru']
sepAngle = 6


for star in stars:
    for planetName in planets:
    

        hip = yogtaradic[star]
        
        planet = graha[planetName]
        totalYears = 2000
        
        csvFile = open(f"MahaAna_{ planetName }_{star}_{sepAngle}.csv", "w") 
        
        print ("Timing is midnight UTC. Add +530 for IST. Year Range : 3000 BC to 1000 BC, HIPCode for star : HIP", hip, file=csvFile)
        
        print ("planetName,starName,day,month,year,Seperation Angle",file=csvFile)
        
        
        t = ts.utc(-3000,12, 12)
        count=0
        for counter in range(0, 365*totalYears, 1):
            barnards_star = Star.from_dataframe(df.loc[hip])
            position_star = kuruKshetraObserver.at(t).observe(barnards_star)
            position_planet = kuruKshetraObserver.at(t).observe(planet)
            sepDegrees = position_star.separation_from(position_planet).degrees
            if ( sepDegrees < sepAngle ) :
                year, month, day, hour, minute, second = t.tai_calendar()
                print(planetName,star,day,month,year,sep=" : ")
                print(planetName, star ,  day,month,year , sepDegrees , sep = " , ", file=csvFile)
        
            t = t + dt.timedelta(days=1)
    
