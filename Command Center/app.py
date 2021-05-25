from flask import Flask, redirect, url_for, flash, request
from flask import render_template
from microphone_recognition import speech
import requests

app = Flask(__name__)
app.secret_key = 'dev'

team_bolt_raspi_url = "http://team-bolt-raspi.local:5000"
command_dict = {
    "down": "d",
    "balance": "kbalance",
    "hi": "khi",
    "push-up": "kpu",
    "sit": "ksit",
    "butt up": "kbuttUp",
    "look up": "klu",
    "walk forward": "kwkF",
    "walk forward left": "kwkL",
    "walk forward right": "kwkR",
    "walk backward": "kbk",
    "walk backward left": "kbkL",
    "walk backward right": "kbkR",
    "bound": "kbd",
    "pause": "p",
    "tip toe": "kvt",
    "lie": "kly",
    "lifted": "klifted",
    "sleep [WIP]": "ksleep",
    "pee": "kpee",
}


@app.route('/')
def root():
    return render_template('app.html', text="", commands=command_dict)


@app.route('/speech')
def begin_speech():
    text = speech()
    if text in command_dict:
        return render_template('app.html', text=text, commands=command_dict, command=command_dict[text])
    else:
        flash("ERROR: " + text.capitalize() + " is not a valid command.")
        return redirect(url_for("root"))


@app.route('/begin-command/<command>')
def begin_command(command):
    comm_url = team_bolt_raspi_url + "/command/" + command_dict[command]
    # print(comm_url)
    try:
        response = requests.post(comm_url)
        flash("SUCCESS: Command '" + command + "' sent successfully!")
        return redirect(url_for("root"))
    except:
        flash("ERROR: Sending command '" + command + "' failed.")
        return redirect(url_for("root"))


@app.route('/text-command/')
def text_command():
    command = request.args.get('c')
    comm_url = team_bolt_raspi_url + "/command/" + command
    # print(comm_url)
    try:
        response = requests.post(comm_url)
        flash("SUCCESS: Command '" + command + "' sent successfully!")
        return redirect(url_for("root"))
    except:
        flash("ERROR: Sending command '" + command + "' failed.")
        return redirect(url_for("root"))
