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

df_nakshatra = pd.read_csv("NakshatraYogtara.csv", header=0) 

with load.open(hipparcos.URL) as f:
    df = hipparcos.load_dataframe(f) 


grahas = [  ("ravi",ravi,1) ,("chandra",chandra,2),("budh",budh,3) , ("shukra",shukra,4), ("mangal",mangal,5),("guru",guru,6), ("shani",shani,7) ] 


starSeq = 10
star = df_nakshatra.loc[starSeq]['Name']
hip = df_nakshatra.loc[starSeq]['HIP']
totalYears = 3000
sepAngle = 6
t = ts.utc(-2997,1, 1)

print("Processing ", star, " with hip code " , hip)

for graha in grahas :

    recordIdentifier = str(graha[2]) + "" + str(starSeq)
    
    grahaName = graha[0]
    


#    or grahaName == 'shukra'  or grahaName == 'mangal'  grahaName == 'ravi' or grahaName == 'chandra' or or grahaName == 'shukra'
#    grahaName == 'ravi' or
    if (  grahaName == 'budh' or grahaName == 'guru' ) :
    
        csvFileName = str(graha[0])  + str(star) + "_" + str(totalYears) + ".csv"
        
        print("Graha Name " , graha[0], "with sequence " , graha[2], " and identifier " + recordIdentifier , " ",  csvFileName )
        
        nakPlanetInfos = []
        for counter in range(0, 365*totalYears, 1):
             barnards_star = Star.from_dataframe(df.loc[hip])
             position_star = kuruKshetraObserver.at(t).observe(barnards_star)
             position_planet = kuruKshetraObserver.at(t).observe(graha[1])
             sepDegrees = position_star.separation_from(position_planet).degrees
             year, month, day, hour, minute, second = t.tai_calendar()
             thisId = str(graha[2]) + "" + str(starSeq)
             if ( sepDegrees < sepAngle ) : 
                 nakPlanetInfos.append(NakPlanetInfo(math.trunc(t.tt), thisId ,year,month,day,math.trunc(sepDegrees)))
          
             t = t + dt.timedelta(days=1)
             
        dff = pd.DataFrame([vars(s) for s in nakPlanetInfos], columns=['tt','recId','year', 'month','day','angle'])
        
        print(dff)
         
        dff.to_csv(csvFileName, sep=',' , encoding='utf-8', index=False)
        
            
    
    
    