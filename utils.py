import requests
import random
from bottle import (get, post, request, route, run,
                    static_file, template, redirect, response, HTTPResponse)
import json
import pymysql
import mimetypes
import hashlib
import uuid
import mimetypes
import find_cycles

connection = pymysql.connect(host='192.168.1.171', user='itc_root',
                              db='gematch', charset='utf8', cursorclass=pymysql.cursors.DictCursor)

#connection = pymysql.connect(host='127.0.0.1', port=3306, user='ITC',
#                             db='gematch', charset='utf8', cursorclass=pymysql.cursors.DictCursor)

def getVersion():
    return "0.0.1"


def is_url_image(url):
    mimetype, encoding = mimetypes.guess_type(url)
    return (mimetype and mimetype.startswith('image'))


def check_url(url):
    try:
        r = requests.head(url)
        return r.status_code == 200
    except:
        return False


def is_image_and_ready(url):
    return is_url_image(url) and check_url(url)


def escape_single_quote(text):
    if not text:
        return text
    result = """"""
    for char in text:
        if char == """'""":
            result += """\\"""
            result += char
        else:
            result += char
    return result


def fetch_categories(request):
        result = {}
        try:
                with connection.cursor() as cursor:
                        sql = 'SELECT category_id, category_name FROM gematch.categories'
                        cursor.execute(sql)
                        categories = cursor.fetchall()
                        result['categories'] = categories
                result['STATUS'] = 'SUCCESS'
                result['MSG'] = 'fetched categories'
                return HTTPResponse(status=200, body=result)
        except Exception as e:
                print(e)
                result['STATUS'] = 'ERROR'
                result['MSG'] = e
                return HTTPResponse(status=200, body=result)


def fetch_countries(request):
    result = {}
    try:
        with connection.cursor() as cursor:
            sql = 'SELECT country_id, country_name FROM gematch.countries'
            cursor.execute(sql)
            countries = cursor.fetchall()
            result['countries'] = countries
        result['STATUS'] = 'SUCCESS'
        result['MSG'] = 'fetched countries'
        return HTTPResponse(status=200, body=result)
    except Exception as e:
        print(e)
        result['STATUS'] = 'ERROR'
        result['MSG'] = e
        return HTTPResponse(status=200, body=result)


def fetch_my_products(request):
    result = {}
    try:
        with connection.cursor() as cursor:
                idFromCookie = int(request.get_cookie('user_id'))
                sql = 'SELECT item_id, title, images FROM gematch.items WHERE user_id={}'.format(idFromCookie)
                cursor.execute(sql)
                my_products = cursor.fetchall()
                result['my_products'] = my_products
        result['STATUS'] = 'SUCCESS'
        result['MSG'] = 'fetched products'
        return HTTPResponse(status=200, body=result)
    except Exception as e:
        print(e)
        result['STATUS'] = 'ERROR'
        result['MSG'] = e
        return HTTPResponse(status=200, body=result)


def fetch_cities(request):
    result = {}
    try:
        with connection.cursor() as cursor:
            sql = 'SELECT city_id, city_name FROM gematch.cities;'
            cursor.execute(sql)
            cities = cursor.fetchall()
            result['cities'] = cities
        result['STATUS'] = 'SUCCESS'
        result['MSG'] = 'fetched cities'
        return HTTPResponse(status=200, body=result)
    except Exception as e:
        print(e)
        result['STATUS'] = 'ERROR'
        result['MSG'] = e
        return HTTPResponse(status=200, body=result)


def handleAlgorithm(request):
        result = {}
        try:
                # implement JENN
                idFromCookie = int(request.get_cookie('user_id'))
                item_title_requested = request.query.get('item_requested')
                print(item_title_requested)
                result['matches'] = get_cycle_info(idFromCookie, item_title_requested)
                result['STATUS'] = 'SUCCESS'
                result['MSG'] = 'fetched cities'
                return HTTPResponse(status=200, body=result)
        except Exception as e:
                print(e)
                result['STATUS'] = 'ERROR'
                result['MSG'] = e
                return HTTPResponse(status=200, body=result)


