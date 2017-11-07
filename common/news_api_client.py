import requests
import yaml
from json import loads


with open('../configuration/common_conf.yaml', 'r') as stream:
    try:
        config = yaml.load(stream)
        #print config

    except yaml.YAMLError as error2:
        print error2

NEWS_API_ENDPOINT = config['news_api_client']['NEWS_API_ENDPOINT']
NEWS_API_KEY = config['news_api_client']['NEWS_API_KEY']
ARTICLES_API = config['news_api_client']['ARTICLES_API']

BBC_NEWS = 'bbc-news'
BBC_SPORT = 'bbc-sport'
CNN = 'cnn'

DEFAULT_SOURCES = config['news_api_client']['DEFAULT_SOURCES']
SORT_BY_TOP = config['news_api_client']['SORT_BY_TOP']

def buildUrl(endPoint=NEWS_API_ENDPOINT, apiName=ARTICLES_API):
    return endPoint + apiName

def getNewsFromSource(sources=DEFAULT_SOURCES, sortBy=SORT_BY_TOP):
    articles = []

    for source in sources:
        payload = {'apiKey': NEWS_API_KEY,
                   'source': source,
                   'sortBy': sortBy
        }

        response = requests.get(buildUrl(), params=payload)
        print response.content
        res_json = loads(response.content)

        # Extract info from response
        if (res_json is not None and
            res_json['status'] == 'ok' and
            res_json['source'] is not None):
            # populate news source in each articles
            for news in res_json['articles']:
                news['source'] = res_json['source']

            articles.extend(res_json['articles'])

    return articles
