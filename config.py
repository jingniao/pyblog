import os

DEBUG = False
SQLALCHEMY_ECHO = False
SECRET_KEY = 'change_this_secret_key'


DB_DATABASE = os.environ['DB_DATABASE']
DB_USER = os.environ['DB_USER']
DB_HOST = os.environ['DB_HOST']
DB_DRIVER = os.environ['DB_DRIVER']
DB_PASSWORD = os.environ['DB_PASSWORD']

SQLALCHEMY_DATABASE_URI = '{0}://{1}:{2}@{3}/{4}?charset=utf8mb4'.format(
    DB_DRIVER,DB_USER,DB_PASSWORD,DB_HOST,DB_DATABASE)
