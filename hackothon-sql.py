import pymysql

con = pymysql.connect(host='192.168.1.171', user='itc_root',
                             db='gematch', charset='utf8', cursorclass=pymysql.cursors.DictCursor)

cur = con.cursor()

user_table_query = """CREATE TABLE IF NOT EXISTS users (
                        user_id int auto_increment, 
                        nickname varchar(255) NOT NULL Unique, 
                        password varchar(255) NOT NULL, 
                        session_id varchar(255), 
                        primary key (user_id))"""

cur.execute(user_table_query)

location_table_query = r"""CREATE TABLE IF NOT EXISTS location (
                        user_id int NOT NULL, 
                        country int, 
                        city int, 
                        address varchar(255),  
                        primary key (user_id))"""
cur.execute(location_table_query)

contact_info_table_query = """CREATE TABLE IF NOT EXISTS contact (
                                user_id int NOT NULL, 
                                phone_number varchar(20), 
                                email varchar(255), 
                                primary key (phone_number))"""

cur.execute(contact_info_table_query)

items_table_query = """CREATE TABLE IF NOT EXISTS items_test (
                            user_id int NOT NULL, 
                            item_id int auto_increment, 
                            title varchar(255), 
                            description Text, 
                            images varchar(255), 
                            category_id int, 
                            primary key (item_id))"""

cur.execute(items_table_query)


categories_query = """CREATE TABLE IF NOT EXISTS categories (
                        category_id int auto_increment, 
                        category_name varchar(255), 
                        primary key (category_id))"""
cur.execute(categories_query)

categories_query = """CREATE TABLE IF NOT EXISTS countries (
                   country_id int auto_increment,
                   country_name varchar(255) NOT NULL Unique,
                   primary key (country_id))"""

cur.execute(categories_query)

categories_query = """CREATE TABLE IF NOT EXISTS cities (
        city_id int auto_increment, 
        city_name varchar(255) NOT NULL Unique, 
        primary key (city_id))"""

cur.execute(categories_query)

alert_query = """CREATE TABLE IF NOT EXISTS request_items (
        alert_id int auto_increment, 
        user_id int NOT NULL, 
        keyword varchar(255) NOT NULL,
        primary key (alert_id))"""

cur.execute(alert_query)

# auto_increment_query = "ALTER TABLE users MODIFY COLUMN user_id int auto_increment;"
# cur.execute(categories_query)
# auto_increment_query = "ALTER TABLE items MODIFY COLUMN item_id int auto_increment;"
# cur.execute(categories_query)
# auto_increment_query = "ALTER TABLE categories MODIFY COLUMN category_id int auto_increment;"
# cur.execute(categories_query)

#category_names = ['gadgets', 'clothing', 'religious_items', 'kitchenware', 'foodstuffs', 'books', 'DVDs']

#cur.execute("select * from categories")
#if len(cur.fetchall()) == 0:
#    for category_name in category_names:
#
#        cur.execute(f"INSERT INTO categories (category_name) VALUES (\'{category_name}\')")
con.commit()
con.close()