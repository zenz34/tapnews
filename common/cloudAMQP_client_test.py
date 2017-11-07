from cloudAMQP_client import CloudAMQPClient


#CLOUDAMQP_URL = "amqp://szlywwfk:mlSl3d9rfBiRbQ1e1dcC1bCFKGqK3CSV@crane.rmq.cloudamqp.com/szlywwfk"
#TEST_QUEUE_NAME = "test"

CLOUDAMQP_URL = "amqp://szlywwfk:mlSl3d9rfBiRbQ1e1dcC1bCFKGqK3CSV@crane.rmq.cloudamqp.com/szlywwfk"
TEST_QUEUE_NAME = "cs503"

def test_basic():
    client = CloudAMQPClient(CLOUDAMQP_URL, TEST_QUEUE_NAME)

    sentMsg = {"test": "test"}
    client.sendMessage(sentMsg)
    receivedMsg = client.getMessage()

    assert sentMsg == receivedMsg
    print "test_basic passed"

if __name__ == "__main__":
    test_basic()
