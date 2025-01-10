# pyAstro
PyAstro Repository for skyfield

All calcuations related to Tithi


mbsrc folder contains data related to seperation angle between 7 planets and some nakshtra mentioned in the Mahabharat.

skyfield python library is used for data computations.

Refer to csv files for input data related to RA/DEC of Nakshatras.

de422.bsp and hip_main.dat will be downloaded locally for the first run. Need internet connection for the same.

mbsrc/data contains csv file for each combination and one or more collective combinations


1. Generate data with NakPlanetPositionInfo.py - some manual setting is required in the code.
2. Run data/PlanetNakshatraAlignments to find out dates for the desired comibinations
