# -*- coding: utf-8 -*-
import os, datetime
import re
from unidecode import unidecode

from flask import Flask, request, render_template, redirect, abort, jsonify
import requests

# from twilio.rest import TwilioRestClient

app = Flask(__name__)


# @app.route('/')
# def main():
# 	return render_template('index.html')

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
			'v': '20121113' # this saves the date data, whichi is nice thing about foursquare
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
			return "something went wrong on line 50 %s " % results.json


@app.errorhandler(404)
def page_not_found(error):
	return render_template('404.html'),404



if __name__ == "__main__":
	app.debug = True

	port = int(os.environ.get('PORT', 5000))
	app.run(host ='0.0.0.0', port= port)