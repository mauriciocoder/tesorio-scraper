# Setup SQLAlchemy and fix sys path for command line execution
import sys

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from pathlib import Path
sys.path.append(str(Path('.').absolute()))

welcome = """
 _____                     _         __                                
/__   \___  ___  ___  _ __(_) ___   / _\ ___ _ __ __ _ _ __   ___ _ __ 
  / /\/ _ \/ __|/ _ \| '__| |/ _ \  \ \ / __| '__/ _` | '_ \ / _ \ '__|
 / / |  __/\__ \ (_) | |  | | (_) | _\ \ (__| | | (_| | |_) |  __/ |   
 \/   \___||___/\___/|_|  |_|\___/  \__/\___|_|  \__,_| .__/ \___|_|   
                                                      |_|              
"""
print(welcome)
print(f'Your system version: {sys.version}')
print(f'Your sys.path: {sys.path}')
print(f'##### Initializing SQLAlchemy')

app = Flask(__name__)
db_file = 'sqlite:////home/mauricio/dev/project/python/tesorio-scraper/instance/db.sqlite'
app.config['SQLALCHEMY_DATABASE_URI'] = db_file
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
print(f'SQLALCHEMY_DATABASE_URI: {db_file}')
db = SQLAlchemy(app)
app.app_context().push()
print(f'SQLAlchemy initialization completed')
