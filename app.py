import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify

# Database Setup

engine = create_engine("sqlite:///Resources/hawaii.sqlite")

Base = automap_base()

Base.prepare(engine, reflect=True)

Measurement = Base.classes.measurement
Station = Base.classes.station

session = Session(engine)

app = Flask(__name__)

# Flask Routes

@app.route("/")
def Welcome():
    """List all available routes"""
    return (
        f"Routes Available:<br/>"
        f"<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"-> List of dates and percipitation observations from the last year (8-23-16 to 8-23-17).<br/>"
        f"<br/>"
        f"/api/v1.0/stations<br/>"
        f"-> List of stations from the dataset.<br/>"
        f"<br/>"
        f"/api/v1.0/tobs<br/>"
        f"-> List of Temperature Observations (tobs) for the previous year (8-23-16 to 8-23-17).<br/>"
        f"<br/>"
        f"/api/v1.0/start<br/>"
        f"-> List of the minimum temperature, the average temperature, and the max temperature for a chosen start date or range of dates.<br/>"
        f"<br/>"
        f"/api/v1.0/start/end<br/>"
        f"-> List of the minimum temperature, the average temperature, and the max temperature for a chosen start date or range of dates. (This list is inclusive)<br/>"

    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    """List of dates and percipitation observations from the last year (8-23-16 to 8-23-17)."""
# Convert the query results to a Dictionary using date as the key and prcp as the value.
# Return the JSON representation of your dictionary.
    one_year = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= '2016-08-23').\
        order_by(Measurement.date).all()

    prcp_list = []
    new = True
    for data in one_year:
        year_data = {}
        year_data["date"] = data.date
        year_data["prcp"] = data.prcp
        prcp_list.append(year_data)
        
    return jsonify(prcp_list)

@app.route("/api/v1.0/stations")
def stations():
    """List of stations from the dataset."""
# Return a JSON list of stations from the dataset.
    stations_query = session.query(Station.name, Station.station)
    stations_list = []
    for data in stations_query:
        stat_data = {}
        stat_data['station'] = data.station
        stat_data['name'] = data.name
        stations_list.append(stat_data)

    return jsonify(stations_list)

@app.route("/api/v1.0/tobs")
def tobs():
    """List of Temperature Observations (tobs) for the previous year (8-23-16 to 8-23-17)."""
# query for the dates and temperature observations from a year from the last data point.
# Return a JSON list of Temperature Observations (tobs) for the previous year.
    temperature = session.query(Measurement.date, Measurement.tobs).\
        filter(Measurement.date >= '2016-08-23').\
        order_by(Measurement.date).all()

    temp_list = []
    for data in temperature:
        temp_data = {}
        temp_data["date"] = data.date
        temp_data["tobs"] = data.tobs
        temp_list.append(temp_data)

    return jsonify(temp_list)

@app.route("/api/v1.0/<start>")
def option1(start):
        """List of the minimum temperature, the average temperature, and the max temperature for a chosen start date or range of dates."""
# Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.
# When given the start only, calculate TMIN, TAVG, and TMAX for all dates greater than and equal to the start date.

#     start_date= dt.datetime.strptime(start, '%Y-%m-%d')
#     last_year = dt.timedelta(days=365)
#     start = start_date-last_year
#     end =  dt.date(2017, 8, 23)
#     trip_data = session.query(func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)).\
#         filter(measurement.date >= start).filter(measurement.date <= end).all()
#     trip = list(np.ravel(trip_data))
#     return jsonify(trip)

# @app.route("/api/v1.0/<start>/<end>")
# def option2(start,end):

#     start_date= dt.datetime.strptime(start, '%Y-%m-%d')
#     end_date= dt.datetime.strptime(end,'%Y-%m-%d')
#     last_year = dt.timedelta(days=365)
#     start = start_date-last_year
#     end = end_date-last_year
#     trip_data = session.query(func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)).\
#         filter(measurement.date >= start).filter(measurement.date <= end).all()
#     trip = list(np.ravel(trip_data))
#     return jsonify(trip)

if __name__ == "__main__":
    app.run(debug=True)