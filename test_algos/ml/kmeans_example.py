
from __future__ import print_function

# $example on$
from pyspark.ml.clustering import KMeans
# $example off$

from pyspark.sql import SparkSession



if __name__ == "__main__":

    spark = SparkSession\
        .builder\
        .appName("PythonKMeansExample")\
        .getOrCreate()

    # $example on$
    # Loads data.
    dataset = spark.read.format("libsvm").load("data/mllib/sample_kmeans_data.txt")

    # Trains a k-means model.
    kmeans = KMeans().setK(2).setSeed(1)
    model = kmeans.fit(dataset)

    # Evaluate clustering by computing Within Set Sum of Squared Errors.
    wssse = model.computeCost(dataset)
    print("Within Set Sum of Squared Errors = " + str(wssse))

    # Shows the result.
    centers = model.clusterCenters()
    print("Cluster Centers: ")
    for center in centers:
        print(center)
    # $example off$

    spark.stop()
