from pyspark import SparkContext
sc = SparkContext("local", "Simple App")

from pyspark.mllib.clustering import KMeans, KMeansModel
from numpy import array
from random import randrange
from math import sqrt


# Generate the observations -----------------------------------------------------
n_in_each_group = 10   # how many observations in each group
n_of_feature = 5 # how many features we have for each observation

observation_group_1=[]
for i in range(n_in_each_group*n_of_feature):
    observation_group_1.append(randrange(5, 8))

observation_group_2=[]
for i in range(n_in_each_group*n_of_feature):
    observation_group_2.append(randrange(55, 58))

observation_group_3=[]
for i in range(n_in_each_group*n_of_feature):
    observation_group_3.append(randrange(105, 108))

data = array([observation_group_1, observation_group_2, observation_group_3]).reshape(n_in_each_group*3, 5)
data = sc.parallelize(data)


# Run the K-Means algorithm -----------------------------------------------------


# Build the K-Means model
clusters = KMeans.train(data, 3, maxIterations=10, initializationMode="random")  # the initializationMode can also be "k-means||" or set by users.

# Collect the clustering result
result=data.map(lambda point: clusters.predict(point)).collect()
print result

# Evaluate clustering by computing Within Set Sum of Squared Errors
def error(point):
    center = clusters.centers[clusters.predict(point)]
    return sqrt(sum([x**2 for x in (point - center)]))

WSSSE = data.map(lambda point: error(point)).reduce(lambda x, y: x + y)
print("Within Set Sum of Squared Error = " + str(WSSSE))