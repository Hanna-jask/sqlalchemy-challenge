# Import the dependencies.

from flask import Flask, jsonify
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt
import numpy as np
#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///C:/Users/hanna/OneDrive/Documents/GitHub/sqlalchemy-challenge/SurfsUp/Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)
Base.classes.keys()
# Save references to each tablepip
measurement = Base.classes.measurement
station = Base.classes.station


# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)



#################################################
# Flask Routes
#################################################

#1
@app.route("/")
def welcome():
    return (
        f"Welcome to the Homepage<br>"
        f"Routes:<br>"
        f"/api/v1.0/precipitation<br>"
        f"/api/v1.0/stations<br>"
        f"/api/v1.0/tobs<br>"
        f"/api/v1.0/<start><br>"
        f"/api/v1.0/<start>/<end><br>"
     )

#2
@app.route("/api/v1.0/precipitation")
def precipitation():
        year_before = dt.date(2017,8,23)- dt.timedelta(days=365)
        scores = session.query(measurement.date, measurement.prcp).filter(measurement.date >= year_before).all()
        scores_dict = dict(scores)
        session.close()
        return jsonify(scores_dict)

#3
@app.route("/api/v1.0/stations")
def stations():
        stations = session.query(measurement.station, func.count(measurement.id)).\
                group_by(measurement.station).order_by(func.count(measurement.id).desc()).all()
        stations_dict = dict(stations)
        session.close()
        return jsonify(stations_dict)

#4
@app.route("/api/v1.0/tobs")
def stations():
        s_USC00519281 = session.query(measurement.station, measurement.tobs)\
                .filter(measurement.date >= '2016-08-23')\
                .filter(measurement.station == 'USC00519281')\
                .all()
        s_USC00519281_dict = dict(s_USC00519281)
        session.close()
        return jsonify(s_USC00519281_dict)

#5
@app.route('/api/v1.0/start')
def start(start):
        stats = session.query(func.max(measurement.tobs), func.min(measurement.tobs), func.avg(measurement.tobs).filter(measurement.date >=start)).all()
        stats_dict = dict(stats)
        session.close() 

if __name__ == '__main__':
    app.run()
