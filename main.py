import os
import jinja2
from flask import Flask, request

TEMPLATE_DIR = os.path.join(os.path.dirname(__file__), 'templates')
JINJA_ENV = jinja2.Environment(loader=jinja2.FileSystemLoader(TEMPLATE_DIR), autoescape=True)

APP = Flask(__name__)
APP.config['DEBUG'] = True

@APP.route('/')
def index():
    template = JINJA_ENV.get_template('signup_form.html')
    return template.render()

@APP.route('/welcome', methods=['POST'])
def welcome():
    username = request.form['username']
    template = JINJA_ENV.get_template('welcome.html')
    return template.render(username)

@APP.route('/completion_check', methods=['POST'])
def completion_check():
    username = request.form['username']
    password = request.form['password']
    verify = request.form['verify']

    username_error = ''
    password_error = ''
    verify_error = ''

    if '' in (username, password, verify):
        template = JINJA_ENV.get_template('signup_form.html')
        
        if username == '':
            username_error = 'That is not a valid username'
            return template.render(username_error=username_error)

        elif password == '':
            password_error = 'That is not a valid password'
            return template.render(password_error=password_error)

        elif verify == '':
            verify_error = 'Please verify password'
            return template.render(verify_error=verify_error)

    else:
        return username_password_check(username, password, verify)

@APP.route('/username_password_check', methods=['POST'])
def username_password_check(username, password, verify):
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
        return template.render(password_error=password_error)

    elif password_length < min_length:
        password_error = 'That is not a valid password (Must be at least 3 characters)'
        return template.render(password_error=password_error)

    elif password_length > max_length:
        password_error = 'That is not a valid password (Cannot be more than 20 characters)'
        return template.render(password_error=password_error)

    else:
        return password_verify_check(username, password, verify)

@APP.route('/password_verify_check',  methods=['POST'])
def password_verify_check(username, password, verify):
    template = JINJA_ENV.get_template('signup_form.html')

    if password != verify:
        verify_error = 'Passwords do not match'
        return template.render(verify_error=verify_error)

APP.run()
