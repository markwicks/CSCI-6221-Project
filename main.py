import pandas as pd
import numpy as np
import fiona
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon

# Radius in meters. When the user enters a point to generate a crime ranking,
# the program checks within the radius below when counting crimes. Crimes 
# outside the radius are ignored.
RADIUS = 250

# Path where the data sets are saved.
data_path = "/Users/markwicks/Desktop/Mark/Advanced Software Paradigms/CSCI-6221-Project/data/"

###############################################################################
# Read in the crime data set downloaded from the DC website.
def getCrimeData(data_path):
    
    ########
    # 2020 #
    ########
    
    data_2020 = pd.read_csv(data_path + "crime_2020.csv")
    data_2020 = data_2020[["LATITUDE", "LONGITUDE", "SHIFT",
                      "START_DATE", "METHOD", "OFFENSE"]]

    ########
    # 2019 #
    ########
    
    data_2019 = pd.read_csv(data_path + "crime_2019.csv")
    data_2019 = data_2019[["LATITUDE", "LONGITUDE", "SHIFT",
                      "START_DATE", "METHOD", "OFFENSE"]]
    
    ########
    # 2018 #
    ########
    
    data_2018 = pd.read_csv(data_path + "crime_2018.csv")
    data_2018 = data_2018[["LATITUDE", "LONGITUDE", "SHIFT",
                      "START_DATE", "METHOD", "OFFENSE"]]
    
    data = data_2020.append(data_2019).append(data_2018)
    
    return(data)

###############################################################################
# Function to convert degrees to meters
# Latitude and longitude are in degrees
# https://sciencing.com/convert-latitude-longtitude-feet-2724.html
def convertDegreesToMeters(degrees):
    return(111139*degrees)

###############################################################################
# Function to convert meters to degrees
def convertMetersToDegrees(meters):
    return(meters/111139)

###############################################################################
# Get Euclidian distance of two points
def getDistance(lat1, long1, lat2, long2):
    return ((lat2-lat1)**2 + (long2-long1)**2)**0.5

###############################################################################
# Given a point (latitude and longitude), count the number of crimes
# in the input radius (in meters). The numbers of each crime type are
# also computed. All info is stored in a dictionary object and returned.
# The 'data' argument should be the crime data downloaded from the DC website.
def countCrimesInArea(latitude, longitude, data, radiusInMeters):
    
    # Counters for the type of offense. Note that sex abuse and arson
    # are too infrequent to be counted, so we put them in 'other'.
    total_number_of_crimes = 0
    theft = 0
    assault = 0
    burglary = 0
    homocide = 0
    robbery = 0
    other = 0
    
    # Loop for each row in the crime data set, and see if it is in the radius.
    # If it is, increase the counter
    for x in range(0, data.shape[0]):
        
        latitude_of_crime  = data.iloc[x]["LATITUDE"]
        longitude_of_crime = data.iloc[x]["LONGITUDE"]

        if False:
           print(" x: " + str(x) + " Input lat: " +  str(latitude_of_crime) +
                 " Input long: " + str(longitude_of_crime) + "  Lat from data: " + 
                 str(latitude_of_crime) + " Long from data: " + str(longitude_of_crime) + "\n"
           )
        
        dist = getDistance(latitude_of_crime, longitude_of_crime, latitude, longitude)
        
        if convertDegreesToMeters(dist) < radiusInMeters:
            
           total_number_of_crimes += 1 
            
           crime = data.iloc[x]['OFFENSE']
           
           if crime in ("THEFT/OTHER", "THEFT F/AUTO", "MOTOR VEHICLE THEFT"):
              theft += 1      
           elif crime == "ASSAULT W/DANGEROUS WEAPON":
              assault += 1
           elif crime == "ROBBERY":
              robbery += 1
           elif crime == "BURGLARY":
              burglary += 1
           elif crime == "HOMOCIDE":
              homocide += 1
           else:
              other += 1
              
    number_of_crimes_dict = {
      "latitude": latitude,
      "longitude": longitude,
      "total_number_of_crimes": total_number_of_crimes,
      "theft": theft, 
      "assault": assault,
      "robbery": robbery,
      "burglary": burglary,
      "homocide": homocide,
      "other": other
    }
      
    return number_of_crimes_dict
    
