
import datetime
import logging
import os
import sys
import yaml

from dateutil import parser
from sklearn.feature_extraction.text import TfidfVectorizer

# import common package in parent directory
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'common'))

import mongo_client
import news_topic_modeling_service_client
from cloudAMQP_client import CloudAMQPClient

# TODO: use your own queue.
"""
DEDUPE_NEWS_TASK_QUEUE_URL = "amqp://woxjcspc:qyiiCvwVlB-Ro4Hsk46qi_vdS3uVwxUM@fish.rmq.cloudamqp.com/woxjcspc"
DEDUPE_NEWS_TASK_QUEUE_NAME = "test1"

SLEEP_TIME_IN_SECONDS = 1
"""
NEWS_TABLE_NAME = "news-test"

SAME_NEWS_SIMILARITY_THRESHOLD = 0.9

with open('../configuration/news_pipeline_conf.yaml', 'r') as stream:
    try:
        config = yaml.load(stream)
    except yaml.YAMLError as error3:
        print error3


cloudAMQP_client = CloudAMQPClient(config['news_deduper']['DEDUPE_NEWS_TASK_QUEUE_URL'],
                                   config['news_deduper']['DEDUPE_NEWS_TASK_QUEUE_NAME'])

def handle_message(msg):
    #if msg is None or not isinstance(msg, dict):
        #return

    task = msg
    text = task['text']
    if text is None:
        #print 'how are you'
        return

    published_at = parser.parse(task['publishedAt'])
    published_at_day_begin = datetime.datetime(published_at.year, published_at.month, published_at.day, 0, 0, 0, 0)
    published_at_day_end = published_at_day_begin + datetime.timedelta(days=1)
    print 'hello'
    db = mongo_client.get_db()
    same_day_news_list = list(db[NEWS_TABLE_NAME].find(
        {'publishedAt': {'$gte': published_at_day_begin,
                         '$lt': published_at_day_end}}))
    print 'how are you'
    if same_day_news_list is not None and len(same_day_news_list) > 0:
        documents = [news['text'] for news in same_day_news_list]
        documents.insert(0, text)

        tfidf = TfidfVectorizer().fit_transform(documents)
        pairwise_sim = tfidf * tfidf.T

        print pairwise_sim

        rows, _ = pairwise_sim.shape

        for row in range(1, rows):
            if pairwise_sim[row, 0] > config['news_deduper']['SAME_NEWS_SIMILARITY_THRESHOLD']:
                print "Duplicated news. Ignore."
                return
    print 'what about'
    task['publishedAt'] = parser.parse(task['publishedAt'])
    #Classified news
    print 'title is title'
    title = task['title']
    if title is not None:
        topic = news_topic_modeling_service_client.classify(title)
        task['class'] = topic
    print 'what is wrong'
    db[NEWS_TABLE_NAME].replace_one({'digest': task['digest']}, task, upsert=True)


while True:

    if cloudAMQP_client is not None:
        msg = cloudAMQP_client.getMessage()
        if msg is not None:
           #Parse and process the task
           try:
               handle_message(msg)
           except Exception as e:
               print e
               pass

        cloudAMQP_client.sleep(config['news_deduper']['SLEEP_TIME_IN_SECONDS'])
