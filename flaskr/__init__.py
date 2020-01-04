from flask import Flask, render_template, jsonify
import os, requests
from bs4 import BeautifulSoup
from flaskr import irc, constants

def create_app(test_config=None):	
	app = Flask(__name__)

	top_channels = getTopChannels()
	empty_set = initViewerSet(top_channels)
	unique_chatters = {}

	@app.route("/")
	def main():
		for chan in top_channels:
			irc.joinchan('{}'.format(chan))	
		return render_template("index.html")
	
	@app.route("/process")
	def process():
		chat = irc.getmsg()
		viewer_set = uniqueChatters(chat, empty_set)
		unique_chat_vol = uniqueChatVol(top_channels, viewer_set, unique_chatters)
		return jsonify(chat=chat, top_channels=top_channels, unique_chat_vol=unique_chat_vol)
		
	return app

def getTopChannels()->'list':
	twitch_directory = "https://api.twitch.tv/helix/streams?first=5"
	headers = {'Client-ID':'93yiz9p9t8j7r8btyvfiyxb1pzcsxv'}
	top = []
	response = requests.get(twitch_directory, headers=headers)
	jresponse = response.json()
	for channel in jresponse["data"]:
		top.append(channel["user_name"].lower())
	return top

def uniqueChatVol(chans:'list', viewer_set:'dict of hashset', unique_chatters:'dict')->'dict':
	for c in chans:
		unique_chatters[c] = len(viewer_set[c])
	return unique_chatters

def uniqueChatters(chat:'list', viewer_set:'dict')->'dict of hashset':
	for msg in chat:
		chanmsg = msg.split("]",1)
		chan = chanmsg[0][1:].strip()
		#print(chan)
		user = chanmsg[1].split(":", 1)[0][1:].strip()
		#print(user)
		viewer_set[chan].add(user)
		#print(viewer_set[chan])
	return viewer_set

def initViewerSet(chans:'channels')->'dict of hashsets':
	empty_set = {}
	for c in chans:
		empty_set[c] = set()
	return empty_set