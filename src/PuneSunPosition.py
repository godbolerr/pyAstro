from pytz import timezone
from skyfield import almanac
from skyfield import api
from skyfield.api import N, E, wgs84, load
import datetime as dt
import skyfield


ts = api.load.timescale()
ist = timezone('Asia/Kolkata')

eph = load('../de422.bsp')
sun = eph['sun']

# 18.5131118,73.8033453
# 18.5125746,73.8028889

# 18.5126717,73.8055924,
# 18.5125288,73.8057981,


puneLatLon1 = wgs84.latlon(18.5131118 * N, 73.8033453 * E)
puneLatLon2 = wgs84.latlon(18.5126717 * N, 70.8055924 * E)

puneObserver1 = eph['Earth'] + puneLatLon1

puneObserver2 = eph['Earth'] + puneLatLon2


t0 = ts.utc(2024, 3, 20,11,31)

position1 = puneObserver1.at(t0).observe(sun).apparent()

print("Sun position at " , t0.astimezone(ist))
print("ALT AZ 1 " , position1.altaz())
print("Sun RA DEC" , position1.radec())





