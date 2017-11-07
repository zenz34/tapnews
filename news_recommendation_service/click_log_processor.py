# -*- coding: utf-8 -*-

'''
Time decay model:
If selected:
p = (1-α)p + α
If not:
p = (1-α)p
Where p is the selection probability, and α is the degree of weight decrease.
The result of this is that the nth most recent selection will have a weight of
(1-α)^n. Using a coefficient value of 0.05 as an example, the 10th most recent
selection would only have half the weight of the most recent. Increasing epsilon
would bias towards more recent results more.
'''
from datetime import datetime
import news_classes
import os
import sys
import yaml


# import common package in parent directory
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'common'))

import mongo_client
from cloudAMQP_client import CloudAMQPClient

# Don't modify this value unless you know what you are doing.

NUM_OF_CLASSES = 17
INITIAL_P = 1.0 / NUM_OF_CLASSES
ALPHA = 0.1

"""
SLEEP_TIME_IN_SECONDS = 1

LOG_CLICKS_TASK_QUEUE_URL = "amqp://crxnfwlj:Xit95SxV29p5HAoSUwDO0BsMd9G6KC82@crane.rmq.cloudamqp.com/crxnfwlj"
LOG_CLICKS_TASK_QUEUE_NAME = "clickLog"

"""
with open('../configuration/recommend_log_conf.yaml', 'r') as stream:
    try:
        config = yaml.load(stream)
    except yaml.YAMLError as error1:
        print error1

PREFERENCE_MODEL_TABLE_NAME = "user_preference_model"
NEWS_TABLE_NAME = "news"

cloudAMQP_client = CloudAMQPClient(config['click_log_processor']['LOG_CLICKS_TASK_QUEUE_URL'],
                                   config['click_log_processor']['LOG_CLICKS_TASK_QUEUE_NAME'])

def handle_message(msg):
    if msg is None or not isinstance(msg, dict) :
        return

    if ('userId' not in msg
        or 'newsId' not in msg
        or 'timestamp' not in msg):
        return

    userId = msg['userId']
    newsId = msg['newsId']

    # Update user's preference
    db = mongo_client.get_db()
    model = db[PREFERENCE_MODEL_TABLE_NAME].find_one({'userId': userId})

    # If model not exists, create a new one
    if model is None:
        print 'Creating preference model for new user: %s' % userId
        new_model = {'userId' : userId}
        preference = {}
        for i in news_classes.classes:
            preference[i] = float(INITIAL_P)
        new_model['preference'] = preference
        model = new_model

    print 'Updating preference model for new user: %s' % userId

    # Update model using time decaying method
    news = db[NEWS_TABLE_NAME].find_one({'digest': newsId})
    if (news is None
        or 'class' not in news
        or news['class'] not in news_classes.classes):
        print news is None
        print 'class' not in news
        print news['class'] not in news_classes.classes
        print 'Skipping processing...'
        return

    click_class = news['class']

    # Update the clicked one.
    old_p = model['preference'][click_class]
    model['preference'][click_class] = float((1 - ALPHA) * old_p + ALPHA)

    # Update not clicked classes.
    for i, prob in model['preference'].iteritems():
        if not i == click_class:
            model['preference'][i] = float((1 - ALPHA) * model['preference'][i])

    db[PREFERENCE_MODEL_TABLE_NAME].replace_one({'userId': userId}, model, upsert=True)

def run():
    while True:
        if cloudAMQP_client is not None:
            msg = cloudAMQP_client.getMessage()
            if msg is not None:
                # Parse and process the task
                try:
                    print msg
                    handle_message(msg)
                except Exception as e:
                    print e
                    pass
            # Remove this if this becomes a bottleneck.
            cloudAMQP_client.sleep(int(config['click_log_processor']['SLEEP_TIME_IN_SECONDS']))

if __name__ ==  "__main__":
    run()
