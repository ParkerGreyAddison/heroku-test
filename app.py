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
from app import app, socketio

if __name__ == '__main__':
    socketio.run(app, debug=True)
