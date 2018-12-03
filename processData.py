from datetime import datetime
import geopy.distance
import pandas as pd
import numpy as np
import holidays

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

def isRushour(dt):
    """
    4pm - 6pm -> Military -> 16 - 19
    5am - 9am -> Military -> 5 - 9
    """

    if ((dt.hour >= 5 and dt.hour <= 9) or (dt.hour >= 16 and dt.hour <= 19)):
        return 1
    return 0

def isWeekend(dt):
    if (dt.weekday() < 5):
        return 0
    return 1

def isHoliday(dt):
    #[(month, day), (month, day)...]
    us_holidays = holidays.UnitedStates()
    if datetime(dt.year, dt.month, dt.day) in us_holidays:
        return 1
    return 0

def processDates(datetimeString):
    dtObject = datetime.strptime(datetimeString, '%Y-%m-%d %H:%M:%S %Z')

    return (isRushour(dtObject), isWeekend(dtObject), isHoliday(dtObject))

def calculateDistance(lon1, lat1, lon2, lat2):
    coords1 = (lat1, lon1)
    coords2 = (lat2, lon2)

    #The Vincenty distance apparently is more accurate than the Haversine formula
    distance = geopy.distance.vincenty(coords1, coords2).km

    return distance

def normalizePassengerCount(count):
    return count / MAX_PASSENGERS

def processData(row):
    lon1 = row['pickup_longitude']
    lat1 = row['pickup_latitude']

    lat2 = row['dropoff_latitude']
    lon2 = row['dropoff_longitude']

    dt = row['pickup_datetime']

    #Extract date time features
    isRushhour, isWeekend, isHoliday = processDates(dt)

    #Consolidate lat/lons into distance
    distance = calculateDistance(lon1, lat1, lon2, lat2)

    normalizedPC = normalizePassengerCount(row['passenger_count'])

    return (isRushhour, isWeekend, isHoliday, normalizedPC, distance)

def main():
    count = 0
    #Read and clean features by chunk
    print(datetime.now())
    for chunk in pd.read_csv('train.csv', chunksize=10000):
        print('Processing chunk ' + str(count))
        #Clean outliers, incomplete, bad lat/lons
        featureFrame = cleanData(chunk)

        #Engineer features
        featureFrame['isRushHour'], featureFrame['isWeekend'], featureFrame['isHoliday'], featureFrame['normalizedPC'], featureFrame['distance'] = zip(*featureFrame.apply(processData, axis=1))

        #Drop leftover raw data
        featureFrame.drop(['key', 'pickup_latitude', 'pickup_longitude', 'dropoff_latitude', 'dropoff_longitude', 'pickup_datetime', 'passenger_count'], axis = 1, inplace=True)

        if(count == 0):
            featureFrame.to_csv('train_processed.csv', mode='a', header=True, index=False)
        else:
            featureFrame.to_csv('train_processed.csv', mode='a', header=False, index=False)
        count += 1

main()
print(datetime.now())
