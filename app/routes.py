from app import app
from flask import request
from datetime import datetime

readings = []

@app.route('/')
@app.route('/index')
def index():
   return "suh dawg!"

@app.route('/upload')
def upload():
   reading = request.args.get('reading')
   readings.append({reading, datetime.now().isoformat()})
   print("set reading: {0}".format(reading))
   return ""

@app.route('/read')
def read():
   print("requested readings")
   return str(readings)