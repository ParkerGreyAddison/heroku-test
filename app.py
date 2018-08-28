##from flask import Flask
##
##app = Flask(__name__)
##
##@app.route('/')
##def index():
##    return 'Hello, working!'
##
##if __name__ == '__main__':
##    app.run()
from app import app

if __name__ == '__main__':
    app.run()
