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

3. Run processData.py

   ```
   python processData.py
   ```

   **NOTE:** This will process the **entire** dataset (6gb) if you let it run forever. This takes a long time. Interrupting after 50 iterations still gives reasonable development accuracy (RMSE 5.5)

4. Run randomForest.py

   ```
   python randomForest.py
   ```

   ​