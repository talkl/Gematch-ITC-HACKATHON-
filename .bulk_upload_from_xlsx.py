import pymysql
import pandas as pd


df = pd.read_excel('C:/ITC/Hackathon/itc-hackathon/Items.xlsx')

submissions = list()

for index, row in df.iterrows():
    submissions.append((row[0], row[1], row[2], row[3], row[4], row[5]))

con = pymysql.connect(host='192.168.1.171', user='itc_root',
                             db='gematch', charset='utf8', cursorclass=pymysql.cursors.DictCursor)

cur = con.cursor()

cur.executemany(
      """INSERT INTO items (user_id, item_id, title, description, images, category_id)
      VALUES (%s, %s, %s, %s, %s, %s)""", submissions)

con.commit()
con.close()
