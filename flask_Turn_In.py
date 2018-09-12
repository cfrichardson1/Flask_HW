# =======================================================
# MODULES
# =======================================================
import datetime as dt
from flask import Flask, jsonify
import numpy as np
import pandas as pd

# Python SQL toolkit and Object Relational Mapper
import sqlalchemy
# =========== base classification ===========
from sqlalchemy.ext.declarative import declarative_base
# =======================================================

from sqlalchemy.orm import Session
from sqlalchemy.orm.session import sessionmaker
from sqlalchemy import and_,Column, create_engine, Date, distinct, Integer,Float, ForeignKey, func, inspect, MetaData, String

# ========================================END======================================================================

# ** other foundational components **


engine = create_engine("sqlite:///Resources/hawaii.sqlite")

Base = declarative_base()

# =======================================================
# classes
# =======================================================

class Measurement(Base):
    __tablename__ = "measurement"
    id = Column(Integer, primary_key=True)
    station = Column(String(255), ForeignKey('station.station'))
    date = Column(Date)
    prcp = Column(Float)
    tobs = Column(Float)
    
class Station(Base):
    __tablename__ = "station"
    station = Column(Integer, primary_key = True)
    name = Column(String(255))
    latitude = Column(Float)
    longitude = Column(Float)
    elevation = Column(Float)
 
# ** other foundational components **

# reflect an existing database into a new model
Base.metadata.create_all(engine)

# create inspector and session
Session = sessionmaker(bind=engine)

app = Flask(__name__)

#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
	"""List all available api routes."""
	return(
		f"<li>/api/v1.0/precipitation<br/>"
		f"<li>/api/v1.0/stations<br/>"
		f"<li>/api/v1.0/tobs<br/>"
		f"<li>/api/v1.0/&lt;start&gt;<br/>"
		f"&emsp;&emsp;format yyyy-mm-dd<br/>"
		f"<li>/api/v1.0/&lt;start&gt;/&lt;end&gt;<br/>"
		f"&emsp;&emsp;format yyyy-mm-dd<br/>"
    )

# ----------------
# PERCEPITATION
# ----------------

@app.route("/api/v1.0/precipitation")
def precipitation():
	session = Session()

	#	calculate	latest	date
	log_date = session.query(func.max(Measurement.date)).all()[0][0]
	#	subtract	1	year
	log_date = log_date-dt.timedelta(days=365)

	query =	session.query(
					Measurement.date,
					Measurement.prcp,
					).filter(Measurement.date >= log_date).all()

	precip = []
	for	row	in	query:
		precip_dict	=	{}
		precip_dict['Date']	= row.date
		precip_dict['Precipitation'] = row.prcp
		precip.append(precip_dict)

	return jsonify(precip)


# ----------------
# STATIONS
# ----------------
@app.route("/api/v1.0/stations")
def stations():
    session = Session()
    results = session.query(Station.station).all()

    # Convert list of tuples into normal list
    all_stations = list(np.ravel(results))

    return jsonify(all_stations)



# ----------------
# TOBS
# ----------------
@app.route("/api/v1.0/tobs")
def tobs():
	session = Session()

	# calculate	latest	date
	log_date = session.query(func.max(Measurement.date)).all()[0][0]
	# subtract	1	year
	log_date = log_date-dt.timedelta(days = 365)

	query = session.query(
					Measurement.date,
					Measurement.tobs,
					).filter(Measurement.date >= log_date).all()

	tobs = []
	for	row	in	query:
		tobs_dict = {}
		tobs_dict['Date'] = row.date
		tobs_dict['Time_Observation_Bias']	= row.tobs
		tobs.append(tobs_dict)

	return jsonify(tobs)


# ----------------
# START DATE
# df date format yyyy-mm-dd
# calculate `TMIN`, `TAVG`, and `TMAX` for all dates >= start date.
# ----------------

@app.route("/api/v1.0/<start>")
def date_start(start):
	session = Session()
	start_date = dt.datetime.strptime(start,'%Y-%m-%d')

	sel	=	[func.min(Measurement.tobs),func.avg(Measurement.tobs),	func.max(Measurement.tobs)]
	response =	session.query(Measurement.date,*sel).group_by(Measurement.date).filter(Measurement.date	>= start_date).all()
	
	list_of_dates = []
	for row in response:
		record_dict = {}
		record_dict['Date'] = row[0]
		record_dict['Min Temp'] = row[1]
		record_dict['Avg Temp'] = row[2]
		record_dict['Max Temp'] = row[3]
		list_of_dates.append(record_dict)

	return jsonify(list_of_dates)





# ----------------
# # START & END DATE
# # calculate the `TMIN`, `TAVG`, and `TMAX` for dates between the start and end date inclusive.
# # ----------------
@app.route("/api/v1.0/<start>/<end>")
def date_start_end(start, end):
	session = Session()

	sel	=	[func.min(Measurement.tobs),func.avg(Measurement.tobs),	func.max(Measurement.tobs)]
	response =	session.query(Measurement.date,*sel).group_by(Measurement.date).filter(Measurement.date	<= end).filter(Measurement.date>= start_date).all()
	
	list_of_dates = []
	for row in response:
		record_dict = {}
		record_dict['Date'] = row[0],
		record_dict['Min Temp'] = row[1],
		record_dict['Avg Temp'] = row[2],
		record_dict['Max Temp'] = row[3],
		list_of_dates.append(record_dict)

	return jsonify(list_of_dates)



if __name__ == '__main__':
    app.run(debug=True)