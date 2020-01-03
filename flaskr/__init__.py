from flask import Flask, render_template, jsonify
import os, requests
from bs4 import BeautifulSoup
from flaskr import irc, constants

def create_app(test_config=None):	
	app = Flask(__name__)

	top_channels = getTopChannels()
	
	@app.route("/")
	def main():
		for chan in top_channels:
			irc.joinchan('{}'.format(chan))	
		return render_template("index.html")
	
	@app.route("/process")
	def process():
		return jsonify(chat=irc.getmsg(), top_channels=top_channels)
		
	return app

def getTopChannels():
	twitch_directory = "https://api.twitch.tv/helix/streams?first=5"
	headers = {'Client-ID':'93yiz9p9t8j7r8btyvfiyxb1pzcsxv'}
	top = []
	response = requests.get(twitch_directory, headers=headers)
	jresponse = response.json()
	for channel in jresponse["data"]:
		top.append(channel["user_name"].lower())
	return top
	
