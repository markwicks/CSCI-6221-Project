import streamlit as st
import numpy as np
import pandas as pd
import requests
#import CSCI-6212-Project.main as md

data_path = "D:/CSCI 6212/CSCI-6221-Project/data/"


###############################################################################

def getCrimeData():
    data = pd.read_csv(data_path + "crime_2020.csv")
    data = data[["LATITUDE", "LONGITUDE", "SHIFT", "START_DATE", "METHOD", "OFFENSE"]]
    return(data)

def main():
	menu = ["Home"]
	choice = st.sidebar.selectbox("Menu",menu)

	st.title("DC Crime Map")

	if choice == "Home":
		st.subheader("Home")

		#Nav Search Form
		with st.form(key='searchform'):
			nav1,nav2 = st.columns([2,1])

			with nav1:
				location= st.text_input("Location")
			with nav2:
				st.text("Search the Crime")
				submit_search = st.form_submit_button(label='Search')
		st.success("You searched for crimes in {}".format(location))

		BASE_URL= 'https://nominatim.openstreetmap.org/search?format=json'
		postcode ='22'

		#results
		if submit_search:
			crimeData = getCrimeData()

			num_of_results = len(crimeData)
			st.subheader("Showing {} crimes".format(num_of_results))

			st.write(crimeData)
			crimeData[["latitude", "longitude", "SHIFT", "START_DATE", "METHOD", "OFFENSE"]] = crimeData[["LATITUDE", "LONGITUDE", "SHIFT", "START_DATE", "METHOD", "OFFENSE"]]
			st.map(crimeData)


if __name__ == '__main__':
	main()