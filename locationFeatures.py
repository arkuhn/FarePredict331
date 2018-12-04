import geopy.distance

nyc_boroughs={
    'manhattan':{
        'min_lng':-74.0479,
        'min_lat':40.6829,
        'max_lng':-73.9067,
        'max_lat':40.8820
    },
    
    'queens':{
        'min_lng':-73.9630,
        'min_lat':40.5431,
        'max_lng':-73.7004,
        'max_lat':40.8007
    },

    'brooklyn':{
        'min_lng':-74.0421,
        'min_lat':40.5707,
        'max_lng':-73.8334,
        'max_lat':40.7395
    },

    'bronx':{
        'min_lng':-73.9339,
        'min_lat':40.7855,
        'max_lng':-73.7654,
        'max_lat':40.9176
    },

    'staten_island':{
        'min_lng':-74.2558,
        'min_lat':40.4960,
        'max_lng':-74.0522,
        'max_lat':40.6490
    } 
}

airports = {
    'jfk': {
        'min_lng':-73.8336,
        'min_lat':40.6087,
        'max_lng':-73.7313,
        'max_lat':40.6754
    },

    'newark': {
        'min_lng':-74.2278,
        'min_lat':40.6530,
        'max_lng':-74.1254,
        'max_lat':40.7197
    }
}

def calculateDistance(lon1, lat1, lon2, lat2):
    coords1 = (lat1, lon1)
    coords2 = (lat2, lon2)

    #The Vincenty distance apparently is more accurate than the Haversine formula
    distance = geopy.distance.vincenty(coords1, coords2).km

    return distance

def isAirport(lon1, lat1, lon2, lat2):
    jfk = airports['jfk']
    newark = airports['newark']
    if (lon1 <= jfk['max_lng'] and lon1 >= jfk['min_lng'] and 
        lat1 >= jfk['min_lat'] and lat1 <= jfk['max_lat']):
        return 1
    elif (lon2 <= jfk['max_lng'] and lon2 >= jfk['min_lng'] and 
        lat2 >= jfk['min_lat'] and lat2 <= jfk['max_lat']):
        return 1
    elif (lon1 <= newark['max_lng'] and lon1 >= newark['min_lng'] and 
        lat1 >= newark['min_lat'] and lat1 <= newark['max_lat']):
        return 1
    elif (lon2 <= newark['max_lng'] and lon2 >= newark['min_lng'] and 
        lat2 >= newark['min_lat'] and lat2 <= newark['max_lat']):
        return 1
    else:
        return 0

def isManhattan(lon1, lat1, lon2, lat2):
    pickup = 0
    dropoff = 0
    mahattan = nyc_boroughs['manhattan']
    if (lon1 <= mahattan['max_lng'] and lon1 >= mahattan['min_lng'] and 
        lat1 >= mahattan['min_lat'] and lat1 <= mahattan['max_lat']):
        pickup = 1
    if (lon2 <= mahattan['max_lng'] and lon2 >= mahattan['max_lng'] and 
        lat2 >= mahattan['min_lat'] and lat2 <= mahattan['max_lat']):
        dropoff = 1
    return (pickup, dropoff)

def isQueens(lon1, lat1, lon2, lat2):
    pickup = 0
    dropoff = 0
    queens = nyc_boroughs['queens']
    if (lon1 <= queens['max_lng'] and lon1 >= queens['min_lng'] and 
        lat1 >= queens['min_lat'] and lat1 <= queens['max_lat']):
        pickup = 1
    if (lon2 <= queens['max_lng'] and lon2 >= queens['max_lng'] and 
        lat2 >= queens['min_lat'] and lat2 <= queens['max_lat']):
        dropoff = 1
    return (pickup, dropoff)

def isBronx(lon1, lat1, lon2, lat2):
    pickup = 0
    dropoff = 0
    bronx = nyc_boroughs['bronx']
    if (lon1 <= bronx['max_lng'] and lon1 >= bronx['min_lng'] and 
        lat1 >= bronx['min_lat'] and lat1 <= bronx['max_lat']):
        pickup = 1
    if (lon2 <= bronx['max_lng'] and lon2 >= bronx['max_lng'] and 
        lat2 >= bronx['min_lat'] and lat2 <= bronx['max_lat']):
        dropoff = 1
    return (pickup, dropoff)

def isBrooklyn(lon1, lat1, lon2, lat2):
    pickup = 0
    dropoff = 0
    brooklyn = nyc_boroughs['brooklyn']
    if (lon1 <= brooklyn['max_lng'] and lon1 >= brooklyn['min_lng'] and 
        lat1 >= brooklyn['min_lat'] and lat1 <= brooklyn['max_lat']):
        pickup = 1
    if (lon2 <= brooklyn['max_lng'] and lon2 >= brooklyn['max_lng'] and 
        lat2 >= brooklyn['min_lat'] and lat2 <= brooklyn['max_lat']):
        dropoff = 1
    return (pickup, dropoff)

def isStaten(lon1, lat1, lon2, lat2):
    pickup = 0
    dropoff = 0
    staten_island = nyc_boroughs['staten_island']
    if (lon1 <= staten_island['max_lng'] and lon1 >= staten_island['min_lng'] and 
        lat1 >= staten_island['min_lat'] and lat1 <= staten_island['max_lat']):
        pickup = 1
    if (lon2 <= staten_island['max_lng'] and lon2 >= staten_island['max_lng'] and 
        lat2 >= staten_island['min_lat'] and lat2 <= staten_island['max_lat']):
        dropoff = 1
    return (pickup, dropoff)

def processLocation(lat1, lon1, lat2, lon2):
    distance = calculateDistance(lon1, lat1, lon2, lat2)
    airport = isAirport(lon1, lat1, lon2, lat2)
    isManhattanPickup, isManhattanDropOff = isManhattan(lon1, lat1, lon2, lat2)
    isQueensPickup, isQueensDropOff = isQueens(lon1, lat1, lon2, lat2)
    isBronxPickup, isBronxDropOff = isBronx(lon1, lat1, lon2, lat2)
    isStatenPickup, isStatenDropOff = isStaten(lon1, lat1, lon2, lat2)
    isBrooklynPickup, isBrooklynDropOff = isBrooklyn(lon1, lat1, lon2, lat2)

    return distance, airport, isManhattanPickup, isManhattanDropOff, isQueensPickup, isQueensDropOff, isBronxPickup, isBronxDropOff, isStatenPickup, isStatenDropOff, isBrooklynPickup, isBrooklynDropOff