from flask import Flask, redirect, url_for, flash
from flask import render_template
from microphone_recognition import speech
import requests

app = Flask(__name__)
app.secret_key = 'dev'

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
current_command = []

@app.route('/')
def root():
    return render_template('app.html', text="", commands=command_dict)


@app.route('/speech')
def begin_speech():
    text = speech()
    if text in command_dict:
        return render_template('app.html', text=text, commands=command_dict, command=command_dict[text])
    else:
        flash(text.capitalize() + " is not a valid command.")
        return redirect(url_for("root"))


@app.route('/begin-command/<command>')
def begin_command(command):
    comm_url = team_bolt_raspi_url + "/command/" + command_dict[command]
    try:
        response = requests.post(comm_url)
        flash("Command '" + command + "' sent successfully!")
        return redirect(url_for("root"))
    except:
        flash("Sending command '" + command + "' failed.")
        return redirect(url_for("root"))

