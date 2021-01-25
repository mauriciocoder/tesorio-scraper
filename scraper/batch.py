import sys
from batch_setup import db

from scraper.github_scraper import GitHubScraper

if __name__ == '__main__':
    """
    Entry point for tesorio scrapper job. The CLI command should have the following format:
    pipenv run python scraper/batch.py {github_username} {github_access_token} {repository_file_full_path}
    {github_username} - GitHub username for api authentication 
    {github_access_token} - GitHub access token for api authentication 
    {repository_file_full_path} - CSV file having the reposiory list for scrapping source
    """
    print('### Starting scraper job')
    arg_len = len(sys.argv)
    print(f"Arguments count: {arg_len}")
    if arg_len <= 1:
        raise ValueError('You should provide command line parameters in the order: [username, token, repository_file] ')
    username = token = repository_file = ''
    for i, arg in enumerate(sys.argv):
        if (i == 1):
            username = arg
            print(f'github username: {username}')
        if (i == 2):
            token = arg
            print(f'github token: {token}')
        if (i == 3):
            repository_file = arg
            print(f'repositories csv file: {repository_file}')
    github_scraper = GitHubScraper(username, token, repository_file).scrap_repositories_from_file()

