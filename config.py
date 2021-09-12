import os

class Config:
    # Load in enviornemnt variables
    JWT_ACCESS_TOKEN_EXPIRES = False
    JWT_REFRESH_TOKEN_EXPIRES = False
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_STRING')
    DB_HOST = os.getenv('VIDEO_SERVICE_SQL_INSTANCE')
    DB_NAME = os.getenv('VIDEO_SERVICE_DB_NAME')
    DB_USER = os.getenv('VIDEO_SERVICE_DB_USER')
    DB_PASSWORD = os.getenv('VIDEO_SERVICE_DB_PASSWORD')
    PORT = os.getenv('PORT')