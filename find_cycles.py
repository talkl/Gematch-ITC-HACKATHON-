
import pymysql


class User:
    def __init__(self, user_id, wants, offers):
        self.id = user_id
        self.wants = wants
        self.offers = offers


class Graph:
    def __init__(self):
        self.connections = []

    def add_connection(self, from_id, to_id):
        self.connections.append((from_id, to_id))


def dfs(current_user, graph1, path1, cycles):

    bottom_of_path = path1[-1]
    for offer in bottom_of_path.offers:
        if offer == current_user.wants:
            #print(f'found closed cycle for {current_user.id}')
            cycle = [item.id for item in path1]
            #print(cycle)
            cycles[current_user.id] = cycle
            #print(cycles)
            return path1

    for connection in graph1.connections:
        if connection[0].id == bottom_of_path.id:
            temp = path1.copy()
            temp.append(connection[1])
            dfs(current_user, graph1, temp, cycles)



def main(user_id, title_wanted=None):

    #Add user items/requests from SQL:

    con = pymysql.connect(host='192.168.1.171', user='itc_root',
                          db='gematch', charset='utf8', cursorclass=pymysql.cursors.DictCursor)
    cur = con.cursor()

    cur.execute("""SELECT user_id, title from items;""")
    items_list = cur.fetchall()
    cur.execute("""SELECT user_id, keyword from request_items;""")
    requests_list = cur.fetchall()

    user_items = dict()
    user_want_items = dict()

    for item in items_list:
        if item['user_id'] not in user_items.keys():
            user_items[item['user_id']] = [item['title']]
        else:
            user_items[item['user_id']].append(item['title'])

    for item in requests_list:
        user_want_items[item['user_id']] = item['keyword']

    if title_wanted is not None:
        user_want_items[user_id] = title_wanted

    print(user_items)
    print(user_want_items)

    users = []

    for key in user_want_items.keys():
        users.append(User(user_id=key, wants=user_want_items[key], offers=user_items[key]))

    #making the graph
    graph1 = Graph()
    for user1 in users:
        for user2 in users:
            for offer in user1.offers:
                if offer == user2.wants:
                    graph1.add_connection(user1, user2)

    for c in graph1.connections:
        print(c[0].id, c[1].id)
    #dfs for each user

    cycles = dict()

    for user in users:
        user_path = [user]
        dfs(user, graph1, user_path, cycles)

    print(cycles)

    cycles_words = dict()

    # print(cycles[user_id])

    cur.execute("""SELECT items.user_id, items.item_id, items.title from request_items
    join items on request_items.keyword = items.title;""")

    item_id_list = cur.fetchall()

    # print(item_id_list)

    final_list = list()

    if cycles.get(user_id, None) is None:
        return final_list

    for item in cycles[user_id]:

        for a in item_id_list:
            if a['title'].lower() == user_want_items[item].lower():
                item_id = a['item_id']

        final_list.append((item, user_want_items[item], item_id))

    return final_list

# print(main(9, 'T-Shirts'))