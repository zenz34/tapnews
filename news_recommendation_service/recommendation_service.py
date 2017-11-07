import operator
import os
import pyjsonrpc
import sys
import yaml 

#import common package in parent directory
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'common'))

import mongo_client

PREFERENCE_MODEL_TABLE_NAME = "user_preference_model"
"""
SERVER_HOST = "localhost"
SERVER_PORT = 5050
"""
with open('../configuration/recommend_log_conf.yaml', 'r') as stream:
    try:
        config = yaml.load(stream)
    except yaml.YAMLError as error1:
        print error1

def isclose(a, b, rel_tol=1e-09, abs_tol=0.0):
    return abs(a-b) <= max(rel_tol * max(abs(a), abs(b)), abs_tol)

class RequestHandler(pyjsonrpc.HttpRequestHandler):
    """ Get user's preference in an ordered class list """
    @pyjsonrpc.rpcmethod
    def getPreferenceForUser(self, user_id):
        db = mongo_client.get_db()
        model = db[PREFERENCE_MODEL_TABLE_NAME].find_one({'userId':user_id})
        if model is None:
            return []

        sorted_tuples = sorted(model['preference'].items(), key=operator.itemgetter(1), reverse=True)
        sorted_list = [x[0] for x in sorted_tuples]
        sorted_value_list = [x[1] for x in sorted_tuples]

        # If the first preference is same as the last one, the preference makes
        # no sense.
        if isclose(float(sorted_value_list[0]), float(sorted_value_list[-1])):
            return []

        return sorted_list


# Threading HTTP Server
http_server = pyjsonrpc.ThreadingHttpServer(
    server_address = (config['recommendation_service']['SERVER_HOST'],
                      config['recommendation_service']['SERVER_PORT']),
    RequestHandlerClass = RequestHandler
)

print "Starting HTTP server on %s:%d" % (config['recommendation_service']['SERVER_HOST'],
                                         config['recommendation_service']['SERVER_PORT'])

http_server.serve_forever()
