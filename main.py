import pandas as pd
import shapely
import fiona



data_path = "/Users/markwicks/Desktop/advanced software paradigms/CSCI-6221-Project/data/"

###############################################################################

data = pd.read_csv(data_path + "crime_2020.csv")
data["year"] = 2020

data =data[["LATITUDE", "LONGITUDE", "SHIFT", "START_DATE", "METHOD", "OFFENSE"]]

offense_value_counts = data["OFFENSE"].value_counts()

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
def getShapeFileForDC():
    with fiona.open(data_path + "/cb_2018_us_state_500k/cb_2018_us_state_500k.shp") as c:
         for record in c:
             if record.get('properties').get('STATEFP') == '11':
                print("\n --> Found DC: " + str(record.get('properties')) + "\n")
                coord_list = record.get('geometry').get('coordinates')
                break
            
    coord_list_string = str(coord_list[0]).split('),')
    
    d = []
    for record in coord_list_string:
        lat_and_long = record.replace('[(', '').split(',')
        d.append(lat_and_long)
        
    return(pd.DataFrame(d))

###############################################################################

# Gives list of latitudes and longitudes for DC boundary
# of type 'polygon'.
DC = getShapeFileForDC()


if False:
   countCrimesInArea(
      lat            = 38.9014829636, 
      long           = -76.9332371122,
      data           = data,
      radiusInMeters = 1000
   )





















    
    
    
    
    
    
    
