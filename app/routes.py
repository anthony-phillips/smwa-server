from app import app
from flask import request

reading = 0

@app.route('/')
@app.route('/index')
def index():
   return "suh dawg!"

@app.route('/upload')
def upload():
   global reading
   reading = request.args.get('reading')
   print("set reading: {0}".format(reading))
   return ""

@app.route('/read')
def read():
   print("requested reading")
   return str(reading)