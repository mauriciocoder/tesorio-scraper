
# Tesorio Scraper 

     
        _____                     _         __                                
      /__   \___  ___  ___  _ __(_) ___   / _\ ___ _ __ __ _ _ __   ___ _ __ 
        / /\/ _ \/ __|/ _ \| '__| |/ _ \  \ \ / __| '__/ _` | '_ \ / _ \ '__|
       / / |  __/\__ \ (_) | |  | | (_) | _\ \ (__| | | (_| | |_) |  __/ |   
       \/   \___||___/\___/|_|  |_|\___/  \__/\___|_|  \__,_| .__/ \___|_|   
                                                            |_|   


Tesorio Scraper is a POC application to scrap repositories and users from GitHub. It is composed of two modules:

* **Batch** - GitHub Repositories and Users
  scraper. It calls external APIs and persists data in a database (SQLite). We are scraping the repositories and their contributors (Users).
* **API** - Endpoints exposing the entities scraped from a batch process.


## Dependencies

From Pipfile:

* `flask` Micro web framework for API. It is classified as a microframework because it does not require particular tools or libraries. It has no database abstraction layer, form validation, or any other components where pre-existing third-party libraries provide common functions.
* `requests` HTTP request handler. Used for GitHub API calls.
* `pytest` Python framework for unit testing.
* `requests-mock` HTTP request mock for GitHub API unit testing.
* `flask-sqlalchemy` Database ORM and abstraction for SQLite connection.
* `sqlalchemy-serializer` Serializer for ORM operations.

## Entities
Application class diagram:
<p align="center">
  <img src="https://i.ibb.co/ZcpTsp9/class-diagram.png" alt="Size Limit CLI" width="738">
</p>


## Usage

### Setup

Before running the batch or exposing the API, the application needs its dependencies installed, DDL script executed (migration) and the unit tests passed.


1. Install all dependencies:

    ```sh
    $ pipenv --rm install
   
   ✔ Successfully created virtual environment!
    Virtualenv location: /home/mauricio/.local/share/virtualenvs/tesorio-scraper-tjk25do1
    Installing dependencies from Pipfile.lock (12f2da)...
    ▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉ 27/27 — 00:00:06
    To activate this project's virtualenv, run pipenv shell.
    Alternatively, run a command inside the virtualenv with pipenv run.
    ```

2. Run unit tests. All should pass:

    ```sh
    $ pipenv run tests
   
   ...
   ======================== 8 passed, 9 warnings in 0.33s =========================
    ```
3. Run data migration (DDL):

    ```sh
    $ export FLASK_APP=flaskr
    $ pipenv run init_db
    
   Init the app.
   SQLAlchemy initialization completed
   Initialized the database.
    ```
You should now have the following SQLite file created:

* `./instance/db.sqlite` contains entities User and Repository created.


### Batch Run

The batch process is responsible for scraping GitHub data and persist both users and repositories. The batch receives as input the CSV file path having all the repositories that we would scrap data from. Example:

```sh
owner,repo
mauriciocoder,tesorio-scraper
bbc,REST-API-example
```



1. Run the following commands passing your GitHub user, token and csv_filepath (You can retrieve your access in  [GitHub-Tokens](https://github.com/settings/tokens)):

    ```sh
    $ export FLASK_APP=flaskr
    $ pipenv run batch {github_user} {github_token} {csv_filepath}
   
   ...
   $$$$$$$$ Saving repository bit-of-trust to db...
   $$$$$$$$ bit-of-trust saved
    ```

You should now have your entities persisted in the previously configured database:

* `./instance/db.sqlite` contains entities User and Repository created.

### API Service

Once the batch has completed its execution, we can then expose an API to retrieve user and repository data.



1. Run the following commands:

    ```sh
    $ export FLASK_APP=flaskr/api.py
    $ export FLASK_ENV=development
    $ pipenv run api
    ```

You should now have your endpoints exposed in the following default port:

* `http://127.0.0.1:5000/` 

## Endpoints

The REST API endpoints are described below.

### Get user by login

##### Request

`GET /user/<login>`

    curl 'http://127.0.0.1:5000/user/wschella'

##### Response

    HTTP/1.0 200 OK
    Content-Type: application/json
    
    {
      "bio": null, 
      "company": "@ZeusWPI ", 
      "created_at": "2014-10-31 09:42:37", 
      "email": null, 
      "followers": "15", 
      "following": "16", 
      "html_url": "https://github.com/wschella", 
      "id": 9478856, 
      "location": "Ghent", 
      "login": "wschella", 
      "name": "Wout Schellaert", 
      "public_gists": "0", 
      "public_repos": "40", 
      "repositories": [
        {
          "id": 107345960, 
          "name": "comunica"
        }
      ], 
      "updated_at": "2021-01-13 15:36:03"
    }


### Get users by query string
You can chain any attribute described in the User's data model in the query string. It will work as filtering by "AND". Also for numeric attributes (Ex. followers, following) you can set the QueryString parameter `followers.gte` or `followers.lte` for greater than or less than.

##### Request

`GET /users`

    curl 'http://127.0.0.1:5000/users?followers.gte=10&followers.lte=20&following.gte=10&following.lte=20'

