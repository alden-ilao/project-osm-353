import numpy as np
import pandas as pd
import sys

from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline

from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier


def score_tags(x, all_tags):

	total_score = 0;

	for tag in x:
		total_score += (all_tags.index(tag) + 1) **2

	# print(total_score)
	return total_score


def main():

	data = pd.read_json(sys.argv[1], orient='records', lines=True, precise_float=True)

	# https://stackoverflow.com/questions/17218139/print-all-unique-values-in-a-python-dictionary
	# get all the unique keys in 'tags'
	raw_tags = data['tags'].values
	all_tags = list(set(val for dic in raw_tags for val in dic.keys()))

	print(all_tags)


	# tag values
	X = pd.DataFrame()
	X['tags'] = data['tags'].apply(score_tags, all_tags=all_tags)
	X['amenity'] = data['amenity']
	X = X[X.tags > 0]

	X_tags = X['tags']

	# amenity type
	y = pd.DataFrame()
	y = X['amenity']

	X.reset_index(inplace=True, drop=True)
	y.reset_index(inplace=True, drop=True)

	print(X)
	print(y)


	X_train, X_valid, y_train, y_valid = train_test_split(X['tags'].values.reshape(-1 , 1), y.values, test_size=0.20)

	bayes_model = make_pipeline(GaussianNB())
	rf_model = make_pipeline(RandomForestClassifier(n_estimators=1000))
	knn_model = make_pipeline(KNeighborsClassifier(n_neighbors=3))

	bayes_model.fit(X_train, y_train)
	rf_model.fit(X_train, y_train)
	knn_model.fit(X_train, y_train)

	print(bayes_model.score(X_valid, y_valid))
	print(rf_model.score(X_valid, y_valid))
	print(knn_model.score(X_valid, y_valid))

	# [7942:7962] - all bench

	print(y[12251:12281])

	print(bayes_model.predict(X['tags'].loc[12251:12281].values.reshape(-1 , 1)))
	print(rf_model.predict(X['tags'].loc[12251:12281].values.reshape(-1 , 1)))
	print(knn_model.predict(X['tags'].loc[12251:12281].values.reshape(-1 , 1)))
	# print(knn_model.predict(X[7952:7962]))


if __name__ == '__main__':
    main()
