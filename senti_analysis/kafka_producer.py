import time
from kafka.common import LeaderNotAvailableError
from kafka.client import KafkaClient
from kafka.producer import SimpleProducer
from datetime import datetime


def print_response(response=None):
	if response:
		print('Error: {0}'.format(response[0].error))
		print('Offset: {0}'.format(response[0].offset))


def main():
	kafka = KafkaClient("localhost:9092")
	producer = SimpleProducer(kafka)
	try:
		time.sleep(5)	
		topic = 'test'
		for i in range(5):
			time.sleep(1)
			msg = 'This is a message sent from the kafka producer: ' \
											+ str(datetime.now().time()) + ' -- '\
														+ str(datetime.now().strftime("%A, %d %B %Y%I:%M%p"))
		print_response(producer.send_messages(topic, msg))
	except LeaderNotAvailableError:
# https://github.com/mumrah/kafka-python/issues/249
		time.sleep(1)
		print_response(producer.send_messages(topic, msg))
	kafka.close()


if __name__ == "__main__":
	main()		