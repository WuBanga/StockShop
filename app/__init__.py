from flask import Flask
import redis
from pymongo import MongoClient
from elasticsearch import Elasticsearch
from neo4j import GraphDatabase
import psycopg2


app = Flask(__name__)


redis = redis.Redis(
    host='localhost',
    port=6379
)

mongo = MongoClient(
    'mongodb://localhost',
    port=27017,
    username='yourusername',
    password='yourpassword'
)

es = Elasticsearch(
    ['localhost'],
    port=9200
)

postgresConnect = psycopg2.connect(
    dbname='yourdatabasename',
    user='yourusername',
    password='yourpassword',
    host='localhost',
    port=5432
)

neo = GraphDatabase.driver('bolt://localhost:7687', auth=('yourusername', 'yourpassword'))

from app import routes