##### Response

    HTTP/1.0 200 OK
    Content-Type: application/json
    
    [
        {
          "bio": null, 
          "company": null, 
          "created_at": "2011-03-22 16:34:18", 
          "email": null, 
          "followers": 12, 
          "following": 13, 
          "html_url": "https://github.com/danielbeeke", 
          "id": 684215, 
          "location": null, 
          "login": "danielbeeke", 
          "name": "Daniel Beeke", 
          "public_gists": 11, 
          "public_repos": 130, 
          "repositories": [
            {
              "id": 240760595, 
              "name": "uhtml"
            }
          ], 
          "updated_at": "2021-01-16 15:21:43"
        }, 
        {
          "bio": null, 
          "company": "@ZeusWPI ", 
          "created_at": "2014-10-31 09:42:37", 
          "email": "wout.schellaert@gmail.com", 
          "followers": 15, 
          "following": 16, 
          "html_url": "https://github.com/wschella", 
          "id": 9478856, 
          "location": "Ghent", 
          "login": "wschella", 
          "name": "Wout Schellaert", 
          "public_gists": 0, 
          "public_repos": 40, 
          "repositories": [
            {
              "id": 107345960, 
              "name": "comunica"
            }
          ], 
          "updated_at": "2021-01-13 15:36:03"
        }
      ]



### Get users by repository name
Get users that contribute to a certain repository. This method was created just to show the usage of native SQL queries instead of the ORM model.

##### Request

`GET /users/repo/<repo_name>`

    curl 'http://127.0.0.1:5000/users/repo/comunica'

##### Response

    HTTP/1.0 200 OK
    Content-Type: application/json
    
    [
        {
        "bio": "Semantic Web researcher and programming enthusiast", 
        "company": "IDLab \u2013 Ghent University \u2013 imec", 
        "created_at": "2010-10-15 06:24:04", 
        "email": null, 
        "followers": "127", 
        "following": "7", 
        "html_url": "https://github.com/rubensworks", 
        "id": 440384, 
        "location": "Ghent, Belgium", 
        "login": "rubensworks", 
        "name": "Ruben Taelman", 
        "public_gists": "15", 
        "public_repos": "173", 
        "repositories": [
          {
            "id": 107345960, 
            "name": "comunica"
          }
        ], 
        "updated_at": "2021-01-22 15:27:27"
      }, 
      {
        "bio": null, 
        "company": "IDLab - UGent - imec", 
        "created_at": "2013-02-01 09:50:16", 
        "email": null, 
        "followers": "17", 
        "following": "0", 
        "html_url": "https://github.com/joachimvh", 
        "id": 3447363, 
        "location": "Belgium", 
        "login": "joachimvh", 
        "name": "Joachim Van Herwegen", 
        "public_gists": "0", 
        "public_repos": "15", 
        "repositories": [
          {
            "id": 107345960, 
            "name": "comunica"
          }
        ], 
        "updated_at": "2021-01-22 15:27:25"
      }
    ]

### Get repository by name

##### Request

`GET /repo/<name>`

    curl 'http://127.0.0.1:5000/repo/comunica'

##### Response

    HTTP/1.1 200 OK
    Content-Type: application/json
    
        {
      "contributors": [
        {
          "id": 440384, 
          "login": "rubensworks"
        }, 
        {
          "id": 3447363, 
          "login": "joachimvh"
        }, 
        {
          "id": 9478856, 
          "login": "wschella"
        }, 
        {
          "id": 23040076, 
          "login": "greenkeeper[bot]"
        }, 
        {
          "id": 25180681, 
          "login": "renovate-bot"
        }, 
        {
          "id": 68223009, 
          "login": "FlorianFV"
        }, 
        {
          "id": 50518218, 
          "login": "stephaniech97"
        }, 
        {
          "id": 29139614, 
          "login": "renovate[bot]"
        }, 
        {
          "id": 17749076, 
          "login": "BCommeine"
        }, 
        {
          "id": 3322119, 
          "login": "jacoscaz"
        }, 
        {
          "id": 1032980, 
          "login": "mielvds"
        }, 
        {
          "id": 675313, 
          "login": "RubenVerborgh"
        }, 
        {
          "id": 18272282, 
          "login": "SanderVanhove"
        }, 
        {
          "id": 33571080, 
          "login": "simonvbrae"
        }, 
        {
          "id": 6189968, 
          "login": "brechtvdv"
        }, 
        {
          "id": 408412, 
          "login": "michielbdejong"
        }, 
        {
          "id": 36776018, 
          "login": "RobinDeBaets"
        }, 
        {
          "id": 15344753, 
          "login": "tbaccaer"
        }, 
        {
          "id": 4251, 
          "login": "Vinnl"
        }
      ], 
      "created_at": "2017-10-18 01:57:55", 
      "description": "\ud83d\udcec A knowledge graph querying framework for JavaScript", 
      "forks": 28, 
      "full_name": "comunica/comunica", 
      "html_url": "https://github.com/comunica/comunica", 
      "id": 107345960, 
      "language": "TypeScript", 
      "name": "comunica", 
      "updated_at": "2021-01-23 19:53:12"
    }
    
### Get repositories by query string
You can chain any attribute described in the Repository data model in the query string. It will work as filtering by "AND". Also for numeric attributes (Ex. followers, following) you can set the QueryString parameter `forks.gte` or `forks.lte` for greater than or less than.

##### Request

`GET /repos`

    curl 'http://127.0.0.1:5000/repos?language=JavaScript'

##### Response

    HTTP/1.1 200 OK
    Status: 200 OK
    Content-Type: application/json
    
    [
      {
        "contributors": [
          {
            "id": 85749, 
            "login": "WebReflection"
          }, 
          {
            "id": 684215, 
            "login": "danielbeeke"
          }
        ], 
        "created_at": "2020-02-15 17:45:33", 
        "description": "A micro HTML/SVG render", 
        "forks": 9, 
        "full_name": "WebReflection/uhtml", 
        "html_url": "https://github.com/WebReflection/uhtml", 
        "id": 240760595, 
        "language": "JavaScript", 
        "name": "uhtml", 
        "updated_at": "2021-01-22 16:40:19"
      }
    ]









