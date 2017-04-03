import json
import random
import string

import httplib2
import requests
from flask import Flask, render_template, request, url_for, flash, jsonify, \
    redirect, make_response, abort
from flask import session as login_session
from oauth2client.client import FlowExchangeError
from oauth2client.client import flow_from_clientsecrets

from database_setup import Category, Item, DBSession
from permissions import Permissions
from users import UserUtils

session = DBSession()

app = Flask(__name__)

# -----------------------------------------------------------------------------
# USERS, AUTHENTICATION, and AUTHORIZATION

CLIENT_ID = \
    json.loads(open('client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "Item Catalog"


@app.route(
    '/gconnect',
    methods=['POST'])
def gconnect():
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code
    code = request.data

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets(
            'client_secrets.json',
            scope='https://www.googleapis.com/auth/userinfo.profile')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print "Token's client ID does not match app's."
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id and \
                    'user_id' in login_session:
        return UserUtils.respond_with_preauthentication_url()

    # Store the access token in the session for later use.
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()
    print data

    # Add user data fields to the session dictionary
    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

    # Either create or retrieve the associated User
    # from the data store, by unique email
    user = UserUtils.try_get_user_by_email(data['email'])
    if not user:
        user = UserUtils.create_user(login_session)
    user_id = user.id
    login_session['user_id'] = user_id

    handle = UserUtils.get_user_handle()

    flash("you are now logged in as %s" % handle)
    print "done!"

    return UserUtils.respond_with_preauthentication_url()


# DISCONNECT - Revoke a current user's token and reset their login_session
@app.route(
    '/gdisconnect')
def gdisconnect():
    UserUtils.set_preauthentication_url()

    if 'access_token' not in login_session:
        return UserUtils.return_to_preauthentication_url()

    access_token = login_session['access_token']

    print 'In gdisconnect access token is %s', access_token
    print 'User name is: '
    print login_session['username']

    if access_token is None:
        print 'Access Token is None'
        response = make_response(
            json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % \
          login_session['access_token']
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]

    print 'result is '
    print result

    if result['status'] != '200':
        response = make_response(
            json.dumps('Failed to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response

    del login_session['access_token']
    del login_session['gplus_id']
    del login_session['username']
    del login_session['email']
    del login_session['picture']
    del login_session['user_id']

    # response = make_response(json.dumps('Successfully disconnected.'), 200)
    # response.headers['Content-Type'] = 'application/json'
    # return response

    return UserUtils.return_to_preauthentication_url()


@app.route(
    '/login')
def get_login_page():
    UserUtils.set_preauthentication_url()

    # Create anti-forgery state token
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for _ in range(32))

    login_session['state'] = state

    # return "The current session state is %s" % login_session['state']
    return render_template(
        'login.html',
        STATE=state)


# -----------------------------------------------------------------------------
# CATEGORY HTML ENDPOINTS

@app.route(
    '/categories/create',
    methods=['GET', 'POST'])
def create_category():
    if not UserUtils.is_authenticated():
        UserUtils.set_preauthentication_url()
        return redirect('/login')

    if request.method == 'POST':

        item = Category(
            name=request.form['name'])
        session.add(item)
        session.commit()

        flash('category created')

        return redirect(url_for(
            'get_category_by_id',
            category_id=item.id))
    else:
        return UserUtils.render_user_template(
            'category_create.html',
            page_title="New Category")


@app.route('/')
@app.route('/categories/')
def get_categories():
    items = session.query(Category).all()

    return UserUtils.render_user_template(
        'category_list.html',
        categories=items,
        page_title="Category List")


@app.route(
    '/categories/<int:category_id>/')
def get_category_by_id(category_id):
    category = session.query(Category).filter_by(id=category_id).one()

    items = session.query(Item).filter_by(category_id=category_id).all()

    return UserUtils.render_user_template(
        'category_items.html',
        category=category,
        items=items,
        page_title="%s Category" % category.name,
        can=Permissions.get_user_permissions_for_category(category))


@app.route(
    '/categories/<int:category_id>/update',
    methods=['GET', 'POST'])
def update_category_by_id(category_id):
    if not UserUtils.is_authenticated():
        UserUtils.set_preauthentication_url()
        return redirect('/login')

    category = session.query(Category).filter_by(id=category_id).one()

    if not Permissions.get_user_permissions_for_category(category).update:
        abort(403)

    if request.method == 'POST':
        category.name = request.form['name']
        session.add(category)
        session.commit()

        flash('category updated')

        return redirect(url_for(
            'get_category_by_id',
            category_id=category_id))
    else:
        return UserUtils.render_user_template(
            'category_update.html',
            category=category,
            page_title="%s %s Category" % ("Edit", category.name))


@app.route(
    '/categories/<int:category_id>/delete',
    methods=['GET', 'POST'])
def delete_category_by_id(category_id):
    if not UserUtils.is_authenticated():
        UserUtils.set_preauthentication_url()
        return redirect('/login')

    category = session.query(Category).filter_by(id=category_id).one()

    if not Permissions.get_user_permissions_for_category(category).delete:
        abort(403)

    if request.method == 'POST':
        session.delete(category)
        session.commit()

        flash('category deleted')

        return redirect(url_for(
            'get_categories'))
    else:
        return UserUtils.render_user_template(
            'category_delete.html',
            category=category,
            page_title="%s %s Category" % ("Delete", category.name))


# -----------------------------------------------------------------------------
# CATEGORY JSON ENDPOINTS

@app.route(
    '/api/categories/')
def api_get_categories():
    categories = session.query(Category).all()

    def serialize(c):
        return {
            'id': c.id,
            'user_id': c.user_id,
            'name': c.name,
            'items_url': url_for(
                'api_get_items_by_category_id', category_id=c.id)
        }

    return jsonify(
        categories=[serialize(category) for category in categories])


@app.route(
    '/api/categories/<int:category_id>/')
def api_get_category(category_id):
    category = \
        session.query(Category).filter_by(id=category_id).one()

    items = \
        session.query(Item).filter_by(category_id=category_id).all()

    def serialize_item(i):
        return {
            'id': i.id,
            'user_id': i.user_id,
            'category_id': i.category_id,
            'url': url_for(
                'api_get_item_by_id',
                category_id=i.category_id, item_id=i.id),
            'title': i.title,
            'description': i.description
        }

    items = [serialize_item(item) for item in items]

    def serialize(c):
        return {
            'id': c.id,
            'user_id': c.user_id,
            'name': c.name,
            'items': items
        }

    return jsonify(
        category=serialize(category))


# -----------------------------------------------------------------------------
# ITEM HTML ENDPOINTS

@app.route(
    '/categories/<int:category_id>/items/create',
    methods=['GET', 'POST'])
def create_item(category_id):
    if not UserUtils.is_authenticated():
        flash('login to create an item')
        UserUtils.set_preauthentication_url()
        return redirect('/login')

    if request.method == 'POST':

        item = Item(
            title=request.form['title'],
            description=request.form['description'],
            category_id=category_id,
            user_id=UserUtils.get_authenticated_user_id())
        session.add(item)
        session.commit()

        flash('item created')

        return redirect(url_for(
            'get_category_by_id',
            category_id=category_id))
    else:
        category = session.query(Category).filter_by(id=category_id).one()

        return UserUtils.render_user_template(
            'item_create.html',
            category=category,
            category_id=category_id)


@app.route(
    '/categories/<int:category_id>/items/<int:item_id>/')
def get_item_by_id(category_id, item_id):
    category = session.query(Category).filter_by(id=category_id).one()

    item = session.query(Item).filter_by(id=item_id).one()

    return UserUtils.render_user_template(
        'item_read.html',
        category=category,
        category_id=category_id,
        item=item,
        page_title="%s Item" % item.title,
        can=Permissions.get_user_permissions_for_item(item))


@app.route(
    '/categories/<int:category_id>/items/<int:item_id>/edit',
    methods=['GET', 'POST'])
def update_item_by_id(category_id, item_id):
    if not UserUtils.is_authenticated():
        UserUtils.set_preauthentication_url()
        return redirect('/login')

    item = session.query(Item).filter_by(id=item_id).one()

    # Users may update only items they created
    if not Permissions.get_user_permissions_for_item(item).update:
        flash('You may edit only items you created')
        abort(403)

    if request.method == 'POST':
        item.title = request.form['title']
        item.description = request.form['description']
        session.add(item)
        session.commit()

        flash('item updated')

        return redirect(url_for(
            'get_category_by_id',
            category_id=category_id))
    else:
        category = session.query(Category).filter_by(id=category_id).one()

        return UserUtils.render_user_template(
            'item_update.html',
            category=category,
            category_id=category_id,
            item=item,
            page_title="%s %s Item" % ("Edit", item.title))


@app.route(
    '/categories/<int:category_id>/items/<int:item_id>/delete',
    methods=['GET', 'POST'])
def delete_item_by_id(category_id, item_id):
    if not UserUtils.is_authenticated():
        UserUtils.set_preauthentication_url()
        return redirect('/login')

    item = session.query(Item).filter_by(id=item_id).one()

    # Users may delete only items they created
    if not Permissions.get_user_permissions_for_item(item).delete:
        flash('You may delete only items you created')
        abort(403)

    if request.method == 'POST':
        session.delete(item)
        session.commit()

        flash('item deleted')

        return redirect(url_for(
            'get_category_by_id',
            category_id=category_id))
    else:
        category = session.query(Category).filter_by(id=category_id).one()

        return UserUtils.render_user_template(
            'item_delete.html',
            category=category,
            category_id=category_id,
            item=item,
            page_title="%s %s Item" % ("Delete", item.title))


# -----------------------------------------------------------------------------
# ITEM JSON ENDPOINTS

@app.route(
    '/api/categories/<int:category_id>/items/')
def api_get_items_by_category_id(category_id):
    items = session.query(Item).filter_by(category_id=category_id).all()

    def serialize(i):
        return {
            'id': i.id,
            'url': url_for(
                'api_get_item_by_id',
                category_id=i.category_id,
                item_id=i.id),
            'user_id': i.user_id,
            'category_id': i.category_id,
            'title': i.title,
            'description': i.description
        }

    return jsonify(items=[serialize(item) for item in items])


@app.route(
    '/api/categories/<int:category_id>/items/<int:item_id>/')
def api_get_item_by_id(category_id, item_id):
    item = session.query(Item). \
        filter_by(category_id=category_id, id=item_id). \
        one()

    def serialize_item(i):
        return {
            'id': i.id,
            'user_id': i.user_id,
            'category_id': i.category_id,
            'category_url': url_for(
                'api_get_category',
                category_id=i.category_id),
            'title': i.title,
            'description': i.description
        }

    return jsonify(item=serialize_item(item))


# -----------------------------------------------------------------------------
# APPLICATION ENTRY POINT

if __name__ == '__main__':
    app.secret_key = 'my_super_secret_app_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
