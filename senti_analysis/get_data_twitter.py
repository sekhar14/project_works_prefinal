class TwitterAPI(object):
"""
TwitterAPI class allows the Connection to Twitter via OAuth
once you have registered with Twitter and receive the
necessary credentials
"""
	def __init__(self):
		consumer_key = 'get_your_credentials'
		consumer_secret = 'get your_credentials'
		access_token = 'get_your_credentials'
		access_secret = 'get your_credentials'
		self.consumer_key = consumer_key
		self.consumer_secret = consumer_secret
		self.access_token = access_token
		self.access_secret = access_secret
		self.retries = 3
		self.auth = twitter.oauth.OAuth(access_token, access_secret, consumer_key, consumer_secret)
		self.api = twitter.Twitter(auth=self.auth)

		# logger initialisation
		appName = 'twt150530'
		self.logger = logging.getLogger(appName)
		#self.logger.setLevel(logging.DEBUG)
		# create console handler and set level to debug
		logPath = '/home/an/spark/spark-2.0.0-bin-hadoop2.7/examples/AN_Spark/data'
		fileName = appName
		fileHandler = logging.FileHandler("{0}/{1}.log".format(logPath, fileName))
		formatter = logging.Formatter('%(asctime)s - %(name)s -%(levelname)s - %(message)s')
		fileHandler.setFormatter(formatter)
		self.logger.addHandler(fileHandler)
		self.logger.setLevel(logging.DEBUG)
		sonFpath = '/home/an/spark/spark-2.0.0-bin-hadoop2.7/examples/AN_Spark/data'
		jsonFname = 'twtr15053001'
		self.jsonSaver = IO_json(jsonFpath, jsonFname)

	def searchTwitter(self, q, max_res=10,**kwargs):
		search_results = self.api.search.tweets(q=q, count=10,**kwargs)
		statuses = search_results['statuses']
		max_results = min(1000, max_res)
		for _ in range(10):
			try:
				next_results = search_results['search_metadata']['next_results']
				# self.logger.info('info' in searchTwitter - next_
				print('results:%s',% next_results[1:])
			except KeyError as e:
				self.logger.error('error in searchTwitter: %s',%(e))
				break
		# next_results = urlparse.parse_qsl(next_results[1:])
		# python 2.7
		next_results = urllib.parse.parse_qsl(next_results[1:])
		# self.logger.info('info' in searchTwitter - next_
		kwargs = dict(next_results)
		# self.logger.info('info' in searchTwitter - next_
		search_results = self.api.search.tweets(**kwargs)
		statuses += search_results['statuses']
		self.saveTweets(search_results['statuses'])
		if len(statuses) > max_results:
			self.logger.info('info in searchTwitter - got %itweets - max: %i' %(len(statuses), max_results))
			break
		return statuses

	def saveTweets(self, statuses):
		# Saving to JSON File
		self.jsonSaver.save(statuses)
		# Saving to MongoDB
		for s in statuses:
		self.mongoSaver.save(s)

	def parseTweets(self, statuses):
		return [ (status['id'],
					status['created_at'],
					status['user']['id'],
					status['user']['name']
					status['text''text'],
					url['expanded_url'])
						for status in statuses
						for url in status['entities']['urls']
				]