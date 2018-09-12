				sel	=	[func.min(Measurement.tobs),	func.avg(Measurement.tobs),	func.max(Measurement.tobs)]
				query	=	session.query(
								Measurement.date,
								*sel
				).group_by(
								Measurement.date
				).filter(
								Measurement.date	>=	start_date
				).all()


sel	=	[func.min(Measurement.tobs),func.avg(Measurement.tobs),	func.max(Measurement.tobs)]
query =	session.query(Measurement.date,*sel).group_by(Measurement.date).filter(Measurement.date	>= start_date).all()