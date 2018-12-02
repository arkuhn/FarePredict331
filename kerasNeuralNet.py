import numpy
import pandas as pd
from keras.models import Sequential
from keras.layers import Dense
from keras import backend as k
from keras.wrappers.scikit_learn import KerasRegressor
from keras.callbacks import EarlyStopping
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import KFold
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from math import sqrt

# load dataset
train_data = pd.read_csv("train_processed.csv")
train_X = train_data.drop(columns=['fare_amount'])
train_y = train_data[['fare_amount']]

#create model
model = Sequential()

#get number of columns in training data
n_cols = train_X.shape[1]

#add model layers
model.add(Dense(1024, activation='relu', input_shape=(n_cols,)))
model.add(Dense(512, activation='relu'))
model.add(Dense(256, activation='relu'))
model.add(Dense(1))

def root_means_squared_error(y_true, y_pred):
    return k.sqrt(k.mean(k.square(y_pred - y_true)))
#compile model using mse as a measure of model performance
model.compile(optimizer='adam', loss=root_means_squared_error)

#set early stopping monitor so the model stops training when it won't improve anymore
early_stopping_monitor = EarlyStopping(patience=3)
#train model
model.fit(train_X, train_y, validation_split=0.2, epochs=30, callbacks=[early_stopping_monitor])



#utility function for kaggle submission
def make_submission(model):
    test_data_x = pd.read_csv("test_processed.csv")
    submission = (pd.read_csv("sample_submission.csv"))
    submission = submission.drop(columns=['fare_amount'])
    test_y_predictions = model.predict(test_data_x)
    test_y_predictions_df = pd.DataFrame(test_y_predictions)
    print(test_y_predictions_df.head())
    submission = submission.assign(fare_amount=test_y_predictions_df)
    #submission = pd.concat([keys, test_y_predictions_df], ignore_index=True)
    submission.to_csv("submission.csv", index=False)