import pandas as pd
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
def convertDegreesToMeters(meters):
    return 111139*meters

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
                print("\n --> Found DC: " + str(record.get('properties')) + "\n")
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
def isPointInDC(lat, long, shape):
   point = Point(lat, long)
   polygon = Polygon(shape)
   #print(polygon.contains(point))
   return(polygon.contains(point))
   
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
# Loop through x EVENLY spaced points within DC, and for each, compute
# the number of crimes within a fixed radius. Save each value in a pandas data 
# frame.       
def getRankingData(pointList):
    
    ### CONVERT INPUT LIST TO PANDAS DATA FRAME ###   
    pointListDataFrame = pd.DataFrame(pointList, columns=(["longitude", "latitude"]))
    
    longMin, longMax = getLatLongRange(pointList, "longitude")
    latMin,  latMax  = getLatLongRange(pointList, "latitude")
    
    numHorizontalSlices = 100
    
    # Divide DC into 100 horizontal slices
    latInt = (latMax-latMin)/numHorizontalSlices
    
    currentLat = latMax
    longitudeSum = 0
    
    for x in range(0, numHorizontalSlices):

       # get points between currentLat and currentLat plus latInt
       tmpPoints = pointListDataFrame[pointListDataFrame['longitude'].between(currentLat, currentLat-latInt)]
       
       # get max and min longitude
       # determine range and add to sum
       currentLat -= latInt


##############################################################################  

# Gives list of latitudes and longitudes for DC boundary
# of type 'polygon'.
DC = getShapeFileForDC()

crimeData = getCrimeData()

offense_value_counts = crimeData["OFFENSE"].value_counts()

if False:
    
   isPointInDC(-77.119759, 38.934343, DC)
    
   countCrimesInArea(
      lat            = 38.9014829636, 
      long           = -76.9332371122,
      data           = crimeData,
      radiusInMeters = 1000
   )





















    
    
    
    
    
    
    
