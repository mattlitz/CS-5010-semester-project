import pandas as pd 
import numpy as np 
import matplotlib.pyplot as plt
import geopandas


csa = geopandas.read_file('/home/matt/Documents/UVa - Data Science Masters/CS 5010/CS-5010-semester-project/shapefiles/cb_2018_us_csa_20m.shp')
states = geopandas.read_file('/home/matt/Documents/UVa - Data Science Masters/CS 5010/CS-5010-semester-project/shapefiles/cb_2018_us_state_20m.shp')

csa = csa.to_crs("EPSG:3395")
states = states.to_crs("EPSG:3395")
print(states)

#Alaska and Hawaii excluded due to lack of CSA
states=states[states['NAME'] != 'Alaska']
states=states[states['NAME'] != 'Hawaii']

us_boundary_map = states.boundary.plot(figsize=(18, 12),color="Black", linewidth=.1)

csa.plot(ax=us_boundary_map, cmap='magma')
#print(cbsa)
#csa[csa['NAME'] == 'Des Moines-Ames-West Des Moines, IA'].plot(figsize=(12, 12))



