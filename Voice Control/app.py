from flask import Flask
from flask import render_template
from microphone_recognition import speech

app = Flask(__name__)


@app.route('/')
def root():
    return render_template('app.html', text="")


@app.route('/speech')
def begin_speech():
    text = speech()
    return render_template('app.html', text=text, command="TEST COMMAND")

