import geopandas
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

df = pd.read_csv("LIM_pixels_population.csv")

fig = plt.figure()

ax = fig.add_subplot(111, projection='3d')
ax.bar(left=df.lat, height=df.population, zs=df.lon, zdir='z')

# ax1 = fig.add_subplot(121, projection='3d')
# ax1.bar(left=df.utm_n, height=df.population, zs=df.utm_e)

plt.show()
