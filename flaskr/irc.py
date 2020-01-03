import time
import socket
import click
import re
from flaskr import constants

user = constants.user
pswd = constants.pswd
server = 'irc.chat.twitch.tv'

ircsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ircsock.connect((server, 6667))
ircsock.send(bytes("PASS " + pswd + "\n", "UTF-8"))
ircsock.send(bytes("NICK " + user + "\n", "UTF-8"))

def joinchan(chan):
    ircsock.send(bytes("JOIN #" + chan + "\n", "UTF-8"))

def ping():
    ircsock.send(bytes("PONG :pingisn", "UTF-8"))

def getmsg():
    ircmsg = ircsock.recv(4096).decode("UTF-8")
    ircmsg = ircmsg.strip('nr')
    if ircmsg.find("PING: ") != -1:
        ping()
    else:
        bulk_chat = ircmsg.split("\n")
        cleaned_chat = []
        for msg in bulk_chat:
            if msg.find("PRIVMSG") != -1:
                channel = msg.split("#", 1)[1].split(":",1)[0].strip()
                name = msg.split("!", 1)[0][1:]
                message = msg.split("PRIVMSG", 1)[
                    1].split(":", 1)[1].strip("\r")
                    #clean problem glyphs
                message = message.replace('"', '""').replace('u"', '""')
                cleaned_chat.append(f"[{channel}] {name}: {message}")
                #print(f"[{channel}] {name}: {message}")
        return cleaned_chat

#def tsock(user, pswd, chan):
#    ircsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#    ircsock.connect(('irc.chat.twitch.tv', 6667))
#    ircsock.send(bytes("PASS " + pswd + "\n", "UTF-8"))
#    ircsock.send(bytes("NICK " + user + "\n", "UTF-8"))
 #   ircsock.send(bytes("JOIN #" + chan + "\n", "UTF-8"))
 #   return ircsock

#def getmsg(ircsock):
#    ircmsg = ircsock.recv(2048).decode("UTF-8")
#    ircmsg = ircmsg.strip('nr')
#    if ircmsg.find("PING: ") != -1:
#        print()
#        #ping()
#    else:
#        bulk_chat = ircmsg.split("\n")
#        cleaned_chat = []
#        for msg in bulk_chat:
#            if msg.find("PRIVMSG") != -1:
#                name = msg.split("!", 1)[0][1:]
#                message = msg.split("PRIVMSG", 1)[
#                    1].split(":", 1)[1].strip("\r")
#                message = message.replace('"', '""').replace('u"', '""')
#                cleaned_chat.append(name + ": " + message)
#                print(name + ": " + message)
#        return cleaned_chat