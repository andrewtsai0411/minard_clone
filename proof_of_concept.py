import sqlite3
import pandas as pd
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt

connection = sqlite3.connect('data/minard.db')

# 繪製地圖
m = Basemap(projection='lcc',resolution='i',width=1000000,height=400000,
            lon_0=31,lat_0=55)

m.drawcountries()
m.drawrivers()
m.drawparallels(range(54,58),labels=[True,False,False,False])
m.drawmeridians(range(23,56,2),labels=[False,False,False,True])
lons = [24.0, 37.6] # 24.0, 55.0 Kowno;
lats = [55.0, 55.8] # 37.6, 55.8 Moscou;
xi, yi = m(lons, lats)
m.scatter(xi, yi)
plt.tight_layout()
plt.show()

# 繪製城市圖
city_df = pd.read_sql('SELECT * FROM cities;', con=connection)
connection.close()
lons = city_df['lonc'].values
lats = city_df['latc'].values
city_names = city_df['city'].values
fig, ax = plt.subplots()
m = Basemap(projection='lcc',resolution='i',width=1000000,height=400000,
            lon_0=31,lat_0=55,ax=ax)
m.drawcountries()
m.drawrivers()
x, y = m(lons, lats)
for xi, yi, city_name in zip(x, y, city_names):
    ax.annotate(text=city_name,xy=(xi, yi), fontsize=6)
plt.tight_layout()
plt.show()

# 繪製氣溫圖
tempertature_df = pd.read_sql('SELECT * FROM temperatures;', con=connection)
connection.close()
temp_celesius = (tempertature_df['temp'] * 5/4).values
lons = tempertature_df['lont'].values
fig, ax = plt.subplots()
ax.plot(lons,temp_celesius)
plt.tight_layout()
plt.show()

# 繪製軍隊圖
troops_df = pd.read_sql('SELECT * FROM troops;', con=connection)
connection.close()
rows = troops_df.shape[0]
lons = troops_df['lonp'].values
lats = troops_df['latp'].values
survivals = troops_df['surviv'].values
directions = troops_df['direc'].values
fig, ax = plt.subplots()
for i in range(rows-1):
    if directions[i] == 'A':
        line_color = 'tan'
    else:
        line_color = 'black'
    star_stop_lons = (lons[i], lons[i+1])
    star_stop_lats = (lats[i], lats[i+1])
    line_width = survivals[i] / 10000
    ax.plot(star_stop_lons, star_stop_lats, color=line_color, linewidth=line_width)
plt.tight_layout()
plt.show()