def handleThumbnail(item_id):
        result = {}
        sectionData = {
                'title': None,
                'images': None,
                'description': None,
                'phone_number': None,
                'email': None,
                'city': None,
                'country': None
        }
        try:
                with connection.cursor() as cursor:
                        sql = "select title from items where item_id = {0};\
                        select images from items where item_id = {0};\
                        select description from items where item_id = {0};\
                        select phone_number from items join contact on items.user_id = contact.user_id where item_id = {0};\
                        select email from items join contact on items.user_id = contact.user_id where item_id = {0};\
                        select city from items join location on items.user_id = location.user_id where item_id = {0};\
                        select country from items join location on items.user_id = location.user_id where item_id = {0};".format(item_id)
                        for stmt in sql.split(';'):
                                if stmt.strip():
                                        stmt = stmt.strip()
                                        cursor.execute(stmt)
                                        row = cursor.fetchone()
                                        for key in row:
                                                sectionData[key] = row[key]
                sectionTemplate = "./templates/thumbnail.tpl"
                user_logged_in = userIsLoggedIn(request)
                return template("./pages/index.html", version=getVersion(), sectionTemplate=sectionTemplate,
                        sectionData=sectionData, logged_in=user_logged_in)

        except Exception as e:
                print(e)
                result['STATUS'] = 'ERROR'
                result['MSG'] = e
                return HTTPResponse(status=200, body=result)

def handleAdd(request):
        result = {}
        try:
                title = escape_single_quote(request.forms.get('title'))
                category = int(escape_single_quote(request.forms.get('category')))
                description = escape_single_quote(request.forms.get('description'))
                image = escape_single_quote(request.forms.get('image'))
                if not is_image_and_ready(image):
                        result['STATUS'] = 'ERROR'
                        result['MSG'] = 'image url is not a working valid image. check again please'
                        return HTTPResponse(status=200, body=result)
                if not all([title,category,description,image]):
                        result['STATUS'] = 'ERROR'
                        result['MSG'] = 'all fields are required'
                        return HTTPResponse(status=200, body=result)
                nicknameFromCookie = request.get_cookie('nickname')
                sessionFromCookie = request.get_cookie('session_id')
                idFromCookie = int(request.get_cookie('user_id'))
                with connection.cursor() as cursor:
                        sql = "INSERT INTO gematch.items(user_id, title, description, images, category_id) \
                        VALUES ({}, '{}', '{}', '{}', {})".format(idFromCookie, title, description, image, category)
                        cursor.execute(sql)
                        connection.commit()
                result['STATUS'] = 'SUCCESS'
                result['MSG'] = 'added successfully'
                return HTTPResponse(status=200, body=result)
        except Exception as e:
                print(e)
                result['STATUS'] = 'ERROR'
                result['MSG'] = e
                return HTTPResponse(status=200, body=result)


def handleSearch(request):
        result = {}
        try:
                user_input_text = request.forms.get('user_input')
                category_id = int(request.forms.get('category_filter'))
                city_id = int(request.forms.get('location_filter'))
                print(request.forms)
                if not user_input_text:
                        result['STATUS'] = 'ERROR'
                        result['MSG'] = 'please provide text before searching'
                        return HTTPResponse(status=200, body=result)
                idFromCookie = int(request.get_cookie('user_id'))
                result['items'] = get_items(idFromCookie, category_id, city_id, user_input_text)
                result['STATUS'] = 'SUCCESS'
                result['MSG'] = 'fetched items'
                return HTTPResponse(status=200, body=result)
        except Exception as e:
                print(e)
                result['STATUS'] = 'ERROR'
                result['MSG'] = e
                return HTTPResponse(status=200, body=result)


def handleUserProducts(request):
    """Get User Products"""
    result = {}
    try:
        nicknameFromCookie = request.get_cookie('nickname')
        sessionFromCookie = request.get_cookie('session_id')
        idFromCookie = int(request.get_cookie('user_id'))
        result['items'] = get_user_products(idFromCookie)
        result['STATUS'] = 'SUCCESS'
        result['MSG'] = 'fetched items'
        return HTTPResponse(status=200, body=result)
    except Exception as e:
        print(e)
        result['STATUS'] = 'ERROR'
        result['MSG'] = e
        return HTTPResponse(status=200, body=result)


def handleAddAlert(request):
    result = {}
    try:
        keyword = escape_single_quote(request.forms.get('keyword'))
        nicknameFromCookie = request.get_cookie('nickname')
        sessionFromCookie = request.get_cookie('session_id')
        idFromCookie = int(request.get_cookie('user_id'))
        prev_alert = get_user_alerts(idFromCookie)
        if prev_alert is None:
            with connection.cursor() as cursor:
                sql = "insert into request_items (user_id, keyword) \
                        VALUES ({}, '{}')".format(idFromCookie, keyword)
                cursor.execute(sql)
                connection.commit()
            result['STATUS'] = 'SUCCESS'
            result['MSG'] = 'added successfully'
            return HTTPResponse(status=200, body=result)
        else:
            alert_id = prev_alert['alert_id']
            with connection.cursor() as cursor:
                sql = "update request_items set keyword='{}' where alert_id = {}".format(keyword, alert_id)
                cursor.execute(sql)
                connection.commit()
            result['STATUS'] = 'SUCCESS'
            result['MSG'] = 'added successfully'
            return HTTPResponse(status=200, body=result)
    except Exception as e:
        print(e)
        result['STATUS'] = 'ERROR'
        result['MSG'] = e
        return HTTPResponse(status=200, body=result)


