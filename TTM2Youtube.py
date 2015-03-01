#!/usr/bin/env python

# This program downloads Tehran Traffic Map images from traffic control website ...
# ... then it creates a video based on the images and upload them to Youtube.
#
#              --- Copyright Ali Mirjamali (2015) ---
#

import httplib, urllib, urllib2
import time

# Currently Tehran Traffic Map is not available via a Domain. Here is the IP:
myHost = "31.24.237.150"
# The URL for the map image (PNG) is here:
myMapURL = "/TTCCTrafficWebSite/UploadedFiles/WebTrafficImages/Web0.png"

# ETags to check if the map is updated
etag_old=""
etag_new=""

# File index
myFileNum = 1

while True:
	# Connect to the server and retrieve headers
	myHTTPConnection = httplib.HTTPConnection(myHost)
	myHTTPConnection.request("HEAD", myMapURL)
	myResponse = myHTTPConnection.getresponse()
	myHeaders = myResponse.getheaders()
	# Store the new ETag header in etag_new
	etag_new = myResponse.getheader("etag")
	# Do we have a new refreshed map?
	if etag_new != etag_old:
		
		# Code for sanity check. To be removed later
		etag_old=etag_new
		for header in myHeaders:
			print header
		
		# Read the PNG file and store in myMap val, write to ./tmp/########.png
		myMap = urllib2.urlopen("http://" + myHost + myMapURL).read()
		myFile = open("./tmp/" + str(myFileNum).zfill(8) + ".png", 'wb')
		myFile.write(myMap)
		myFile.close()
		# Increase file index for next map image	
		myFileNum+=1
	else:
		# If not, wait 15 seconds and check again
		time.sleep(15)
		continue
