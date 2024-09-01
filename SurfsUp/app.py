# Import the dependencies.
from flask import Flask, jsonify
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt

#################################################
# Database Setup
#################################################

# create an engine to connect to the SQLite database
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################

# Create an instance of the Flask class
app = Flask(__name__)

@app.route("/")
def welcome():
    """List all available API routes."""
    return (
        f"Welcome to the Climate App API!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/&lt;start&gt;<br/>"
        f"/api/v1.0/&lt;start&gt;/&lt;end&gt;<br/>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    """Return the last 12 months of precipitation data."""
    # Create a session to connect to the database
    session = Session(engine)

    # Calculate the date one year from the most recent date
    recent_date = session.query(func.max(Measurement.date)).scalar()
    one_year_ago = dt.datetime.strptime(recent_date, "%Y-%m-%d") - dt.timedelta(days=365)

    # Query for the last 12 months of precipitation data
    results = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= one_year_ago).all()

    # Close the session
    session.close()

    # Convert the query results to a dictionary
    precipitation_dict = {date: prcp for date, prcp in results}

    # Return the JSON representation of the dictionary
    return jsonify(precipitation_dict)

@app.route("/api/v1.0/stations")
def stations():
    """Return a JSON list of all stations from the dataset."""
    # Create a session to connect to the database
    session = Session(engine)

    # Query all stations
    results = session.query(Station.station).all()

    # Close the session
    session.close()

    # Convert results to a list
    stations_list = list(map(lambda x: x[0], results))

    # Return the JSON list of stations
    return jsonify(stations_list)

@app.route("/api/v1.0/tobs")
def tobs():
    """Return the temperature observations for the most active station for the last year."""
    # Create a session to connect to the database
    session = Session(engine)

    # Calculate the date one year from the most recent date
    recent_date = session.query(func.max(Measurement.date)).scalar()
    one_year_ago = dt.datetime.strptime(recent_date, "%Y-%m-%d") - dt.timedelta(days=365)

    # Find the most active station
    most_active_station = session.query(Measurement.station).\
        group_by(Measurement.station).\
        order_by(func.count(Measurement.station).desc()).first()[0]

    # Query the temperature observations for the most active station for the last year
    results = session.query(Measurement.date, Measurement.tobs).\
        filter(Measurement.station == most_active_station).\
        filter(Measurement.date >= one_year_ago).all()

    # Close the session
    session.close()

    # Convert the query results to a list
    tobs_list = list(map(lambda x: {"date": x[0], "tobs": x[1]}, results))

    # Return the JSON list of temperature observations
    return jsonify(tobs_list)


@app.route("/api/v1.0/<start>")
@app.route("/api/v1.0/<start>/<end>")
def temp_stats(start=None, end=None):
    """Return min, avg, and max temperatures for a given start or start-end range."""
    # Create a session to connect to the database
    session = Session(engine)

    # Convert start and end dates from string to datetime objects to ensure correct format
    try:
        start_date = dt.datetime.strptime(start, "%Y-%m-%d")
        if end:
            end_date = dt.datetime.strptime(end, "%Y-%m-%d")
    except ValueError:
        # Return an error message if the date format is incorrect
        return jsonify({"error": "Invalid date format. Please use YYYY-MM-DD."}), 400

    # Perform query based on whether an end date is provided
    if end:
        # Query for min, avg, and max temperatures between start and end dates
        results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
            filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all()
    else:
        # Query for min, avg, and max temperatures from start date onward
        results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
            filter(Measurement.date >= start_date).all()

    # Close the session
    session.close()

    # Check if results are empty and return a 404 if not
    if not results or results[0][0] is None:
        return jsonify({"error": "No data available for the given date range."}), 404

    # Convert results to a dictionary
    temp_stats_dict = {
        "TMIN": results[0][0],
        "TAVG": results[0][1],
        "TMAX": results[0][2]
    }

    # Return the JSON representation of temperature statistics
    return jsonify(temp_stats_dict)
# Run the Flask application
if __name__ == "__main__":
    app.run(debug=True)

#################################################
# Flask Routes
#################################################
