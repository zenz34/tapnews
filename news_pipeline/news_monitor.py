import datetime
import hashlib
import logging
import redis
import os
import sys
import yaml

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'common'))

import news_api_client
from cloudAMQP_client import CloudAMQPClient

"""SLEEP_TIME_IN_SECONDS = 10
NEWS_TIME_OUT_IN_SECONDS = 3600 * 24 * 3

REDIS_HOST = 'localhost'
REDIS_PORT = 6379

# TODO: use your own queue
SCRAPE_NEWS_TASK_QUEUE_URL = "amqp://szlywwfk:mlSl3d9rfBiRbQ1e1dcC1bCFKGqK3CSV@crane.rmq.cloudamqp.com/szlywwfk"
SCRAPE_NEWS_TASK_QUEUE_NAME = "cs503"

NEWS_SOURCES = [
    'bbc-news',
    'bbc-sport',
    'bloomberg',
    'cnn',
    'entertainment-weekly',
    'espn',
    'ign',
    'techcrunch',
    'the-new-york-times',
    'the-wall-street-journal',
    'the-washington-post'
]
"""
with open('../configuration/news_pipeline_conf.yaml', 'r') as stream:
    try:
        config = yaml.load(stream)
    except yaml.YAMLError as error1:
        print error1

redis_client = redis.StrictRedis(config['news_monitor']['REDIS_HOST'],
                                 config['news_monitor']['REDIS_PORT'])
cloudAMQP_client = CloudAMQPClient(config['news_monitor']['SCRAPE_NEWS_TASK_QUEUE_URL'],
                                 config['news_monitor']['SCRAPE_NEWS_TASK_QUEUE_NAME'])

while True:
    news_list = news_api_client.getNewsFromSource(config['news_monitor']['NEWS_SOURCES'])

    num_of_news_news = 0

    for news in news_list:
        news_digest = hashlib.md5(news['title'].encode('utf-8')).digest().encode('base64')

        if redis_client.get(news_digest) is None:
            num_of_news_news = num_of_news_news + 1
            news['digest'] = news_digest

            if news['publishedAt'] is None:
                news['publishedAt'] = datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")

            redis_client.set(news_digest, "True")
            redis_client.expire(news_digest, config['news_monitor']['NEWS_TIME_OUT_IN_SECONDS'])

            cloudAMQP_client.sendMessage(news)

    print "Fetched %d news." % num_of_news_news
    logging.basicConfig(level=logging.INFO, format='%(asctime)s %(message)s', filename='NumbersOfNews.log')
    logging.info('We have %d news monitored' %num_of_news_news)

    cloudAMQP_client.sleep(config['news_monitor']['SLEEP_TIME_IN_SECONDS'])
