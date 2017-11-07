import pyjsonrpc
import yaml

#URL = "http://localhost:6060/"
with open('../configuration/common_conf.yaml', 'r') as stream:
    try:
        config = yaml.load(stream)
    except yaml.YAMLError as error5:
        print error5

client = pyjsonrpc.HttpClient(url=config['news_topic_modeling_service_client']['URL'])

def classify(text):
    topic = client.call('classify', text)
    print "Topic: %s" % str(topic)
    return topic
