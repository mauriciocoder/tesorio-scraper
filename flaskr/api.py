import json

from flask import g, jsonify, abort, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import tuple_

from model.github import User
from . import create_app
from scraper import db

app = create_app()
db = SQLAlchemy(app)

# TODO: Create endpoints for both repository and users
# TODO: Document the methods
# TODO: Document the readme file
# TODO: Check why the application is loading twice
# TODO: Add pre commit hook
# TODO: Add test coverage tool
USER_FIELDS = 'id', 'login', 'name', 'email', 'company', 'bio', 'location', 'html_url', 'public_repos', 'public_gists', 'followers', 'following', \
              'created_at', 'updated_at', 'repositories.id', 'repositories.name'


@app.route('/user/<login>', methods=['GET'])
def get_user(login):
    user = db.session.query(User).filter_by(login=f"{login}").first()
    if user is None:
        abort(404, description="Resource not found")
    return jsonify(json.dumps(user.to_dict(only=USER_FIELDS)))


@app.route('/users', methods=['GET'])
def get_user_by_query():
    """
    Get users by query string
    :return:
    """
    query_params = normalize_query(request.args)
    filters = []
    if 'id' in query_params:
        filters.append(User.id == query_params['id'])
    if 'login' in query_params:
        filters.append(User.login == query_params['login'])
    if 'name' in query_params:
        filters.append(User.name == query_params['name'])
    if 'email' in query_params:
        filters.append(User.email == query_params['email'])
    if 'company' in query_params:
        filters.append(User.company == query_params['company'])
    if 'bio' in query_params:
        filters.append(User.bio == query_params['bio'])
    if 'location' in query_params:
        filters.append(User.location == query_params['location'])
    if 'html_url' in query_params:
        filters.append(User.html_url == query_params['html_url'])
    if 'public_repos' in query_params:
        filters.append(User.public_repos == query_params['public_repos'])
    if 'public_repos.gte' in query_params:
        filters.append(User.public_repos >= query_params['public_repos.gte'])
    if 'public_repos.lte' in query_params:
        filters.append(User.public_repos <= query_params['public_repos.lte'])
    if 'public_gists' in query_params:
        filters.append(User.public_gists == query_params['public_gists'])
    if 'public_gists.gte' in query_params:
        filters.append(User.public_gists >= query_params['public_gists.gte'])
    if 'public_gists.lte' in query_params:
        filters.append(User.public_gists <= query_params['public_gists.lte'])
    if 'followers' in query_params:
        filters.append(User.followers == query_params['followers'])
    if 'followers.gte' in query_params:
        filters.append(User.followers >= query_params['followers.gte'])
    if 'followers.lte' in query_params:
        filters.append(User.followers <= query_params['followers.lte'])
    if 'following' in query_params:
        filters.append(User.following == query_params['following'])
    if 'following.gte' in query_params:
        filters.append(User.following >= query_params['following.gte'])
    if 'following.lte' in query_params:
        filters.append(User.following <= query_params['following.lte'])
    if 'created_at' in query_params:
        filters.append(User.created_at == query_params['created_at'])
    if 'updated_at' in query_params:
        filters.append(User.updated_at == query_params['updated_at'])

    users = db.session.query(User).filter(
        *tuple(filters)
    ).all()
    print(f'users = {users}')
    if users is None:
        abort(404, description="Resource not found")
    users_list = [user.to_dict(only=USER_FIELDS) for user in users]
    print(f'users_list = {users_list}')
    return jsonify(users_list)

@app.route('/users/repo/<name>', methods=['GET'])
def get_users_by_repo_name(name):
    
"""
    select
    user. *
    from user
    inner
    join
    REPOSITORY_USER
    on
    REPOSITORY_USER.USER_ID = user.ID
    inner
    join
    REPOSITORY
    on
    REPOSITORY.ID = REPOSITORY_USER.REPOSITORY_ID
    where
    REPOSITORY.name = 'comunica'
"""


@app.errorhandler(404)
def resource_not_found(e):
    return jsonify(error=str(e)), 404


def normalize_query_param(value):
    """
    Given a non-flattened query parameter value,
    and if the value is a list only containing 1 item,
    then the value is flattened.

    :param value: a value from a query parameter
    :return: a normalized query parameter value
    """
    return value if len(value) > 1 else value[0]


def normalize_query(params):
    """
    Converts query parameters from only containing one value for each parameter,
    to include parameters with multiple values as lists.

    :param params: a flask query parameters data structure
    :return: a dict of normalized query parameters
    """
    params_non_flat = params.to_dict(flat=False)
    return {k: normalize_query_param(v) for k, v in params_non_flat.items()}
