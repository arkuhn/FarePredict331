import numpy
import pandas as pd
import time
import json
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Dropout
from keras.models import load_model
from keras.callbacks import Callback
from keras import backend as k
from keras.wrappers.scikit_learn import KerasRegressor
from keras.callbacks import EarlyStopping
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import KFold
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from math import sqrt
from pathlib import Path
import matplotlib.pyplot as plt

#Define custom RMSE to use as optimization function
def root_means_squared_error(y_true, y_pred):
        return k.sqrt(k.mean(k.square(y_pred - y_true)))

#Create input and output layers from data
def prepare_data(data):
    train_X = data.drop(columns=['fare_amount'])
    train_y = data[['fare_amount']]
    n_cols = train_X.shape[1]
    return (train_X, train_y, n_cols)

#Load model from disk or create from scratch
def load_or_make_model(n_cols, modelfile):
    model = Path(modelfile)
    if (not model.is_file()):
        model = Sequential()
        model.add(Dense(2048, activation='relu', input_shape=(n_cols,)))
        model.add(Dense(1024, activation='relu'))
        model.add(Dense(512, activation='relu'))
        model.add(Dense(420, activation='relu'))
        model.add(Dense(256, activation='relu'))
        model.add(Dense(128, activation='relu'))
        model.add(Dense(69, activation='relu'))
        model.add(Dense(1))
        model.compile(optimizer='adam', loss=root_means_squared_error)
    else:
        model = load_model(modelfile, custom_objects={'root_means_squared_error': root_means_squared_error})
    
    return model

#Save the history of model for graphing later
def save_history(results):
    timestr = time.strftime("%Y%m%d-%H%M%S")
    with open('history' + timestr + '.json', 'w') as f:
        json.dump(results.history, f)

#Train by loading the entire file
def train(filename, modelfile):
    data = pd.read_csv(filename)
    train_X, train_y, n_cols = prepare_data(data)
    model = load_or_make_model(n_cols, modelfile)
    results = model.fit(train_X, train_y, validation_split=0.2, shuffle=True, epochs=60)
    model.save(modelfile)
    save_history(results)

#Train by loading batches of file
def batch_train(filename, modelfile):
    epochs = 2
    chunk_size = 100000
    for epoch in range(1, epochs+1):
        print('epoch ' + str(epoch))
        counter = 0
        for data in pd.read_csv(filename, chunksize=chunk_size):
            counter += 1
            print('batch ' + str(counter))
            train_X, train_y, n_cols = prepare_data(data)
            model = load_or_make_model(n_cols, modelfile)
            results = model.fit(train_X, train_y, validation_split=0.2, shuffle=True)
            model.save(modelfile)

#utility function for kaggle submission
def make_kaggle_submission(modelfile):
    model = load_model(modelfile, custom_objects={'root_means_squared_error': root_means_squared_error})
    test_data_x = pd.read_csv("test_processed.csv")
    submission = (pd.read_csv("sample_submission.csv"))
    submission = submission.drop(columns=['fare_amount'])
    test_y_predictions = model.predict(test_data_x)
    test_y_predictions_df = pd.DataFrame(test_y_predictions)
    submission = submission.assign(fare_amount=test_y_predictions_df)
    submission.to_csv("submission.csv", index=False)

#utility function for graphing loss history
def graph_model_results(history):
    plt.plot(history.history['loss'])
    plt.plot(history.history['val_loss'])
    plt.title('model loss')
    plt.ylabel('loss')
    plt.xlabel('epoch')
    plt.legend(['train', 'test'], loc='upper left')
    plt.show()


FILE_TO_LOAD='train_processed.csv'
MODEL_FILENAME='keras_model_c.h5'
#train(FILE_TO_LOAD, MODEL_FILENAME)
#batch_train(FILE_TO_LOAD, MODEL_FILENAME)
#make_kaggle_submission(MODEL_FILENAME)