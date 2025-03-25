import sqlite3
import pandas as pd
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt

connection = sqlite3.connect('data/minard.db')
city_df = pd.read_sql('SELECT * FROM cities;', con=connection)
tempertature_df = pd.read_sql('SELECT * FROM temperatures;', con=connection)
troops_df = pd.read_sql('SELECT * FROM troops;', con=connection)
connection.close()

# 城市經資料
loncs = city_df['lonc'].values
latcs = city_df['latc'].values
city_names = city_df['city'].values

# 軍隊路線資料
rows = troops_df.shape[0]
lonps = troops_df['lonp'].values
latps = troops_df['latp'].values
survivals = troops_df['surviv'].values
directions = troops_df['direc'].values

# 氣溫資料
temp_celsius = (tempertature_df['temp'] * 5/4).astype(int)
lonts = tempertature_df['lont'].values

plt.style.use('seaborn-v0_8')
fig, axes = plt.subplots(nrows=2, figsize=(16, 7),gridspec_kw={'height_ratios': [4, 1]})

# 繪製底圖
m = Basemap(projection='lcc',resolution='i',width=1000000,height=400000,
            lon_0=31,lat_0=55,ax=axes[0])
m.drawcountries()
m.drawrivers()
m.drawparallels(range(54,58),labels=[True,False,False,False])
m.drawmeridians(range(23,56,2),labels=[False,False,False,True])

# 顯示城市名稱
x, y = m(loncs, latcs)
for xi, yi, city_name in zip(x, y, city_names):
    axes[0].annotate(text=city_name,xy=(xi, yi), fontsize=12, zorder=2)

# 軍隊路線，一組經緯度畫一段線段
x, y = m(lonps, latps)
for i in range(rows-1):
    if directions[i] == 'A': # directions == attack
        line_color = 'tan'
    else: # directions == retreat
        line_color = 'black'
    star_stop_lons = (x[i], x[i+1])
    star_stop_lats = (y[i], y[i+1])
    line_width = survivals[i] / 10000 # 寬度表示人數
    m.plot(star_stop_lons, star_stop_lats, color=line_color, linewidth=line_width,zorder=1)

# axes[1]繪製氣溫折線圖
annotations = temp_celsius.astype(str).str.cat(tempertature_df['date'], sep='°C ')
axes[1].plot(lonts,temp_celsius) #,linestyle='dashed',color='b'
for lont, temp_c, annotation in zip(lonts, temp_celsius, annotations):
    axes[1].annotate(text=annotation,xy=(lont-.3, temp_c-7), fontsize=12)

# 軸物件顯示設定
axes[1].set_ylim(-50, 10)
axes[1].spines['top'].set_visible(False)
axes[1].spines['bottom'].set_visible(False)
axes[1].spines['right'].set_visible(False)
axes[1].spines['left'].set_visible(False)
axes[1].grid(True, which='major',axis='both')
axes[1].set_xticklabels([])
axes[1].set_yticklabels([])
axes[0].set_title("Napoleon's disastrous Russian campaign of 1812", loc='left', fontsize=20)
plt.tight_layout()
plt.show()
fig.savefig('minard_clone.png')