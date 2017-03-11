# the two lines below are added so that this code can be run as a self-containd application.
from pyspark import SparkContext
sc = SparkContext("local", "Simple App")

# load the necessary modules
from pyspark.mllib.regression import LabeledPoint, LinearRegressionWithSGD
from pyspark.mllib.evaluation import RegressionMetrics

# Load and parse the data
def parsePoint(line):
    values = [float(x) for x in line.replace(',', ' ').split(' ')]
    return LabeledPoint(values[0], values[1:])

data = sc.textFile("data/mllib/ridge-data/lpsa.data")
parsedData = data.map(parsePoint)


# split the data into two sets for training and testing
# Here I have set the seed so that I can reproduce the result
(trainingData, testData) = parsedData.randomSplit([0.7, 0.3], seed=100)


# Build the model
model = LinearRegressionWithSGD.train(trainingData)


# Evaluate the model on training data
# --- Point 1 ---
Preds = testData.map(lambda p: (float(model.predict(p.features)), p.label))
MSE = Preds.map(lambda (v, p): (v - p)**2).reduce(lambda x, y: x + y) / Preds.count()
print("Mean Squared Error = " + str(MSE))
print("\n")

# --- Point 2 ---
# More about model evaluation and regression analysis
# Instantiate metrics object
metrics = RegressionMetrics(Preds)

# Squared Error
print("MSE = %s" % metrics.meanSquaredError)
print("RMSE = %s" % metrics.rootMeanSquaredError)

# R-squared
print("R-squared = %s" % metrics.r2)

# Mean absolute error
print("MAE = %s" % metrics.meanAbsoluteError)

# Explained variance
print("Explained variance = %s" % metrics.explainedVariance)