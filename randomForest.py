import pandas as pd
import numpy as np 
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
from math import sqrt
#Read features
features = pd.read_csv('train_processed.csv')


#Target
labels = np.array(features['fare_amount'])

#Drop the target from features
features= features.drop('fare_amount', axis = 1)

# Convert to numpy array
features = np.array(features)

"""
Since the provided training data doesn't include
the target value, the fare, we will split our own
for validation purposes from train.csv
"""
train_features, test_features, train_labels, test_labels = train_test_split(features, labels, test_size = 0.25, random_state = 42)

# Instantiate model with 1000 decision trees
rf = RandomForestRegressor(n_estimators = 2000, random_state = 42)
# Train the model on training data
rf.fit(train_features, train_labels);

# Use the forest's predict method on the test data
predictions = rf.predict(test_features)

print('RMSE: ' + str(sqrt(mean_squared_error(test_labels, predictions))) + ' dollars')