def handleDashboard(request):
    if userIsLoggedIn(request):
        idFromCookie = int(request.get_cookie('user_id'))
        result = get_user_details(idFromCookie)
        alert = get_user_alerts(idFromCookie)
        if alert is not None:
            result["alert_keyword"] = alert['keyword']
        else:
            result["alert_keyword"] = None
        products = get_user_products(idFromCookie)
        if products is None:
            result['products'] = None
        else:
            result['products'] = products
            print(products)
        return login_or_render(result, 'dashboard', '/dashboard', request)
    else:
        return redirect('./login?next_url={}'.format('/add_alert'))


def login_or_render(sectionData, templateName, next_url, request):
    if userIsLoggedIn(request) or (templateName in ('home', 'search_page')):
        sectionTemplate = "./templates/{}.tpl".format(templateName)
        user_logged_in = userIsLoggedIn(request)
        return template("./pages/index.html", version=getVersion(), sectionTemplate=sectionTemplate,
                        sectionData=sectionData, logged_in=user_logged_in)
    else:
        return redirect('./login?next_url={}'.format(next_url))

def handleLogin(request):
    nickname = request.forms.get('nickname')
    userPassword = request.forms.get('password')
    requestedUrl = request.forms.get('next_url')
    userVerified = verifyUser(nickname, userPassword)
    if userVerified:
        redirect(requestedUrl)
    else:
        context = {'next_url': requestedUrl, 'err_msg': "wrong username or password"}
        sectionTemplate = "./templates/login.tpl"
        return template("./pages/index.html", version=getVersion(), sectionTemplate=sectionTemplate,
                        sectionData=context, logged_in=False)

def verifyUser(nickname, userPassword):
    hashedPassword = hashPass(userPassword)
    with connection.cursor() as cursor:
        sql = "SELECT * FROM users WHERE nickname='{}' AND password='{}'".format(nickname, hashedPassword)
        cursor.execute(sql)
        result = cursor.fetchone()
        if result:
            updateUserSessionId(nickname, hashedPassword, result['user_id'])
            return True
        return False

def hashPass(password):
    secret_combination = 'tH777nf'
    return hashlib.md5((password + secret_combination).encode('utf-8')).hexdigest()

def updateUserSessionId(nickname, hashedPassword, userId):
    sessionId = str(uuid.uuid4().hex)[:8]
    with connection.cursor() as cursor:
        sql = "UPDATE users SET session_id='{}' WHERE nickname='{}' AND password='{}'".format(sessionId, nickname, hashedPassword)
        cursor.execute(sql)
        connection.commit()
    response.set_cookie('session_id', sessionId, max_age=900)
    response.set_cookie('user_id', str(userId))
    response.set_cookie('nickname', nickname)

def userIsLoggedIn(request):
    nicknameFromCookie = request.get_cookie('nickname')
    sessionFromCookie = request.get_cookie('session_id')
    with connection.cursor() as cursor:
        sql = "SELECT * FROM users WHERE nickname='{}' AND session_id='{}'".format(nicknameFromCookie, sessionFromCookie)
        cursor.execute(sql)
        result = cursor.fetchone()
        return result

