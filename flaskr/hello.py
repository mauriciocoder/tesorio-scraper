from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_world():
    x = int('asdsa')
    return 'Hello, World! It works man!!! Hot!!!'