import sqlite3
import pandas as pd

class CreateMinardDB:
    def __init__(self):
        with open('data/minard.txt', 'r') as f:
            lines = f.readlines()
        self.lines = lines
        column_names = lines[2].split()
        patterns_to_be_removed = ['(', ')', '$', ',']
        adjusted_column_names = []
        for column_name in column_names:
            for pattern in patterns_to_be_removed:
                if pattern in column_name:
                    column_name = column_name.replace(pattern, '')
            adjusted_column_names.append(column_name)
        self.column_names_city = adjusted_column_names[:3]
        self.column_names_temperature = adjusted_column_names[3:7]
        self.column_names_troop = adjusted_column_names[7:]

    def create_city_dataframe(self):
        # 抓6-25列
        i = 6
        longitudes, latitudes, cities = [], [], []
        while i <= 25:
            long, lat, city = self.lines[i].split()[:3]
            longitudes.append(float(long))
            latitudes.append(float(lat))
            cities.append(city)
            i += 1
        city_data = (longitudes, latitudes, cities)
        city_df = pd.DataFrame()
        for column_name, data in zip(self.column_names_city, city_data):
            city_df[column_name] = data
        return city_df

    def create_temperature_dataframe(self):
        i = 6
        longitudes, temperatures, days, dates = [], [], [], []
        while i <= 14:
            lines_split = self.lines[i].split()
            longitudes.append(float(lines_split[3]))
            temperatures.append(int(lines_split[4]))
            days.append(int(lines_split[5]))
            if i == 10:
                dates.append('Nov 24')
            else:
                date_str = lines_split[6] + ' ' + lines_split[7]
                dates.append(date_str)
            i += 1
        temperature_data = (longitudes, temperatures, days, dates)
        temperature_df = pd.DataFrame()
        for column_name, data in zip(self.column_names_temperature, temperature_data):
            temperature_df[column_name] = data
        return temperature_df

    def create_troop_dataframe(self):
        i = 6
        longitudes, latitudes, survivals, directions, divisions = [], [], [], [], []
        while i <= 53:
            lines_split = self.lines[i].split()
            longitudes.append(float(lines_split[-5]))
            latitudes.append(float(lines_split[-4]))
            survivals.append(int(lines_split[-3]))
            directions.append(lines_split[-2])
            divisions.append(int(lines_split[-1]))
            i += 1
        troop_data = (longitudes, latitudes, survivals, directions, divisions)
        troop_df = pd.DataFrame()
        for column_name, data in zip(self.column_names_troop, troop_data):
            troop_df[column_name] = data
        return troop_df
   
    def create_database(self):
        connection = sqlite3.connect('data/minard.db')
        city_df = self.create_city_dataframe()
        temperature_df = self.create_temperature_dataframe()
        troop_df = self.create_troop_dataframe()
        df_dict = {'cities': city_df, 'temperatures': temperature_df, 'troops': troop_df}
        for k,v in df_dict.items():
            v.to_sql(name=k, con=connection, if_exists='replace', index=False)
        connection.close()
    
create_minard_db = CreateMinardDB()
create_minard_db.create_database()
