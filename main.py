import os
import jinja2
from flask import Flask, request

TEMPLATE_DIR = os.path.join(os.path.dirname(__file__), 'templates')
JINJA_ENV = jinja2.Environment(loader=jinja2.FileSystemLoader(TEMPLATE_DIR), autoescape=True)

APP = Flask(__name__)
APP.config['DEBUG'] = False

@APP.route('/')
def index():
    template = JINJA_ENV.get_template('signup_form.html')
    return template.render()

@APP.route('/welcome', methods=['POST'])
def welcome(username):
    template = JINJA_ENV.get_template('welcome.html')
    return template.render(username=username)

@APP.route('/completion_check', methods=['POST'])
def completion_check():
    username = request.form['username']
    password = request.form['password']
    verify = request.form['verify']
    email = request.form['email']

    username_error = ''
    password_error = ''
    verify_error = ''

    if '' in (username, password, verify):
        template = JINJA_ENV.get_template('signup_form.html')
        
        if username == '':
            username_error = 'That is not a valid username'
            return template.render(username_error=username_error, email=email)

        elif password == '':
            password_error = 'That is not a valid password'
            return template.render(username=username, password_error=password_error, email=email)

        elif verify == '':
            verify_error = 'Please verify password'
            return template.render(username=username, verify_error=verify_error, email=email)

    else:
        return username_password_check(username, password, verify, email)

@APP.route('/username_password_check', methods=['POST'])
def username_password_check(username, password, verify, email):
    template = JINJA_ENV.get_template('signup_form.html')
    min_length = 3
    max_length = 20

    username_length = len(username)
    password_length = len(password)

    username_error = ''
    password_error = ''

    if ' ' in username:
        username_error = 'That is not a valid username (Space not allowed)'
        return template.render(username_error=username_error)

    elif username_length < min_length:
        username_error = 'That is not a valid username (Must be at least 3 characters)'
        return template.render(username_error=username_error)

    elif username_length > max_length:
        username_error = 'That is not a valid username (Cannot be more than 20 characters)'
        return template.render(username_error=username_error)

    elif ' ' in password:
        password_error = 'That is not a valid password (Space not allowed)'
        return template.render(username=username, password_error=password_error, email=email)

    elif password_length < min_length:
        password_error = 'That is not a valid password (Must be at least 3 characters)'
        return template.render(username=username, password_error=password_error, email=email)

    elif password_length > max_length:
        password_error = 'That is not a valid password (Cannot be more than 20 characters)'
        return template.render(username=username, password_error=password_error, email=email)

    else:
        return password_verify_check(username, password, verify, email)

@APP.route('/password_verify_check',  methods=['POST'])
def password_verify_check(username, password, verify, email):
    template = JINJA_ENV.get_template('signup_form.html')

    if password != verify:
        verify_error = 'Passwords do not match'
        return template.render(username=username, verify_error=verify_error, email=email)

    else:
        return email_check(username, password, verify, email)

@APP.route('/email_check', methods=['POST'])
def email_check(username, password, verify, email):
    template = JINJA_ENV.get_template('signup_form.html')

    email = request.form['email']
    email_length = len(email)

    email_error = ''

    if ' ' in email:
        email_error = 'That is not a valid email address (Space not allowed)'
        return template.render(username=username, email_error=email_error)

    elif '@' not in email:
        email_error = 'That is not a valid email address (Missing @ character)'
        return template.render(username=username, email_error=email_error)

    elif '.' not in email:
        email_error = 'That is not a valid email address (Missing . character)'
        return template.render(username=username, email_error=email_error)

    elif email_length < 3:
        email_error = 'That is not a valid email address (Address cannot be less than 3 characters)'
        return template.render(username=username, email_error=email_error)

    elif email_length > 20:
        email_error = 'That is not a valid email address (Address cannot be more than 20 characters)'
        return template.render(username=username, email_error=email_error)

    else:
        return welcome(username)

APP.run()
