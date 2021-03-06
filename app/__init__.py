from flask import Flask
from flask_socketio import SocketIO

app = Flask(__name__)
app.config["SECRET_KEY"] = "Not very secretive."
socketio = SocketIO(app, debug=True)

from app import routes
