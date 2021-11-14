
#######################
### REMAINING TASKS ###
#######################

    1) A way to generate the user's current location (latitude and longitude)
    2) A GUI, which can zero in on a point
    3) A way to type in an actual street address, and get the latitude and 
       longitude

###############################
### NOTES ON THE CRIME DATA ###
###############################

 - Crime data come from here: 
   https://opendata.dc.gov/datasets/DCGIS::crime-incidents-in-2020/about

    - OFFENSE variable includes: 
         'MOTOR VEHICLE THEFT', 'THEFT/OTHER', 'BURGLARY', 'THEFT F/AUTO',
         'ROBBERY', 'ASSAULT W/DANGEROUS WEAPON', 'HOMICIDE', 'SEX ABUSE',
         'ARSON'

    - METHOD variable includes: "GUN", "KNIFE", "OTHERS"

    - SHIFT variable includes 'DAY', 'EVENING', 'MIDNIGHT'

####################
### RANDOM NOTES ###
####################  
   
   - Multiply the degrees of separation of longitude and latitude by 111,139 to
  get the corresponding linear distances in meters.  
  
  - D.C. shape file (set of longitude and latitude points delineatings DC) came
    from here: 
    https://www.census.gov/geographies/mapping-files/time-series/geo/carto-boundary-file.html