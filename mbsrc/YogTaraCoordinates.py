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


ravi, chandra, earth, mangal,budh,shukra,shani = eph['sun'], eph['moon'], eph['earth'], eph['mars'],eph['mercury'],eph['venus'],eph['SATURN BARYCENTER']


yogtaradic = { "Ashwini" : 8832 ,
               "Magha" : 49669 ,
               "Jeshtha" : 80112 ,
               "Anuradha" : 78265 ,
               "Rohini" : 21421 
             }  

graha = { "ravi" : ravi ,
               "chandra" : chandra ,
               "mangal" : mangal ,
               "budh" : budh ,
               "shukra" : shukra ,
               'Shani' : shani
             }  




with load.open(hipparcos.URL) as f:
    df = hipparcos.load_dataframe(f) 
    
star = 'Rohini'
planetName = 'Shani'
    
hip = yogtaradic[star]

planet = graha[planetName]

t = ts.utc(-3000,12, 12)

for counter in range(0, 365*100, 1):
    barnards_star = Star.from_dataframe(df.loc[hip])
    position_star = kuruKshetraObserver.at(t).observe(barnards_star)
    position_planet = kuruKshetraObserver.at(t).observe(planet)
    sepDegrees = position_star.separation_from(position_planet).degrees
    if ( sepDegrees < 4 ) :
        year, month, day, hour, minute, second = t.tai_calendar()
        print(star , hip , planetName, day,month,year , sepDegrees , sep = " , ")

    t = t + dt.timedelta(days=1)

