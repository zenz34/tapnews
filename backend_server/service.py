"""Backend service"""
import logging
import operations
import pyjsonrpc
import yaml


"""
SERVER_HOST = 'localhost'
SERVER_PORT = 4040
"""

with open('../configuration/backend_conf.yaml', 'r') as stream:
    try:
       config = yaml.load(stream)
    except yaml.YAMLError as error1:
       print error1

class RequestHandler(pyjsonrpc.HttpRequestHandler):
    """ RPC request handler """
    @pyjsonrpc.rpcmethod
    def add(self, num1, num2):
        """Test method"""
        print "add is called with %d and %d" % (num1, num2)
        return num1 + num2

    """ Get news summaries for a user """
    @pyjsonrpc.rpcmethod
    def getNewsSummariesForUser(self, user_id, page_num):
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', filename='newsSummary.log')
        logging.info('userId: ' + user_id + '  pageNumber: ' + page_num)
        return operations.getNewsSummariesForUser(user_id, page_num)


    """ Log user news clicks """
    @pyjsonrpc.rpcmethod
    def logNewsClickForUser(self, user_id, news_id):
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', filename='click_record_two.log')
        logging.info('userId: ' + user_id +', ' + 'newsId: ' + news_id +', ' + 'timestamp: '+ datetime.utcnow())

        return operations.logNewsClickForUser(user_id, news_id)


HTTP_SERVER = pyjsonrpc.ThreadingHttpServer(
    server_address=(config['service']['SERVER_HOST'],
                    int(config['service']['SERVER_PORT'])),
    RequestHandlerClass=RequestHandler
)

print "Starting HTTP server on %s:%d" % (config['service']['SERVER_HOST'],
                                         int(config['service']['SERVER_PORT']))

HTTP_SERVER.serve_forever()
