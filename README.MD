# Fare Prediction

Get started

1.  Download and extract the data

    ```
    https://www.kaggle.com/c/new-york-city-taxi-fare-prediction/data
    ```

2.  Install dependencies

    ```
    pip install -r requirements.txt
    ```

3. Clean and process the data for ML training

    ```
    python processData.py
    ```

    **NOTE:** This will process the **entire** dataset (6gb) if you let it run forever. You can get a decent 100,000 lines in 50 iterations/20 seconds

4. Run the model
    -Pick a main function to execute, train or batch_train
    -Util functions include loss graphing and kaggle submission


    -Keras neural network regression:

    ```
    python kerasNeuralNet.py
    ```

   ​
