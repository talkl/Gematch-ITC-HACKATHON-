import pymysql
import pandas as pd
import numpy as np


con = pymysql.connect(host='192.168.1.171', user='itc_root',
                             db='gematch', charset='utf8', cursorclass=pymysql.cursors.DictCursor)

cur = con.cursor()

# csv_file = pd.read_csv('worldcities.csv')
# cities = np.unique(csv_file.iloc[:,0].values)
# countries = np.unique(csv_file.iloc[:,1].values)

# for country_name in countries:
# 	cur.execute(f"INSERT INTO countries (country_name) VALUES (\'{country_name}\')")


# for city_name in cities:
# 	try:
# 		cur.execute(f"INSERT INTO cities (city_name) VALUES (\'{city_name}\')")
# 		xcon.commit()
# 	except:
# 		print("fail")


for i in range(7):
	cur.execute(f"UPDATE location (user_id, city, country, address) VALUES ( \'{i+1}\', 638, 10125, \'{'weizmann ' + str(i)}\')")



con.commit()
con.close()