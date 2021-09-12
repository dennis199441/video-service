from datetime import datetime
import sqlalchemy
import os
from sqlalchemy import Column, String, Integer, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import config

sql_instance_name = str(config.Config.DB_HOST)
db_name = str(config.Config.DB_NAME)
db_user = str(config.Config.DB_USER)
db_password = str(config.Config.DB_PASSWORD)
'''
engine = sqlalchemy.create_engine(
	# Equivalent URL:
	# mysql+pymysql://<db_user>:<db_pass>@/<db_name>?unix_socket=/cloudsql/<cloud_sql_instance_name>
	sqlalchemy.engine.url.URL(
		drivername='mysql+pymysql',
		username=db_user,
		password=db_password,
		database=db_name,
		query={
			'unix_socket': '/cloudsql/{}'.format(sql_instance_name)
		}
	)
)
'''
# For localhost
engine = sqlalchemy.create_engine(
    'mysql+pymysql://{}:{}@{}/{}'.format(db_user, db_password, sql_instance_name, db_name))

Session = sessionmaker(bind=engine)

Base = declarative_base()


class Entity():
    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)

    def __init__(self):
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
