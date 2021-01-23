from flask import g
from flask_sqlalchemy import SQLAlchemy

from model.github import User
from . import create_app
from scraper import db

app = create_app()
db = SQLAlchemy(app)
print(f'app.config = {app.config}')


@app.route('/user/<login>', methods=['GET'])
def get_user(login):
    # conn = db.get_connection()
    print(f'db = {db}')

    user_list = db.session.query(User).all()
    result = ''
    for user in user_list:
        result += f' {user.login}'

    return f'Login passed {login} result = {result}'
