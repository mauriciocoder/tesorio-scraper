import sys
from batch_setup import db

from scraper.github_scraper import GitHubScraper

def scrap_repositories(github_scraper):
    github_scraper.scrap_repositories_from_file()


if __name__ == '__main__':
    print('### Starting scraper job')
    print(f"Arguments count: {len(sys.argv)}")
    for i, arg in enumerate(sys.argv):
        if (i == 1):
            print(f'github username: {arg}')
        if (i == 2):
            print(f'github token: {arg}')
        if (i == 3):
            print(f'repositories csv file: {arg}')

    github_scraper = GitHubScraper(sys.argv[1], sys.argv[2], sys.argv[3])
    scrap_repositories(github_scraper)


    # admin = User(username='admin5', password='admin1')
    # db.session.add(admin)
    # db.session.commit()
    # print(User.query.all())