###############################################################################
# Returns the boundary for DC, as a set of lat/long points.
# This can be used for a GUI, looping through areas in DC, and checking
# whether a point (latitude & longitude) is inside DC.
# - The first value in each point returned is the longitude, and the second
#   is the latitude.
def getShapeFileForDC(data_path, returnDataFrame=False):
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
def isPointInDC(lat, long, shape, output = False):
    
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
def getRankingData(pointList, crimeData, metersInterval, debug=True):
    
    # Use the max/min of lat and long to loop over a rectangular 
    # grid that is overlaid over DC
    longMin, longMax = getLatLongRange(pointList, "longitude")
    latMin,  latMax  = getLatLongRange(pointList, "latitude")
    
    degreesInterval = convertMetersToDegrees(metersInterval) 
    
    # Current longitudinal and latitudinal values in the loop
    currentLong = longMin
    currentLat = latMin
    
    # Counters for number of points in and outside of DC
    # Used for debugging
    in_DC_counter = 0
    not_in_DC_counter = 0
    
    longArray = np.arange(longMin, longMax, degreesInterval)
    latArray  = np.arange(latMin, latMax, degreesInterval)
    
    # Empty data frame that we'll append to below.
    dataframe = pd.DataFrame(
      columns = [
        "latitude", "longitude", "total_number_of_crimes", "theft", 
        "assault", "robbery", "burglary", "homocide", "other"
      ]
    )
    
    ##############################
    # Work laterally (longitude) #
    ##############################
    for currentLong in longArray:
        
       if debug==True:
          print(" --> Current Long: " + str(currentLong))
          print("     Max Long: " + str(longMax))
          print("     In DC. Counter: " + str(in_DC_counter))
          print("     Not in DC. Counter: " + str(not_in_DC_counter))
          print("")
          
       #################################
       # Working vertically (latitude) #
       #################################
       for currentLat in latArray:
           
           # If point is in DC, count the number of crimes in radius.
           if isPointInDC(currentLat, currentLong, pointList, False) == True:
               
              number_of_crimes_dict = countCrimesInArea(
                latitude       = currentLat, 
                longitude      = currentLong,
                data           = crimeData,
                radiusInMeters = metersInterval
              )
              
              # Append to data frame
              dataframe = dataframe.append(number_of_crimes_dict, ignore_index= True)
              
              in_DC_counter += 1
              
           else:
              not_in_DC_counter += 1
          
           currentLat += degreesInterval
           
       currentLong += degreesInterval
       
    # Sort by number of crimes
    (
     dataframe.
     sort_values(by = 'total_number_of_crimes', ascending = True, inplace = True)
    )
 
    return dataframe

##############################################################################
# Generate the dataset used for the crime queries. The dataset output by 
# this function contains info on the number of crimes at each of a certain number
# of evenly spaced points in DC. This dataset is used to generate the percentile 
# crime rankings (e.g. the location is in the 50% percentile of crime).
def makeRankingData(data_path, out_path, metersInterval, debug=False):
    
   # Gives list of latitudes and longitudes for DC boundary
   # of type 'polygon'.
   DC_shape_file = getShapeFileForDC(data_path)

   crimeData = getCrimeData(data_path)

   rankingData = getRankingData(
       pointList      = DC_shape_file,
       crimeData      = crimeData,
       metersInterval = metersInterval,
       debug          = debug
   )

   if out_path is not None: 
      rankingData.to_csv(out_path + "rankingData.csv")
      
   return rankingData

