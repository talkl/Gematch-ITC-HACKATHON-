import os
from bottle import (get, post, request, route, run, static_file, template, redirect, sys)
import utils
import sys

# Static Routes
@get("/js/<filepath:re:.*\.js>")
def js(filepath):
    return static_file(filepath, root="./js")


@get("/css/<filepath:re:.*\.css>")
def css(filepath):
    return static_file(filepath, root="./css")


@get("/images/<filepath:re:.*\.(jpg|png|gif|ico|svg)>")
def img(filepath):
    return static_file(filepath, root="./images")

@get("/sholom/<filepath:re:.*\.ttf>")
def fonts(filepath):
    return static_file(filepath, root="./sholom")


# Dynamic Routes
@get('/categories')
def categories():
    return utils.fetch_categories(request)


@get('/countries')
def countries():
    return utils.fetch_countries(request)


@get('/cities')
def cities():
    return utils.fetch_cities(request)


@get('/my_products')
def my_products():
    return utils.fetch_my_products(request)

@get('/algorithm')
def algorithm():
    return utils.handleAlgorithm(request)


@route('/')
def index():
    sectionData = None
    return utils.login_or_render(sectionData, 'home', '/', request)


@get('/view/thumbnail')
def get_thumbnail_information():
    id = int(request.query.get('id'))
    print(id)
    return utils.handleThumbnail(id)

@get('/search')
def search_page():
    sectionData = {'msg': ""}
    return utils.login_or_render(sectionData, 'search_page', '/search', request)

@post('/search')
def search():
    return utils.handleSearch(request)

@get('/add')
def add_product_page():
    sectionData = {'msg': ""}
    return utils.login_or_render(sectionData, 'add_product', '/add', request)

@post('/add')
def add_product():
    return utils.handleAdd(request)

@get('/add_alert')
def add_alert_page():
    sectionData = {'msg': ""}
    sectionData['next_url'] = '/add_alert'
    return utils.login_or_render(sectionData, 'add_alert', '/add_alert', request)

@post('/add_alert')
def add_alert():
    return utils.handleAddAlert(request)



@get('/add_contact')
def add_contact_page():
    sectionData = {'msg': ""}
    return utils.login_or_render(sectionData, 'add_contact', '/add_contact', request)

@post('/add_contact')
def add_contact():
    # implement adding the form into the database
    utils.handleAddContact(request)



@get('/register')
@post('/register')
def register():
    if request.method == 'POST':
        return utils.handleRegister(request)
    else:
        sectionTemplate = "./templates/register.tpl"
        requestedUrl = request.GET.get('next_url', '/')
        sectionData = {'next_url': requestedUrl, 'err_msg': ""}
        user_logged_in = utils.userIsLoggedIn(request)
        return template("./pages/index.html", version=utils.getVersion(), sectionTemplate=sectionTemplate,
                        sectionData=sectionData, logged_in=user_logged_in)

@get('/logout')
@post('/logout')
def logout():
    if request.method == 'GET':
        redirect('/register')
    elif request.method == 'POST':
        if utils.handleLogout(request):
            sectionTemplate = "./templates/loggedout.tpl"
            user_logged_in = utils.userIsLoggedIn(request)
            return template("./pages/index.html", version=utils.getVersion(), sectionTemplate=sectionTemplate,
                            sectionData=None, logged_in=user_logged_in)
        else:
            return {'msg': 'already logged out', 'LoggedIn': False}


@get('/login')
@post('/login')
def login():
    if request.method == 'POST':
        return utils.handleLogin(request)
    else:
        sectionTemplate = "./templates/login.tpl"
        requestedUrl = request.GET.get('next_url', '/')
        sectionData = {'next_url': requestedUrl, 'err_msg': ""}
        user_logged_in = utils.userIsLoggedIn(request)
        return template("./pages/index.html", version=utils.getVersion(), sectionTemplate=sectionTemplate,
                        sectionData=sectionData, logged_in=user_logged_in)


@get('/dashboard')
@post('/dashboard')
def dashboard():
    return utils.handleDashboard(request)


run(host='localhost', port=os.environ.get('PORT', 5000))
