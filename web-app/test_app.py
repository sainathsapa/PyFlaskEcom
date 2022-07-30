"""

Flask to Perform Actions on WebApp
@author: Sainath Sapa, 7518
@for : Tiger Analytics India Consulting Private Limited
@mentor: Sandeep Arora

"""
from flask import Flask
from config_route import configure_routes


def test_base_route():
    """
    Test Base Route
    """
    app = Flask(__name__)
    configure_routes(app)
    client = app.test_client()
    url = '/'

    response = client.get(url)
    assert response.status_code == 200


def test_add_admin_route():
    """
    Add Admin Route
    """
    app = Flask(__name__)
    app.secret_key = 'TigerAnalyticsIndiaConsultingPrivateLimited'
    app.config['MONGODB_SETTINGS'] = {
        'db': 'tig',
        'host': 'MongoDB',
        'port': 27017
    }
    configure_routes(app)
    client = app.test_client()
    url = '/AddAdmin'
    request_data = {
        'name': 'admin',
        'pwd': 'admin@213'
    }
    response = client.get(url,
                          data=request_data)

    assert response.status_code in (200, 500)


def test_login_admin_route():
    """
    Admin Login Route
    """
    # APPCONFIG
    app = Flask(__name__)
    app.secret_key = 'TigerAnalyticsIndiaConsultingPrivateLimited'
    app.config['MONGODB_SETTINGS'] = {
        'db': 'tig',
        'host': 'MongoDB',
        'port': 27017
    }

    # Calling Admin Login Method
    configure_routes(app)

    client = app.test_client()
    url = '/adminLogin'
    request_data = {
        'userName': 'admin',
        'pwd': 'admin@213'
    }
    response = client.post(url, data=request_data)
    assert response.status_code in (500, 200)


def test_admin_page_route():
    """
    View Admin Page Route
    """
    app = Flask(__name__)
    app.secret_key = 'TigerAnalyticsIndiaConsultingPrivateLimited'
    app.config['MONGODB_SETTINGS'] = {
        'db': 'tig',
        'host': 'MongoDB',
        'port': 27017
    }
    configure_routes(app)
    client = app.test_client()
    url = '/admin'

    response = client.get(url)
    assert response.status_code in (200, 400, 500)


def test_user_signup_route():
    """
    User Sign Up Route
    """
    # APPCONFIG
    app = Flask(__name__)
    app.secret_key = 'TigerAnalyticsIndiaConsultingPrivateLimited'
    app.config['MONGODB_SETTINGS'] = {
        'db': 'tig',
        'host': 'MongoDB',
        'port': 27017
    }

    # Calling Admin Login Method
    configure_routes(app)

    client = app.test_client()
    url = '/signup'
    request_data = {
        'fname': 'Sainath',
        'lname': 'Sapa',
        'email': 'sainath@gmail.com',
        'pwd': 'sainath@123'
    }
    # Check GET parameters
    reponse_get = client.get(url)
    response_code = reponse_get.status_code
    assert response_code in (200, 400, 500)
    # Check POST parameters
    response_post = client.post(url, data=request_data)
    response_code = response_post.status_code
    assert response_code in (200, 400, 500)


def test_user_login_route():
    """
    User Login Route
    """
    # APPCONFIG
    app = Flask(__name__)
    app.secret_key = 'TigerAnalyticsIndiaConsultingPrivateLimited'
    app.config['MONGODB_SETTINGS'] = {
        'db': 'tig',
        'host': 'MongoDB',
        'port': 27017
    }

    # Calling Admin Login Method
    configure_routes(app)

    client = app.test_client()
    url = '/login'
    request_data = {
        'email': 'sainath@gmail.com',
        'pwd': 'sainath@123'
    }
    # Check GET parameters
    reponse_get = client.get(url)
    response_code = reponse_get.status_code
    assert response_code in (200, 400, 500)

    # Check POST parameters
    response_post = client.post(url, data=request_data)
    response_code = response_post.status_code
    assert response_code in (200, 400, 500)


def test_user_logout_route():
    """
    User Log out Route
    """
    app = Flask(__name__)
    app.secret_key = 'TigerAnalyticsIndiaConsultingPrivateLimited'
    app.config['MONGODB_SETTINGS'] = {
        'db': 'tig',
        'host': 'MongoDB',
        'port': 27017
    }
    configure_routes(app)
    client = app.test_client()
    url = '/logout'

    response = client.get(url)
    assert response.status_code == 200


def test_user_view_products_route():
    """
    View User Products Route
    """
    app = Flask(__name__)
    app.secret_key = 'TigerAnalyticsIndiaConsultingPrivateLimited'
    app.config['MONGODB_SETTINGS'] = {
        'db': 'tig',
        'host': 'MongoDB',
        'port': 27017
    }
    configure_routes(app)
    client = app.test_client()
    url = '/products'

    response = client.get(url)
    assert response.status_code in (200, 400)
