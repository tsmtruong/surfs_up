# importing dependencies
import datetime as dt
from unittest import result
from bs4 import ResultSet
import numpy as np
import pandas as pd
from pkg_resources import resource_string

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect

from flask import Flask, jsonify
from sympy import fu, python, stationary_points

# set up database
engine = create_engine("sqlite:///hawaii.sqlite")

inspector = inspect(engine)
print(inspector.get_table_names())
Base = automap_base()

# reflect database
Base.prepare(engine, reflect=True)


# references
Measurement = Base.classes.measurement
Station = Base.classes.station

# session link
session = Session(engine)

#set up flask
app = Flask(__name__)

# define welcome route
@app.route("/")

def welcome():
    return(
    '''
    Welcome to the Climate Analysis API! <br/>
    Available Routes: <br/>
    /api/v1.0/precipitation <br/>
    /api/v1.0/stations <br/>
    /api/v1.0/tobs <br/>
    /api/v1.0/temp/start/end
    ''')

# precipitation route
@app.route("/api/v1.0/precipitation")

# create function
def precipitation():
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    precipitation = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= prev_year).all()
    precip = {date: prcp for date, prcp in precipitation}
    return jsonify(precip)

# station route
@app.route("/api/v1.0/stations")

# create fuction
def stations():
    results = session.query(Station.station).all()
    stations = list(np.ravel(results))
    return jsonify(stations = stations)

# temperature route
@app.route("/api/v1.0/tobs")

# create function
def temp_monthly():
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    results = session.query(Measurement.tobs).\
        filter(Measurement.station =='USC00519281').\
        filter(Measurement.date >= prev_year).all()
    temps = list(np.ravel(results))
    return jsonify(temps = temps)

# statistics route
@app.route("/api/v1.0/temp/<start>")
@app.route("/api/v1.0/temp/<start>/<end>")

# create stats function
def stats(start = None, end = None):
    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]

    if not end:
        results = session.query(*sel).\
            filter(Measurement.date >= start).all()
        temps = list(np.ravel(results))
        return jsonify(temps)

    results = session.query(*sel).\
        filter(Measurement.date >= start).\
        filter(Measurement.date <= end).all()
    temps = list(np.ravel(results))
    return jsonify(temps)

