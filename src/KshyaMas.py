from datetime import datetime 
from datetime import timedelta
import datetime


from pytz import timezone
import pytz  
from skyfield import almanac
from skyfield import api

from skyfield.api import GREGORIAN_START
from skyfield.api import N, E, wgs84, load
from skyfield.framelib import ecliptic_frame
from skyfield.toposlib import Topos
from skyfield.trigonometry import position_angle_of
import sqlite3
import datetime as dt
import numpy as np

np.set_printoptions(legacy='1.25')

# –13200 to 17191
# #################### Constants ########################
ts = api.load.timescale()
istZone = timezone('Asia/Kolkata')
ts.julian_calendar_cutoff = GREGORIAN_START
eph = load('../de422.bsp')
sun, moon, earth = eph['sun'], eph['moon'], eph['earth']



startYear = 1600
endYear = 3000
startMonth = 6
startDay = 1


lat=18.5204
long=73.8567 
obsLocation="Pune"

pune = wgs84.latlon(lat * N, long * E)
puneObserver = eph['Earth'] + pune

csvFile = open(f"KshyaMaas_{ startDay }_{startMonth}_{startYear}_{endYear}_{obsLocation}_{lat}_{long}.csv", "a") 

from_dms = lambda degs, mins, secs: degs + mins / 60 + secs / 3600

def convert(seconds):
    hour = int(seconds/3600) 
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60
    
    return "%d:%02d:%02d" % (hour, minutes, seconds)


def cleaupString(slon):
    return str(slon.dms()).replace('(', '').replace(')', '')

def getDms(slon):
    newStr=  str(slon.dms()).replace('(', '').replace(')', '')
    dmsarray =  newStr.split(',')
    return dmsarray[0],dmsarray[1],dmsarray[2]

phaseValue = 0
prevNewMoon = 0

#print("year", "month","day","hour","minute","Duration","Sun Longitude","Moon Longitude",sep="," , file=csvFile )

for curYear in range(startYear, endYear, 1):
 #   print(" Processing from ", curYear)
    t0 = ts.utc(curYear, 1, 1)
    t1 = ts.utc(curYear, 12, 31)
    diff = 0

    t, y = almanac.find_discrete(t0, t1, almanac.moon_phases(eph))
       
    
    for (eventTime , phases ) in zip(t,y) :
        
        if (phases == phaseValue ) :
            
            year, month, day, hour, minute, second = eventTime.tt_calendar()
            
            if  ( prevNewMoon == 0 ):
                prevNewMoon = eventTime.tt
            else :
                curNewMoon = eventTime.tt
                diff = curNewMoon - prevNewMoon
                prevNewMoon = curNewMoon
             
            kmlat, kmlon, distance = earth.at(eventTime).observe(moon).frame_latlon(ecliptic_frame)
            kslat, kslon, distance = earth.at(eventTime).observe(sun).frame_latlon(ecliptic_frame)
                        
            ksld,kslm,ksls = getDms(kslat)
            ksod,ksom,ksos = getDms(kslon)    
            kmld,kmlm,kmls = getDms(kmlat)   
            kmod,kmom,kmos = getDms(kmlon)               
            
            dt = eventTime.astimezone(pytz.timezone("Asia/Kolkata"))
            
            
            print(dt.year, dt.month,dt.day,dt.hour,dt.minute,dt.second,diff,ksod,ksom,ksos,round(diff*24*60*60), sep=",", file=csvFile )

