import pytest
from requests import HTTPError

import scraper.github_scraper as s
import tests.mock_results as mock


### Test extract_attributes function
def test_extract_attributes():
    result = s.extract_attributes({"keya": "valuea", "keyb": "valueb", "keyc": "valuec"}, None)
    assert result == {"keya": "valuea", "keyb": "valueb", "keyc": "valuec"}


def test_extract_attributes_from_dict():
    result = s.extract_attributes({"keya": "valuea", "keyb": "valueb", "keyc": "valuec"}, ['keya', 'keyb'])
    assert result == {"keya": "valuea", "keyb": "valueb"}


def test_extract_attributes_from_array():
    result = s.extract_attributes([{"keya": "valuea", "keyb": "valueb", "keyc": "valuec"},
                                   {"keya": "valuea", "keyb": "valueb", "keyc": "valuec"}], ['keya', 'keyb'])
    assert result == [{"keya": "valuea", "keyb": "valueb"}, {"keya": "valuea", "keyb": "valueb"}]


def test_extract_attributes_from_unsupported():
    with pytest.raises(ValueError):
        s.extract_attributes((1, 2, 3), ['test'])


### Test Scraper
def test_get_repo(requests_mock):
    owner = 'octocat'
    repo = 'hello-world'
    requests_mock.get(f'https://api.github.com/repos/{owner}/{repo}', json=mock.repo_json)

    obj = s.Scraper(None, None)
    result = obj.scrap(f'https://api.github.com/repos/{owner}/{repo}', ['id', 'node_id'])
    assert result == mock.repo_json_result


def test_get_contributors(requests_mock):
    owner = 'twigphp'
    repo = 'Twig'
    requests_mock.get(f'https://api.github.com/repos/{owner}/{repo}/contributors', json=mock.contributors_json)

    obj = s.Scraper(None, None)
    result = obj.scrap(f'https://api.github.com/repos/{owner}/{repo}/contributors', ['id', 'login'])

    assert result == mock.contributors_json_result


### Test GitHub scraper
def test_scrap_users(requests_mock):
    username = 'mauriciocoder'
    requests_mock.get(f'https://api.github.com/users/{username}', json=mock.user_json)
    obj = s.GitHubScraper(None, None, None)
    result = obj.scrap_user(username,
                            ['id', 'login', 'email', 'bio', 'location', 'public_repos', 'followers', 'created_at',
                              'updated_at'])
    assert result == mock.user_json_result


def test_scrap_contributors(requests_mock):
    owner = 'twigphp'
    repo = 'Twig'
    requests_mock.get(f'https://api.github.com/repos/{owner}/{repo}/contributors', json=mock.contributors_json)
    obj = s.GitHubScraper(None, None, None)
    result = obj.scrap_contributors(owner, repo,
                                    ['id', 'login'])
    assert result == mock.contributors_json_result
