import os
import sys
import yaml
from newspaper import Article

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'common'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'scraper'))

import cnn_news_scraper
from cloudAMQP_client import CloudAMQPClient

"""
DEDUPE_NEWS_TASK_QUEUE_URL = "amqp://woxjcspc:qyiiCvwVlB-Ro4Hsk46qi_vdS3uVwxUM@fish.rmq.cloudamqp.com/woxjcspc"
DEDUPE_NEWS_TASK_QUEUE_NAME = "test1"
SCRAPE_NEWS_TASK_QUEUE_URL = "amqp://szlywwfk:mlSl3d9rfBiRbQ1e1dcC1bCFKGqK3CSV@crane.rmq.cloudamqp.com/szlywwfk"
SCRAPE_NEWS_TASK_QUEUE_NAME = "cs503"

SLEEP_TIME_IN_SECONDS = 5
"""
with open('../configuration/news_pipeline_conf.yaml', 'r') as stream:
    try:
        config = yaml.load(stream)
    except yaml.YAMLError as error1:
        print error1

dedupe_news_queue_client = CloudAMQPClient(config['news_fetcher']['DEDUPE_NEWS_TASK_QUEUE_URL'],
                                           config['news_fetcher']['DEDUPE_NEWS_TASK_QUEUE_NAME'])
scrape_news_queue_client = CloudAMQPClient(config['news_fetcher']['SCRAPE_NEWS_TASK_QUEUE_URL'],
                                           config['news_fetcher']['SCRAPE_NEWS_TASK_QUEUE_NAME'])

def handle_messsage(msg):
    if msg is None or not isinstance(msg, dict):
        print 'message is broken'
        return
    
    task = msg
    text = None

    article = Article(task['url'])
    article.download()
    article.parse()

    task['text'] = article.text.encode('utf-8')

    #if task['source'] == 'cnn':
    #    print 'scrapping cnn news'
    #    text = cnn_news_scraper.extract_news(task['url'])
    #else:
    #    print "News source [%s] is not supported" % task['source']

    #task['text'] = text
    dedupe_news_queue_client.sendMessage(task)

while True:
    if scrape_news_queue_client is not None:
        msg = scrape_news_queue_client.getMessage()
        if msg is not None:
            try:
                handle_messsage(msg)
            except Exception as e:
                print
                pass
        scrape_news_queue_client.sleep(config['news_fetcher']['SLEEP_TIME_IN_SECONDS'])
