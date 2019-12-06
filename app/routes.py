from app import app
import numpy as np
from scipy.integrate import trapz
from scipy.stats import linregress
from flask import request, render_template
from datetime import datetime
import math
import json

readings = []

date_format = '%d%m%y%H%M%S'

@app.route('/')
@app.route('/index')
def index():
   return render_template('index.html')

@app.route('/upload')
def upload():
   reading = float(request.args.get('reading'))
   readings.append([reading if reading>375 else 0, datetime.now().timestamp()])
   return ""

@app.route('/read/now')
def read_now():
   now = readings[-1]
   now_date = datetime.fromtimestamp(now[1]).isoformat()
   return '{{"read":{0},"date":"{1}"}}'.format(now[0], now_date)

@app.route('/read')
def read_all():
   start = request.args.get('start')
   end = request.args.get('end')
   start_time = readings[0][1]
   end_time = math.inf
   if start:
      start_time = datetime.strptime(start, date_format).timestamp()
   if end:
      end_time = datetime.strptime(end, date_format).timestamp()
   interval = filter(lambda reading: start_time <= reading[1] <= end_time, readings)
   interval = list(interval)
   iter_reads = iter(interval)
   json_str = '{"readings":['
   if interval:
      now_date = datetime.fromtimestamp(interval[0][1]).isoformat()
      json_str += '{{"read":{0},"date":"{1}"}}'.format(interval[0][0], now_date)
      next(iter_reads)
      for reading in interval:
         now_date = datetime.fromtimestamp(reading[1]).isoformat()
         json_str += ',{{"read":{0},"date":"{1}"}}'.format(reading[0], now_date)
   json_str += ']}'
   return json_str

@app.route('/analytics/consumption')
def analytics_consumption():
   start = request.args.get('start')
   end = request.args.get('end')
   start_time = readings[0][1]
   end_time = math.inf
   if start:
      start_time = datetime.strptime(start, date_format).timestamp()
   if end:
      end_time = datetime.strptime(end, date_format).timestamp()
   interval = filter(lambda reading: start_time <= reading[1] <= end_time, readings)
   interval = list(interval)
   consumption = trapz([reading[0] for reading in interval],
                       [reading[1] for reading in interval])
   return str(consumption / 3600) # 3600 watt-seconds in a watt-hour

@app.route('/analytics/prediction')
def analytics_prediction():
   start = request.args.get('start')
   end = request.args.get('end')
   start_time = readings[0][1]
   if start:
      start_time = datetime.strptime(start, date_format).timestamp()
   end_time = datetime.strptime(end, date_format).timestamp()
   interval = filter(lambda reading: start_time <= reading[1] <= end_time, readings)
   interval = list(interval)
   m,b,r,p,e = linregress([reading[1] for reading in interval],
                          [reading[0] for reading in interval])
   def P(t):
      return m * t + b
   dx = end_time-start_time
   return str((P(start_time)*dx - (P(start_time)-P(end_time))*dx / 2)/3600)


@app.route('/demo')
def demo():
   return render_template('demo.html')