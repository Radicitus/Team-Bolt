from flask import Flask
from flask import render_template
from microphone_recognition import speech
import requests

app = Flask(__name__)

team_bolt_raspi_url = "http://team-bolt-raspi.local:5000"
command_dict = {
    "rest": "r",
    "walk forward": "kwkF",
    "walk forward left": "kwkL",
    "walk forward right": "kwkR",
    "walk backward": "kbk",
    "walk backward left": "kbkL",
    "walk backward right": "kbkR",
    "balance": "kbalance",
    "bound": "kbd",
    "down": "d",
}


@app.route('/')
def root():
    return render_template('app.html', text="")


@app.route('/speech')
def begin_speech():
    text = speech()
    if text in command_dict:
        comm_url = team_bolt_raspi_url + "/command/" + command_dict[text]
        response = requests.post(comm_url)
        print(response)
    return render_template('app.html', text=text, command="TEST COMMAND")
