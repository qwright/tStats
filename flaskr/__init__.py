from flask import Flask, render_template, jsonify
import os
from bs4 import BeautifulSoup
from flaskr import irc

def create_app(test_config=None):	
	app = Flask(__name__)

	irc.joinchan('hasanabi')
	
	@app.route("/")
	def main():
		return render_template("index.html")
	
	@app.route("/process")
	def process():
		return jsonify(chat=irc.getmsg())
		
	return app

#def getTopChanels():
#	with open("https://www.twitch.tv/directory/all") as fin:
#		soup = BeautifulSoup(fin)
	
