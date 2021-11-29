import streamlit as st
import numpy as np
import pandas as pd
import requests
from geopy.geocoders import Nominatim
import folium
from streamlit_folium import folium_static
import main


#type "streamlit run webstreamlit.py" in your cmd window , it will pop out the website#

data_path = "/Users/josepher/PycharmProjects/test/CSCI-6221-Project/data/"


###############################################################################
def website():
	menu = ["Home"]
	choice = st.sidebar.selectbox("Menu", menu)

	st.title("DC Crime Map")

	if choice == "Home":
		st.subheader("Home")

		# Nav Search Form
		with st.form(key='searchform'):
			nav1, nav2 = st.columns([2, 1])

			with nav1:
				location = st.text_input("Location")
			with nav2:
				st.text("Check statistics")
				submit_search = st.form_submit_button(label='Search')
		st.success("You searched for crimes in {}".format(location))

		BASE_URL = 'https://nominatim.openstreetmap.org/search?format=json'
		postcode = '22'

		# results
		if submit_search:
			# use Geopy to fetch the latitude and longitude
			geolocator = Nominatim(user_agent="DC_Crime")
			test_loc = geolocator.geocode({location})
			# show the latitude and longtitude
			st.write(test_loc.latitude, test_loc.longitude)

			# show the corresponding result table
			crimeData = main.getQuery(test_loc.latitude, test_loc.longitude, data_path, 250)
			crimeresult = pd.DataFrame(crimeData, index=[0])
			st.table(crimeresult)

			lat_long = float(test_loc.latitude), float(test_loc.longitude)
			# show the map with the input address
			m = folium.Map(location=lat_long, width=800, height=400, zoom_start=16)
			folium.Marker(lat_long, popup=test_loc,
						  icon=folium.Icon(color='red', icon='fa-exclamation', prefix='fa')).add_to(m)
			folium_static(m)


if __name__ == '__main__':
	website()