##############################################################################
# A location in DC is input, and the number of crimes within a fixed radius 
# are computed. Then use the ranking dataset to output the rankings (e.g.
# 50% percentile of crime). 
def getQuery(latitude, longitude, data_path, metersInterval, printValues=True):
    
    # Get DC shape file
    pointList = getShapeFileForDC(data_path)
    
    # Check if the point input is inside DC
    if isPointInDC(latitude, longitude, pointList, False) == False:
       print("  ERROR: Point input is not in DC.")
       return
    
    # Read the crime data    
    crimeData = getCrimeData(data_path)
    
    # Count the number of crimes in the radius
    number_of_crimes_dict = countCrimesInArea(
       latitude       = latitude, 
       longitude      = longitude,
       data           = crimeData,
       radiusInMeters = metersInterval
    )
 
    # Read the ranking dataset
    rankingData = pd.read_csv(data_path + "rankingData.csv")
    
    ############################
    ### COMPUTE THE RANKINGS ###
    ############################
    
    num_rows = rankingData.shape[0]
    
    # Total number of crimes
    rankingData.sort_values(by=["total_number_of_crimes"], inplace=True)
    for row_num in range(num_rows):
        if (rankingData.iloc[row_num].total_number_of_crimes >= 
            number_of_crimes_dict['total_number_of_crimes']):
           total_number_of_crimes = str(round(row_num/num_rows*100, 1))
           break
           
    # Theft
    rankingData.sort_values(by=["theft"], inplace=True)
    for row_num in range(num_rows):
        if rankingData.iloc[row_num].theft >= number_of_crimes_dict['theft']: 
           theft = str(round(row_num/num_rows*100, 1))
           break
           
    # Assault
    rankingData.sort_values(by=["assault"], inplace=True)
    for row_num in range(num_rows):
        if rankingData.iloc[row_num].assault >= number_of_crimes_dict['assault']: 
           assault = str(round(row_num/num_rows*100, 1))
           break
           
    # Robbery
    rankingData.sort_values(by=["robbery"], inplace=True)
    for row_num in range(num_rows):
        if rankingData.iloc[row_num].robbery >= number_of_crimes_dict['robbery']: 
           robbery = str(round(row_num/num_rows*100, 1))
           break
           
    # Burglary
    rankingData.sort_values(by=["burglary"], inplace=True) 
    for row_num in range(num_rows):
        if rankingData.iloc[row_num].burglary >= number_of_crimes_dict['burglary']: 
           burglary = str(round(row_num/num_rows*100, 1))
           break
           
    # Burglary
    rankingData.sort_values(by=["homocide"], inplace=True)
    for row_num in range(num_rows):
        if rankingData.iloc[row_num].homocide >= number_of_crimes_dict['homocide']: 
           homocide = str(round(row_num/num_rows*100, 1)) 
           break
       
    # Other
    rankingData.sort_values(by=["other"], inplace=True)
    for row_num in range(num_rows):
        if rankingData.iloc[row_num].other >= number_of_crimes_dict['other']: 
           other = str(round(row_num/num_rows*100, 1)) 
           break
           
    if printValues == True:
       print("\nCrime Rankings (0% = lowest, 100% = highest):")
       print("   Total:      " + total_number_of_crimes + "%")
       print("     Theft:    " + theft + "%")
       print("     Assault:  " + assault + "%")
       print("     Robbery:  " + robbery + "%")
       print("     Burglary: " + burglary + "%")
       print("     Homocide: " + homocide + "%")
       #print("     Other:    " + other + "%")       
    
    # Store all info in a dictionary object, which will be returned
    crime_rankings_dict = {
      "latitude": latitude,
      "longitude": longitude,
      "radius in meters": metersInterval,
      
      "total number of crimes ranking": number_of_crimes_dict['total_number_of_crimes'],
      "number of theft crimes": number_of_crimes_dict['theft'],
      "number of assault crimes": number_of_crimes_dict['assault'],
      "number of robbery crimes": number_of_crimes_dict['robbery'],
      "number of burglary crimes": number_of_crimes_dict['burglary'],
      "number of homicide crimes": number_of_crimes_dict['homocide'],
      "number of other crimes": number_of_crimes_dict['other'],      
      
      "total crimes percentile ranking": total_number_of_crimes,
      "theft crimes percentile ranking": theft,
      "assault crimes percentile ranking": assault,
      "robbery crimes percentile ranking": robbery,
      "burglary crimes percentile ranking ": burglary,
      "homicide crimes percentile ranking": homocide,
      "other crimes percentile ranking": other     
    }
    
    return crime_rankings_dict
        
     
##############################################################################

######################################
### MAKE THE CRIME RANKING DATASET ###
######################################
  
if False:
    
   # Make the data set used to generate 
   # crime queries (i.e. the crime rankings)
   rankingData = makeRankingData(
     data_path      = data_path, 
     out_path       = data_path,
     metersInterval = RADIUS,
     debug          = True
   )
 
########################################
### GET CRIME RANKINGS FOR LOCATIONS ###
########################################  

if False:
  
   # For a given lat/long, get the crime rankings
   query1 = getQuery(
     latitude       = 38.859959,
     longitude      = -76.969035,
     data_path      = data_path,
     metersInterval = RADIUS
   )

   query2 = getQuery(
     latitude       = 38.9014829636,
     longitude      = -76.9332371122,
     data_path      = data_path,
     metersInterval = RADIUS
   )
   
   # Lincoln memorial
   query3 = getQuery(
     latitude       = 38.889248,
     longitude      = -77.050636,
     data_path      = data_path,
     metersInterval = RADIUS
   )
    
################################
### TESTING & DEBUGGING ONLY ###
################################
  
if False:
    
   DC_shape_file = getShapeFileForDC(data_path)

   crimeData = getCrimeData(data_path)
   
   # lincoln memorial
   isPointInDC(
     lat    = 38.889248,
     long   = -77.050636,
     shape  = DC_shape_file,
     output = True
   ) 
    
   numCrimes = countCrimesInArea(
      latitude       = 38.9014829636, 
      longitude      = -76.9332371122,
      data           = crimeData,
      radiusInMeters = RADIUS
   )
   
   offense_value_counts = crimeData["OFFENSE"].value_counts()





















    
    
    
    
    
    
    
