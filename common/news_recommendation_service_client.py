import pyjsonrpc
import yaml
#URL = "http://localhost:5050/"
with open('../configuration/common_conf.yaml', 'r') as stream:
    try:
        config = yaml.load(stream)
    except yaml.YAMLError as error7:
        print error7

client = pyjsonrpc.HttpClient(url=config['news_recommendation_service_client']['URL'])

def getPreferenceForUser(userId):
    preference = client.call('getPreferenceForUser', userId)
    print "Preference list: %s" % str(preference)
    return preference
