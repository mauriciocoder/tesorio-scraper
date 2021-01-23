import json

from flask import g, jsonify, abort
from flask_sqlalchemy import SQLAlchemy

from model.github import User
from . import create_app
from scraper import db

app = create_app()
db = SQLAlchemy(app)


# TODO: Make sure batch is populating all fields from data model
# TODO: Create more fields in the api to return user
# TODO: Create endpoints for both repository and users
# TODO: Document the readme file
# TODO: Check why the application is loading twice

@app.route('/user/<login>', methods=['GET'])
def get_user(login):
    user = db.session.query(User).filter_by(login=f"{login}").first()
    if user is None:
        abort(404, description="Resource not found")
    fields = 'id', 'login', 'repositories.id', 'repositories.name'
    return json.dumps(user.to_dict(only=fields))


@app.errorhandler(404)
def resource_not_found(e):
    return jsonify(error=str(e)), 404