def handleRegister(request):
        nickname = request.forms.get('nickname')
        userPassword = request.forms.get('password')
        userPassword2 = request.forms.get('password2')
        country_id = int(request.forms.get('country'))
        city_id = int(request.forms.get('city'))
        address = escape_single_quote(request.forms.get('address'))
        phone = escape_single_quote(request.forms.get('phone'))
        email = escape_single_quote(request.forms.get('email'))
        requestedUrl = request.forms.get('next_url')
        passwordOkResult, msg = validateData(nickname, userPassword, userPassword2)
        if passwordOkResult:
                try:
                        with connection.cursor() as cursor:
                                hashedPassword = hashPass(userPassword)
                                sql = 'INSERT INTO users (nickname, password) VALUES (%s,%s)'
                                cursor.execute(sql, (nickname, hashedPassword))
                                connection.commit()
                                user_id = cursor.lastrowid
                                sql = "INSERT INTO location (user_id, country, city, address) VALUES ({}, {}, {}, '{}')".format(user_id, country_id, city_id, address)
                                cursor.execute(sql)
                                connection.commit()
                                sql = "INSERT INTO contact (user_id, phone_number, email) VALUES ({}, '{}', '{}')".format(
                                    user_id, phone, email)
                                cursor.execute(sql)
                                connection.commit()
                except Exception as e:
                        print(e)
                        context = {'next_url': requestedUrl, 'err_msg': e}
                        user_logged_in = userIsLoggedIn(request)
                        sectionTemplate = "./templates/register.tpl"
                        return template("./pages/index.html", version=getVersion(), sectionTemplate=sectionTemplate,
                        sectionData=context, logged_in=user_logged_in)
                return redirect('/login?next_url={}'.format(requestedUrl), code=303)
        else:
                context = {'next_url': requestedUrl,
                        'err_msg': msg}
                sectionTemplate = "./templates/register.tpl"
                return template("./pages/index.html", version=getVersion(), sectionTemplate=sectionTemplate,
                                sectionData=context, logged_in=False)

def handleLogout(request):
        nicknameFromCookie = request.get_cookie('nickname')
        sessionFromCookie = request.get_cookie('session_id')
        with connection.cursor() as cursor:
                sql = "SELECT * FROM users WHERE nickname='{}' AND session_id='{}'".format(
                nicknameFromCookie, sessionFromCookie)
                cursor.execute(sql)
                result = cursor.fetchone()
                if not result:
                        return False
                else:
                        sql = "UPDATE users SET session_id=NULL WHERE nickname='{}'".format(nicknameFromCookie)
                        cursor.execute(sql)
                        connection.commit()
                        response.set_cookie('session_id', "")
                        return True

        

def validateData(nickname, password, passwordRepeated):
        sql = "SELECT * FROM users WHERE nickname='{}'".format(nickname)
        with connection.cursor() as cursor:
                cursor.execute(sql)
                r = cursor.fetchone()
                if r:
                        return False, 'nickname already exists'
        if len(nickname) > 15:
                return False, 'nickname must be no more than 15 characters'
        if len(password) < 8:
                return False, 'Password must be at least 8 characters'
        if len(password) > 15:
                return False, 'Password must be not more than 15 characters'
        if password != passwordRepeated:
                return False, 'password was not repeated correctly'
        return True, ''

def get_items(userId, categoryId, cityId, userInput):
        with connection.cursor() as cursor:
                # idFromCookie, category_id, city_id, user_input_text
                # sql = "select * from items where user_id <> {0} AND (title LIKE '%{1}%' OR description LIKE '%{1}%')".format(userId,userInput)
                sql_filter = "select items.user_id, item_id, title, description, images, category_id, city from items join location on items.user_id = location.user_id where items.user_id <> {0} and (city={1} and category_id = {2} AND (title LIKE '%{3}%'\
                 OR description LIKE ' % {3} % '));".format(userId, cityId, categoryId, userInput)
                cursor.execute(sql_filter)
                return cursor.fetchall()


def get_user_products(userID):
    with connection.cursor() as cursor:
        sql = "select * from items where user_id = {0}".format(userID)
        cursor.execute(sql)
        return cursor.fetchall()

def get_user_details(userID):
    result = {}
    with connection.cursor() as cursor:
        sql = """select phone_number, email, address, city_name, country_name
                    from contact
                    join location
                    on contact.user_id = location.user_id
                    join cities
                    on cities.city_id = location.city
                    join countries
                    on countries.country_id = location.country
                    where contact.user_id = {0}""".format(userID)
        cursor.execute(sql)
        r = cursor.fetchone()
        return r


def get_user_alerts(userID):
    with connection.cursor() as cursor:
        sql = "select alert_id, keyword from request_items where user_id = {0}".format(userID)
        cursor.execute(sql)
        return cursor.fetchone()

def get_cycle_info(user_id, wanted_item=None):
    user_cycle = find_cycles.main(user_id, wanted_item)
    """Get the info for displaying in the cycle given user, item_id"""
    results = list()
    for user in user_cycle:
        item_id = user[2]
        with connection.cursor() as cursor:
            sql = """select item_id, title, images, nickname, city_name 
                    from items join users on items.user_id = users.user_id  
                    join location on location.user_id = items.user_id
                    join cities on location.city = cities.city_id 
                    where items.item_id = {0}""".format(item_id)
            cursor.execute(sql)
            trade_info = cursor.fetchone()
            results.append(trade_info)
    return results
