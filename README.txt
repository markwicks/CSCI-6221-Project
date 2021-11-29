
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

 - D.C. shape file (set of longitude and latitude points delineatings DC) came
    from here: 
    https://www.census.gov/geographies/mapping-files/time-series/geo/carto-boundary-file.html

Instructions to run: 

Open the main.py and webstreamlit.py and update the data path variables on line 13 in both programs to where the clone repository is. 

Navigate via the terminal or command line to the where the repository was cloned. There, ensure you are in the "CSCI-6221-Project" folder. From there, ensure you have the following Python libraries installed: 

streamlit
numpy
pandas
geopy
geocoders
nominatim
folium
streamlit_folium
folium_static

Upon confirmation of installed libraries, enter the following command in the command line/terminal: 
"streamlit run webstreamlit.py"

This will open a web browser with the LCG App. From there, you can input either an address like; 
"800 22nd St NW, Washington, DC 20052"
Or a generic term for a location in Washington DC like: 
"White House"
"George Washington University"

From there, the program will filter this to a lat/long reading and output a map and table containing the percentile readings. 
