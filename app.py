# -*- coding: utf-8 -*-
import os, datetime
import re
from unidecode import unidecode

from flask import Flask, request, render_template, redirect, abort, jsonify
import requests

app = Flask(__name__)


# access tokens allow apps to make rewquests to foursquare on the behalf of a user. 
# each access token is unique to the user and consumer key

# some of the endpoints do not require the specific user information, such as venue search. 

@app.route("/", methods = ['GET', 'POST'])

def fsqdemo():
	if request.method == "GET":
		return render_template('fsq.html')

	elif request.method == "POST":
		user_latlng = request.form.get('user_latlng')

		#below is Foursquare API endpoint for search
		fsq_url = "https://api.foursquare.com/v2/venues/search"

		# prepare the query parameters
		fsq_query = {
			'client_id': os.environ.get('FOURSQUARE_CLIENT_ID'),
			'client_secret': os.environ.get('FOURSQUARE_CLIENT_SECRET'),
			'v': '20121118',
			'query': 'macaron',
			'll': user_latlng # this saves the date data, whichi is nice thing about foursquare
			# v means version. 
			# v = YYYYMMDD
		}

		results = requests.get(fsq_url, params = fsq_query)

		app.logger.info("Requested url: %s " % results.url )

		if results.status_code == 200: # that means it's okay!
			fsq_response = results.json
			nearby_venues = fsq_response['response']['venues']

			app.logger.info('nearby venues are: ')
			app.logger.info(nearby_venues)

			return jsonify(results.json['response'])

		else:
			return "Oops, something went wrong %s " % results.json



@app.route("/map.html")
def mapRender():
	return render_template('map.html')

@app.errorhandler(404)
def page_not_found(error):
	return render_template('404.html'),404


if __name__ == "__main__":
	app.debug = True

	port = int(os.environ.get('PORT', 5000))
	app.run(host ='0.0.0.0', port= port)