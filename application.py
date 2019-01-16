import os
import sys
import datetime

from flask import Flask, render_template, request, jsonify, redirect
from flask_socketio import SocketIO, emit

rooms = {}

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
socketio = SocketIO(app)


@app.route("/")
def index():
    """ Returns index page """
    return render_template("index.html", rooms=rooms)

@app.route("/displayname")
def displayname():
    """ Returns displayname page """
    return render_template("displayname.html", notloggedin=True)


@app.route("/chat/<room>")
def chat(room):
    """"Returns chat log of specified room"""

    # Zips the users and messages together, so they can be iterated over
    content = zip(rooms[room]['users'], rooms[room]['messages'], rooms[room]['times'])

    # Then returns the page with that zipped content
    return render_template("chat.html", content=content, room=room)

@app.route("/newchat", methods=["POST"])
def newchat():

    # Get new chat name and make sure it isn't already used
    newChatName = request.form.get("newChatName")
    if newChatName in rooms:
        return jsonify({"success": False})

    else:
        # Initialize new dictionary to go inside the new room
        tempdict = {"users": [], "messages": [], "times": []}

        # Put new chat in rooms
        rooms[newChatName] = tempdict

        # Returns success
        return jsonify({"success": True})

@socketio.on('new message')
def message(data):
    user = data['user']
    message = data['message']
    room = data['room']

    currentTime = datetime.datetime.now()

    time = currentTime.strftime("%H:%M:%S")

    rooms[room]['users'].append(user)
    rooms[room]['messages'].append(message)
    rooms[room]['times'].append(time)

    if len(rooms[room]['users']) > 100 or len(rooms[room]['messages']) > 100:
        print(rooms[room]['messages'][0], file=sys.stderr)
        del rooms[room]['users'][0]
        del rooms[room]['messages'][0]
        del rooms[room]['times'][0]
        print(rooms[room]['messages'][0], file=sys.stderr)

    emit('display message', {'user': user, 'message': message, 'time': time}, broadcast=True)


if __name__ == "__main__":
    socketio.run(app)
