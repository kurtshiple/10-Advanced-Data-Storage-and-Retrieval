import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, inspect, func, distinct

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
#engine = create_engine("sqlite:///Resources/hawaii.sqlite")
database_path = "/Users/kurtshiple/Desktop/catchup/resources/hawaii.sqlite"
engine = create_engine(f"sqlite:///{database_path}")
# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """Homework 10 Flask App"""
    return (
        f"Kurt's Flask App <br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        )

@app.route("/api/v1.0/precipitation")
def precipitation():
    results = session.query(Measurement.date, Measurement.prcp).all()

    data1 = []
    for date, prcp in results:
        dateprcpdict = {}
        dateprcpdict["date"] = date
        dateprcpdict["prcp"] = prcp
        data1.append(dateprcpdict)

    return jsonify(data1)

@app.route("/api/v1.0/stations")
def stations():
    results = session.query(Station.station).group_by(Station.station)

    data2 = []
    for station in results:
        stationdict = {}
        stationdict["station"] = station
        data2.append(stationdict)

    return jsonify(data2)

#Finding Date
from datetime import datetime, timedelta

data3 = engine.execute('SELECT MAX(date) FROM ' '"measurement"' '').fetchall() #last date
lastdateS = data3[0][0]

lastdateF = datetime.strptime(lastdateS, '%Y-%m-%d').date() #datetime
from dateutil.relativedelta import relativedelta
datepastyear = lastdateF - relativedelta(years=1)


@app.route("/api/v1.0/tobs")
def tobs():
    results = session.query(Measurement.date, Measurement.tobs).order_by(Measurement.date.asc()).filter((Measurement.date >= datepastyear))

    data4 = []
    for date, tobs in results:
        tobsdict = {}
        tobsdict["date"] = date
        tobsdict["tobs"] = tobs
        data4.append(tobsdict)

    return jsonify(data4)

if __name__ == '__main__':
    app.run(debug=True)
