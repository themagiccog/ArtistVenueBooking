import os
SECRET_KEY = os.urandom(32)
# Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))

# Enable debug mode.
DEBUG = True

# Connect to the database


# TODO IMPLEMENT DATABASE URL - DONE
SQLALCHEMY_DATABASE_URI = 'sqlite:///fyyur.db'
#SQLALCHEMY_DATABASE_URI = 'postgresql://cog:1234@localhost:5432/fyyur'
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///testing.db'
