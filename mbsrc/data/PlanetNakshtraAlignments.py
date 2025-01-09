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
from functools import reduce
from typing import Union
import math
from fileinput import filename


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
def dataframe_intersection(
    dataframes: list[pd.DataFrame], by: Union[list, str]
) -> list[pd.DataFrame]:
    set_index = [d.set_index(by) for d in dataframes]
    index_intersection = reduce(pd.Index.intersection, [d.index for d in set_index])
    intersected = [df.loc[index_intersection].reset_index() for df in set_index]

    return intersected


fileExtn= "_3000.csv"

raviMagha = "raviMagha";
chandraMagha = "chandraMagha";
budhMagha = "budhMagha";
shukraMagha = "shukraMagha";
mangalMagha = "mangalMagha";
guruMagha = "guruMagha";
shaniMagha = "shaniMagha";


df_raviMagha = pd.read_csv(raviMagha + fileExtn)
df_chandraMagha = pd.read_csv(chandraMagha + fileExtn)
df_budhMagha = pd.read_csv(budhMagha + fileExtn)
df_shukraMagha = pd.read_csv(shukraMagha + fileExtn)
df_mangalMagha = pd.read_csv(mangalMagha + fileExtn)
df_guruMagha = pd.read_csv(guruMagha + fileExtn)
df_shaniMagha = pd.read_csv(shaniMagha + fileExtn)


df_list = [df_raviMagha, df_budhMagha]
resultFile = "ravi_budh_magha.csv"
pd.concat(dataframe_intersection(df_list,by='tt')).to_csv(resultFile, sep=',' , encoding='utf-8', index=False)





