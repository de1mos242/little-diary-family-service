from os import environ

from dotenv import load_dotenv

load_dotenv()


class Config:
    DATABASE_URI = environ.get('DATABASE_URI')
