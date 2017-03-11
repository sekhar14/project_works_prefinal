import time
from pyspark import SparkContext
from pyspark.streaming import StreamingContext
import twitter
import dateutil.parser
import json
# Connecting Streaming Twitter with Streaming Spark via Queue
class Tweet(dict):
	def __init__(self, tweet_in):
		super(Tweet, self).__init__(self)
		if tweet_in and 'delete' not in tweet_in:
			self['timestamp'] = dateutil.parser.parse(tweet_
											in[u'created_at']
														).replace(tzinfo=None).isoformat()
		self['text'] = tweet_in['text'].encode('utf-8')
#self['text'] = tweet_in['text']
		self['hashtags'] = [x['text'].encode('utf-8') for x in tweet_in['entities']['hashtags']]
#self['hashtags'] = [x['text'] for x in tweet_
																				in['entities']['hashtags']
		self['geo'] = tweet_in['geo']['coordinates'] if tweet_ in['geo'] else None
		self['id'] = tweet_in['id']
		self['screen_name'] = tweet_in['user']['screen_name'].encode('utf-8')
#self['screen_name'] = tweet_in['user']['screen_name']
		self['user_id'] = tweet_in['user']['id']
	def connect_twitter():
		twitter_stream = twitter.TwitterStream(auth=twitter.OAuth(
												token = "get_your_own_credentials",
												token_secret = "get_your_own_credentials",
												consumer_key = "get_your_own_credentials",
												consumer_secret = "get_your_own_credentials"))
		return twitter_stream
	def get_next_tweet(twitter_stream):
		stream = twitter_stream.statuses.sample(block=True)
		tweet_in = None
		while not tweet_in or 'delete' in tweet_in:
			tweet_in = stream.next()
			tweet_parsed = Tweet(tweet_in)
		return json.dumps(tweet_parsed)
	def process_rdd_queue(twitter_stream):
# Create the queue through which RDDs can be pushed to
# a QueueInputDStream
		rddQueue = []
		for i in range(3):
			rddQueue += [ssc.sparkContext.parallelize([get_next_
			tweet(twitter_stream)], 5)]
		lines = ssc.queueStream(rddQueue)
		lines.pprint()
if __name__ == "__main__":
	sc = SparkContext(appName="PythonStreamingQueueStream")
	ssc = StreamingContext(sc, 1)
# Instantiate the twitter_stream
	twitter_stream = connect_twitter()
# Get RDD queue of the streams json or parsed
	process_rdd_queue(twitter_stream)
	ssc.start()
	time.sleep(2)
	ssc.stop(stopSparkContext=True, stopGraceFully=True)