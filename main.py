import pandas as pd

###############################################################################
#
# Multiply the degrees of separation of longitude and latitude by 111,139 to
#  get the corresponding linear distances in meters.
#
# Data: https://opendata.dc.gov/datasets/DCGIS::crime-incidents-in-2020/about
#
# OFFENSE variable includes: 
#         'MOTOR VEHICLE THEFT', 'THEFT/OTHER', 'BURGLARY', 'THEFT F/AUTO',
#         'ROBBERY', 'ASSAULT W/DANGEROUS WEAPON', 'HOMICIDE', 'SEX ABUSE',
#         'ARSON'
#
# METHOD variable includes: "GUN", "KNIFE", "OTHERS"
#
# SHIFT variable includes 'DAY', 'EVENING', 'MIDNIGHT'
#
# need to compute # of crimes/total area
#
###############################################################################

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

countCrimesInArea(
   lat            = 38.9014829636, 
   long           = -76.9332371122,
   data           = data,
   radiusInMeters = 1000
)





















    
    
    
    
    
    
    
