from os import environ

from dotenv import load_dotenv

load_dotenv()


class Config:
    DATABASE_URI = environ.get('DATABASE_URI')
    JWT_PUBLIC_KEY = environ.get('JWT_PUBLIC_KEY').replace('\\n', '\n')
