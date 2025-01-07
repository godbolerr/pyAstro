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


ravi, chandra, earth, mangal= eph['sun'], eph['moon'], eph['earth'], eph['mars']


yogtaradic = { "Ashwini" : "HIP8832" ,
               "Magha" : "HIP49669" ,
               "Jeshtha" : "HIP80112" ,
               "Anuradha" : "HIP78265" ,
               "Rohini" : "HIP21421" 
             }  


with load.open(hipparcos.URL) as f:
    df = hipparcos.load_dataframe(f) 
    
hip = 49669

t = ts.utc(-100,1, 1)

for counter in range(0, 365*100, 1):
    barnards_star = Star.from_dataframe(df.loc[hip])
    position_star = kuruKshetraObserver.at(t).observe(barnards_star)
    position_planet = kuruKshetraObserver.at(t).observe(mangal)
    sepDegrees = position_star.separation_from(position_planet).degrees
    if ( sepDegrees < 1 ) :
        year, month, day, hour, minute, second = t.tai_calendar()
        print(day,month,year, "   " , sepDegrees)

    t = t + dt.timedelta(days=1)

