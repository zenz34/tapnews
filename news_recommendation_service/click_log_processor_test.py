import click_log_processor
import os
import sys

from datetime import datetime
from sets import Set

#import common package in parent directory
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'common'))

import mongo_client

PREFERENCE_MODEL_TABLE_NAME = 'user_preference_model'
NEWS_TABLE_NAME = "news"

NUM_OF_CLASSES = 17

#start MongoDB before running followings
def test_basic():
    db = mongo_client.get_db()
    db[PREFERENCE_MODEL_TABLE_NAME].delete_many({"userId": "test_user1"})

    msg = {"userId": "test_user1",
           "newsId": "test_news",
           "timestamp": str(datetime.utcnow())}

    click_log_processor.handle_message(msg)

    model = db[PREFERENCE_MODEL_TABLE_NAME].find_one({'userId':'test_user1'})
    assert model is not None
    assert len(model['preference']) == NUM_OF_CLASSES

    print 'test_basic passed'

if __name__ == "__main__":
    test_basic()
