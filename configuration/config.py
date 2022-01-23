import os
import secrets
from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())

class Config:
    SECRETE_KEY = secrets.token_hex(16)
    DEBUG = True #flase if in production
    SQLALCHEMY_DATABASE_URI = None
    #other settings constacts NB; replace None above with database uri
