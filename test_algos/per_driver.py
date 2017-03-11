from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from perceptron import Perceptron
from sklearn.metrics import accuracy_score
import numpy as np


def main():
	data = load_iris()
	data = data.data[:100,:]
	target = load_iris().target[:100]
	print(data)
	print(target)
	print(type(target))
	
	target = np.where(target == 'Iris-setosa',-1,1)
	print(type(target))
	'''
	X_train,X_test,y_train,y_test = train_test_split(data,target,test_size=0.4,random_state = 0)
	p = Perceptron()
	p.fit(X_train,y_train)
	predictions = p.predict(X_test)
	print(accuracy_score(predictions,y_test))
	'''

if __name__ == "__main__":
	main()