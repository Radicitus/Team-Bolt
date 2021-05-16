import os
from flask import Flask
app = Flask(__name__)

@app.route('/command/<com>', methods=['POST'])
def run_command(com):
	ardSerialPath = "/home/pi/Desktop/Team-Bolt/OpenCat/serialMaster/ardSerial.py"
	os.system(ardSerialPath + " " +  str(com))
	return "The command [" + com + "] has been sent successfully."
