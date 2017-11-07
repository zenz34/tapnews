import cnn_news_scraper as scraper

#EXPECTED_NEWS = "Santiago is charged with using and carrying a firearm during and in relation to a crime of violence"
#CNN_NEWS_URL = "http://edition.cnn.com/2017/01/17/us/fort-lauderdale-shooter-isis-claim/index.html"

EXPECTED_NEWS = "A source with knowledge of the staff shakeup told CNN in late July that deputy press secretary Lindsay Walters"
CNN_NEWS_URL = "http://www.cnn.com/2017/08/24/politics/andrew-hemming-white-house-communications-spicer-priebus/index.html"

def test_basic():
    news = scraper.extract_news(CNN_NEWS_URL)

    print news
    assert EXPECTED_NEWS in news
    print 'test_basic passed!'

if __name__ == "__main__":
    test_basic()
