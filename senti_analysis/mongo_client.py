from pymongo import MongoClient as MCli
class IO_mongo(object):
	conn={'host':'localhost', 'ip':'27017'}

	def __init__(self, db='twtr_db', coll='twtr_coll', **conn ):
		# Connects to the MongoDB server
		self.client = MCli(**conn)
		self.db = self.client[db]
		self.coll = self.db[coll]

	def save(self, data):
		# Insert to collection in db
		return self.coll.insert(data)

	def load(self, return_cursor=False, criteria=None,projection=None):
		if criteria is None:
			criteria = {}
		if projection is None:
			cursor = self.coll.find(criteria)
		else:
			cursor = self.coll.find(criteria, projection)

		if return_cursor:
			return cursor
		else:
			return [ item for item in cursor ]