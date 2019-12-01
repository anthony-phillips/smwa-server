from app import app
import numpy as np
from scipy.integrate import trapz
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
   readings.append([float(reading), datetime.now().timestamp()])
   return ""

@app.route('/read/now')
def read_now():
   return str(readings)

@app.route('/analytics/consumption')
def analytics_consumption():
   consumption = trapz([reading[0] for reading in readings],
                       [reading[1] for reading in readings])
   return str(consumption / 3600) # 3600 WS in a WH

@app.route('/analytics/prediction')
def analytics_prediction():
   return str(readings)