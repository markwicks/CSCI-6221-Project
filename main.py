import pandas as pd
import numpy as np
import fiona
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon


data_path = "/Users/markwicks/Desktop/advanced software paradigms/CSCI-6221-Project/data/"

###############################################################################

def getCrimeData():
    data = pd.read_csv(data_path + "crime_2020.csv")
    data = data[["LATITUDE", "LONGITUDE", "SHIFT", "START_DATE", "METHOD", "OFFENSE"]]
    return(data)

###############################################################################
# Latitude and longitude are in degrees
# https://sciencing.com/convert-latitude-longtitude-feet-2724.html
def convertDegreesToMeters(degrees):
    return(111139*degrees)

###############################################################################
def convertMetersToDegrees(meters):
    return(meters/111139)

###############################################################################
def getDistance(lat1, long1, lat2, long2):
    return ((lat2-lat1)**2 + (long2-long1)**2)**0.5

###############################################################################
def countCrimesInArea(lat, long, data, radiusInMeters):
    
    counter = 0
    
    for x in range(0, data.shape[0]):
        
        lat1 = data.iloc[x]["LATITUDE"]
        long1 = data.iloc[x]["LONGITUDE"]
        
        if False:
           print(" x: " + str(x) + " Input lat: " +  str(lat1) +
                 " Input long: " + str(long1) + "  Lat from data: " + 
                 str(lat1) + " Long from data: " + str(long1) + "\n"
           )
        
        dist = getDistance(lat1, long1, lat, long)
        
        if convertDegreesToMeters(dist) < radiusInMeters:
           counter = counter+1
           print(dist)
           
    return counter
    
###############################################################################
# Returns the boundary for DC, as a set of lat/long points.
# This can be used for a GUI, looping through areas in DC, and checking
# whether a point (latitude & longitude) is inside DC.
# - The first value in each point returned is the longitude, and the second
#   is the latitude.
def getShapeFileForDC(returnDataFrame=False):
    with fiona.open(data_path + "/cb_2018_us_state_500k/cb_2018_us_state_500k.shp") as c:
         for record in c:
             if record.get('properties').get('STATEFP') == '11':
                #print("\n --> Found DC: " + str(record.get('properties')) + "\n")
                coord_list = record.get('geometry').get('coordinates')
                break
            
    if returnDataFrame==True:
       coord_list_string = str(coord_list[0]).split('),')
       d = []
       for record in coord_list_string:
           lat_and_long = record.replace('[(', '').split(',')
           d.append(lat_and_long)
        
       return(pd.DataFrame(d))
   
    else:
        return(coord_list[0])

###############################################################################
# Returns boolean value indicating whether the point input is inside a polygon.
# - lat is Latitude
# - long is Longitude
# - Shape is a list of the latitude and longitude of each point giving the 
#   outline of an area (in our case, DC)
def isPointInDC(lat, long, shape, output):
    
   point = Point(long, lat)
   polygon = Polygon(shape)
   result = polygon.contains(point)
   
   if output==True:
      print(" --> Lat: " + str(lat) +  "  Long: " + str(long)) 
      print(" --> In DC?: " + str(result))
      
   return(result)
   
###############################################################################
# Returns the min and max value of the point list input.
def getLatLongRange(pointList, coordType):
    
    if coordType not in ["latitude", "longitude"]:
       raise Exception("Error: Invalid argument to coordType argument")
        
    min = float('inf')
    max = float('-Inf')
    
    for point in pointList:
        
        # Longitude
        if coordType=="longitude":
           val = point[0]
           if val < min:
              min = val
           elif val > max:
              max = val
        # Latitude
        else:
          val = point[1]
          if val < min:
              min = val
          elif val > max:
              max = val  
              
    return(min, max)
          
##############################################################################  
# Overlay square a grid on top of DC, and iterate over each point in the grid, 
# while checking whether each point is in DC. If the point is in DC, count 
# the crimes in the surrounding area and save the result in a dataset.
# When done, output the dataset.
def getRankingData(pointList, crimeData, metersInterval):
    
    longMin, longMax = getLatLongRange(pointList, "longitude")
    latMin,  latMax  = getLatLongRange(pointList, "latitude")
    
    degreesInterval = convertMetersToDegrees(metersInterval) 
    
    # Current longitudinal and latitudinal values in the loop
    currentLong = longMin
    currentLat = latMin
    
    # Counters for number of points in and outside of DC
    in_DC_counter = 0
    not_in_DC_counter = 0
    
    latArray = np.arange(longMin, longMax, degreesInterval)
    longArray = np.arange(latMin, latMax, degreesInterval)
    
    ##############################
    # Work laterally (longitude) #
    ##############################
    for currentLong in longArray:
           
       #################################
       # Working vertically (latitude) #
       ##################################
       for currentLat in latArray:
           
           if False:
              print(" --> Current Lat: " + str(currentLat) + 
                    "  Max Lat: " + str(latMax) + "\n")
              print(" --> In DC. Counter: " + str(in_DC_counter))
              print(" --> Not in DC. Counter: " + str(not_in_DC_counter))
                
           if isPointInDC(currentLong, currentLat, pointList, False) == True:
               
              x = countCrimesInArea(
                lat            = currentLat, 
                long           = currentLong,
                data           = crimeData,
                radiusInMeters = metersInterval
              )
              
              in_DC_counter += 1
           else:
              not_in_DC_counter += 1
          
           currentLat += degreesInterval
           
       currentLong += degreesInterval
       
    return in_DC_counter, not_in_DC_counter


##############################################################################  

# Gives list of latitudes and longitudes for DC boundary
# of type 'polygon'.
DC_shape_file = getShapeFileForDC()

crimeData = getCrimeData()

offense_value_counts = crimeData["OFFENSE"].value_counts()

numInDC, numNotInDC = getRankingData(DC_shape_file, crimeData, 1000)

if False:
    
   # lincoln memorial
   isPointInDC(lat=38.889248, long=-77.050636, shape=DC_shape_file, output=True) 
    
   countCrimesInArea(
      lat            = 38.9014829636, 
      long           = -76.9332371122,
      data           = crimeData,
      radiusInMeters = 1000
   )





















    
    
    
    
    
    
    
