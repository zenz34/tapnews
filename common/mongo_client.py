from pymongo import MongoClient
import yaml
"""
MONGO_DB_HOST = 'localhost'
MONGO_DB_PORT = '27017'
"""
DB_NAME = 'tap-news'


with open('../configuration/common_conf.yaml', 'r') as stream:
    try:
        config = yaml.load(stream)
    except yaml.YAMLError as error1:
        print error1

client = MongoClient("%s:%s" %(config['mongo_client']['MONGO_DB_HOST'], config['mongo_client']['MONGO_DB_PORT']))


def get_db(db=DB_NAME):
    return client[db]
