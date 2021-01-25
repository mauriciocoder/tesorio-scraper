import datetime

import requests

from .batch_setup import db
from model.github import Repository, User


def extract_attributes(result, attributes):
    """
    Extract attributes from result.
    :param result: HTTP GET result
    :param attributes: List of attributes to be extracted
    :return: Result only having attributes extracted
    """
    if attributes is None or len(attributes) == 0:
        return result
    if isinstance(result, dict):
        return {attr: result[attr] for attr in attributes}
    elif isinstance(result, list):
        new_result = []
        for r in result:
            if isinstance(r, dict):
                new_result.append({attr: r[attr] for attr in attributes})
        return new_result
    else:
        raise ValueError('Unsupported result set')


class Scraper:
    """Perform HTTP requests for scrapping"""

    def __init__(self, user, password):
        """
        Initialize scraper with api's user and password
        :param user:
        :param password:
        """
        self.auth = (user, password)

    def scrap(self, url, attributes):
        """
        Scrap the url and extract the results based on attributes provided
        :param url: Url to scrap data from
        :param attributes: List of attributes to be extracted
        :return:
        """
        result = requests.get(url, auth=self.auth).json()
        print(f'Result before extract attributes: {result}')
        return extract_attributes(result, attributes)

    def custom_get(self, url, meaning):
        result = requests.get(url, auth=self.auth).json()
        # print(f'r.request.headers: {result.request.headers}')
        print(f'{meaning}: {result}')


class GitHubScraper(Scraper):
    BASE_URL = 'https://api.github.com'
    REPO_ATTRIBUTES = ['id', 'name', 'full_name', 'description', 'language', 'html_url'
        , 'forks', 'created_at', 'updated_at']
    CONTRIBUTORS_ATTRIBUTES = ['login']
    USER_ATTRIBUTES = ['id', 'login', 'name', 'email', 'company', 'bio', 'location', 'html_url', 'public_repos'
        , 'public_gists', 'followers', 'following', 'created_at', 'updated_at']

    def __init__(self, user, password, repositories_file_name):
        super(GitHubScraper, self).__init__(user, password)
        self.repositories_file_name = repositories_file_name

    def print_rate_limit(self):
        self.custom_get(self.BASE_URL, 'Rate limit')

    def scrap_repo(self, owner, repo, attributes):
        print(f'Scrapping repo owned by {owner} with name {repo}...')
        result = self.scrap(f'{self.BASE_URL}/repos/{owner}/{repo}', attributes)
        print(f'Result: {result}')
        return result

    def scrap_contributors(self, owner, repo, attributes):
        print(f'Scrapping contributors from {repo}...')
        result = self.scrap(f'{self.BASE_URL}/repos/{owner}/{repo}/contributors', attributes)
        print(f'Result: {result}')
        return result

    def scrap_user(self, username, attributes):
        print(f'Scrapping user {username}...')
        result = self.scrap(f'{self.BASE_URL}/users/{username}', attributes)
        print(f'Result: {result}')
        return result

    @staticmethod
    def convert_str_to_datetime(obj):
        obj.created_at = datetime.datetime.strptime(obj.created_at, '%Y-%m-%dT%H:%M:%SZ')
        obj.updated_at = datetime.datetime.strptime(obj.updated_at, '%Y-%m-%dT%H:%M:%SZ')

    def scrap_repositories_from_file(self):
        print('$$$$$$$$ Reading repositories file...')
        lines = [line.strip() for line in open(self.repositories_file_name, 'r')]
        print('$$$$$$$$ Repositories file read.')
        print('$$$$$$$$ Checking API rate limit')
        self.print_rate_limit()
        if lines is not None:
            for i in range(1, len(lines)):
                # Starts in 1 to avoid the header
                owner = lines[i].split(',')[0]
                repo = lines[i].split(',')[1]
                result = self.scrap_repo(owner, repo, self.REPO_ATTRIBUTES)
                repository = Repository(**result)
                self.convert_str_to_datetime(repository)
                repository.contributors = []
                contributors_json = self.scrap_contributors(owner, repo, self.CONTRIBUTORS_ATTRIBUTES)
                if contributors_json is not None:
                    for contributor_json in contributors_json:
                        login = contributor_json['login']
                        user_json = self.scrap_user(login, self.USER_ATTRIBUTES)
                        user = User(**user_json)
                        self.convert_str_to_datetime(user)
                        repository.contributors.append(user)
                print(f'$$$$$$$$ Saving repository {repo} to db...')
                db.session.merge(repository)
                db.session.commit()
                print(f'$$$$$$$$ {repo} saved')
