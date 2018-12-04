import numpy
import pandas as pd
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


def root_means_squared_error(y_true, y_pred):
        return k.sqrt(k.mean(k.square(y_pred - y_true)))

def load_data():
    train_data = pd.read_csv("train_processed.csv")
    train_X = train_data.drop(columns=['fare_amount'])
    train_y = train_data[['fare_amount']]
    n_cols = train_X.shape[1]
    return (train_X, train_y, n_cols)

def load_or_make_model(n_cols):
    model = Path("keras_model.h5")
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
        model = load_model('keras_model.h5', custom_objects={'root_means_squared_error': root_means_squared_error})
    
    return model


def train(model, train_X, train_y):
    history = model.fit(train_X, train_y, validation_split=0.2, shuffle=True, epochs=60)
    model.save('keras_model.h5')
    return history


#utility function for kaggle submission
def make_kaggle_submission(model):
    test_data_x = pd.read_csv("test_processed.csv")
    submission = (pd.read_csv("sample_submission.csv"))
    submission = submission.drop(columns=['fare_amount'])
    test_y_predictions = model.predict(test_data_x)
    test_y_predictions_df = pd.DataFrame(test_y_predictions)
    print(test_y_predictions_df.head())
    submission = submission.assign(fare_amount=test_y_predictions_df)
    #submission = pd.concat([keys, test_y_predictions_df], ignore_index=True)
    submission.to_csv("submission.csv", index=False)

def graph_model_results(history):
    plt.plot(history.history['loss'])
    plt.plot(history.history['val_loss'])
    plt.title('model loss')
    plt.ylabel('loss')
    plt.xlabel('epoch')
    plt.legend(['train', 'test'], loc='upper left')
    plt.show()

train_X, train_y, n_cols = load_data()
model = load_or_make_model(n_cols)
results = train(model, train_X, train_y)
graph_model_results(results)
make_submission(model)
