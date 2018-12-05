from datetime import datetime
import pandas as pd
import numpy as np
import holidays
import locationFeatures
import timeFeatures


#NYC Bounding box
LONGITUDE_MIN = -74.263242
LONGITUDE_MAX = -72.986532
LATITUDE_MIN = 40.568973
LATITUDE_MAX = 41.709555

MIN_PASSENGERS = 1
MAX_PASSENGERS = 7

def cleanData(features):
    cleanedFeatures = features[
                                (features.fare_amount > 0) &
                                (features.passenger_count <= 7) &
                                (features.passenger_count > 0) &
                                (features.pickup_latitude >= LATITUDE_MIN) &
                                (features.pickup_latitude <= LATITUDE_MAX) &
                                (features.pickup_longitude >= LONGITUDE_MIN) &
                                (features.pickup_longitude <= LONGITUDE_MAX) &
                                (features.dropoff_latitude >= LATITUDE_MIN) &
                                (features.dropoff_latitude <= LATITUDE_MAX) &
                                (features.dropoff_longitude >= LONGITUDE_MIN) &
                                (features.dropoff_longitude <= LONGITUDE_MAX)
                            ]
    return cleanedFeatures

def normalizePassengerCount(count):
    return round(count / MAX_PASSENGERS, 3)

def processData(row):
    lon1 = row['pickup_longitude']
    lat1 = row['pickup_latitude']
    lat2 = row['dropoff_latitude']
    lon2 = row['dropoff_longitude']
    dt = row['pickup_datetime']
    pc = row['passenger_count']

    #Extract date time features
    (isRushhour, isWeekend, isHoliday, nHour,
    nDay, nMonth, nYear) = timeFeatures.processDates(dt)

    #Extract route features
    (nBearing, vDistance, eDistance, isAirport, isManhattanPickup, isManhattanDropOff, 
    isQueensPickup, isQueensDropOff, isBronxPickup, 
    isBronxDropOff, isStatenPickup, isStatenDropOff, 
    isBrooklynPickup, isBrooklynDropOff) = locationFeatures.processLocation(lat1, lon1, lat2, lon2)

    #Passenger count feature
    normalizedPC = normalizePassengerCount(pc)

    return (isRushhour, isWeekend, isHoliday, nHour, nDay, nMonth, 
            nYear, normalizedPC, nBearing, vDistance, eDistance, isAirport, isManhattanPickup, 
            isManhattanDropOff, isQueensPickup, isQueensDropOff, 
            isBronxPickup, isBronxDropOff, isStatenPickup, 
            isStatenDropOff, isBrooklynPickup, isBrooklynDropOff)

def main():
    count = 0
    linesRead = 0
    #Read and clean features by chunk
    print(datetime.now())
    for chunk in pd.read_csv('train.csv', chunksize=5000):
        #linesRead += 100000
        #if (linesRead <= 40000000):
        #    continue
        print('Processing chunk ' + str(count))
        #Clean outliers, incomplete, bad lat/lons
        featureFrame = cleanData(chunk)

        """
        Engineer features
        """
        (
        #Datetime
        featureFrame['isRushHour'], featureFrame['isWeekend'], featureFrame['isHoliday'],
        featureFrame['nHour'], featureFrame['nDay'], featureFrame['nMonth'], featureFrame['nYear'],
        
        #Passenger count
        featureFrame['normalizedPC'], 

        #Location
        featureFrame['nBearing'], featureFrame['vDistance'], featureFrame['eDistance'], featureFrame['isAirport'], featureFrame['isManhattanPickup'], 
        featureFrame['isManhattanDropOff'], featureFrame['isQueensPickup'], featureFrame['isQueensDropOff'], featureFrame['isBronxPickup'],
        featureFrame['isBronxDropOff'], featureFrame['isStatenPickup'], featureFrame['isStatenDropOff'],
        featureFrame['isBrooklynPickup'], featureFrame['isBrooklynDropOff']
        ) = zip(*featureFrame.apply(processData, axis=1))

        #Drop leftover raw data
        featureFrame.drop(['key', 'pickup_latitude', 'pickup_longitude', 'dropoff_latitude', 'dropoff_longitude', 'pickup_datetime', 'passenger_count'], axis = 1, inplace=True)

        if(count == 0):
            featureFrame.to_csv('train_processed.csv', mode='a', header=True, index=False)
        else:
            featureFrame.to_csv('train_processed.csv', mode='a', header=False, index=False)
        count += 1

main()
print(datetime.now())
