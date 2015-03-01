#!/usr/bin/env python

# This program downloads Tehran Traffic Map images from traffic control website ...
# ... then it creates a video based on the images and upload them to Youtube.
#
#              --- Copyright Ali Mirjamali (2015) ---
#

import httplib, urllib
import time

# Currently Tehran Traffic Map is not available via a Domain. Here is the IP:
myHost = "31.24.237.150"
# The URL for the map image (PNG) is here:
myMapURL = "/TTCCTrafficWebSite/UploadedFiles/WebTrafficImages/Web0.png"

# ETags to check if the map is updated
etag_old=""
etag_new=""


while True:
	# Connect to the server and retrieve headers
	myHTTPConnection = httplib.HTTPConnection(myHost)
	myHTTPConnection.request("HEAD", myMapURL)
	myResponse = myHTTPConnection.getresponse()
	myHeaders = myResponse.getheaders()
	# Store the new ETag header in etag_new
	for header in myHeaders:
		if header[0] == 'etag':
			etag_new=header[1]
			break
	# Do we have a new refreshed map?
	if etag_new != etag_old:
		etag_old=etag_new
		for header in myHeaders:
			print header
	else:
		# If not, wait 15 seconds and check again
		time.sleep(15)
		continue
