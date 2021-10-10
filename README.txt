
###############################
### NOTES ON THE CRIME DATA ###
###############################

 - Crime data come from here: https://opendata.dc.gov/datasets/DCGIS::crime-incidents-in-2020/about

    - OFFENSE variable includes: 
         'MOTOR VEHICLE THEFT', 'THEFT/OTHER', 'BURGLARY', 'THEFT F/AUTO',
         'ROBBERY', 'ASSAULT W/DANGEROUS WEAPON', 'HOMICIDE', 'SEX ABUSE',
         'ARSON'

    - METHOD variable includes: "GUN", "KNIFE", "OTHERS"

    - SHIFT variable includes 'DAY', 'EVENING', 'MIDNIGHT'

#######################
### REMAINING TASKS ###
#######################

    1) A way to generate the user's current location (latitude and longitude)
    2) A way to generate x evenly spaced data points in DC. These can be looped
       through to generate the number of crimes in the surrounding area. After
       the data are saved, we can use the data set to generate a percentile 
       ranking.
    3) A GUI

####################
### RANDOM NOTES ###
####################  
   
   - Multiply the degrees of separation of longitude and latitude by 111,139 to
  get the corresponding linear distances in meters.  