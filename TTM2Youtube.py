#!/usr/bin/env python

# This program downloads Tehran Traffic Map images from Tehran Traffic Control website ...
# ... then it creates a video from the downloaded images and upload it to Youtube.!!!
#
#                   --- Copyright Ali Mirjamali (2015) ---
#
#  --- This code should be GPL 2.0 compliant. Please report any issues ---

import httplib, urllib, urllib2
import time, datetime
import tempfile
import subprocess

# Currently Tehran Traffic Map is not available via a Domain address. Here is the server's IP:
myHost = "31.24.237.150"
# The URL for the map image (JPEG)
# Note that the .png in URL is not correct and the actual data format is JPEG
myMapURL = "/TTCCTrafficWebSite/UploadedFiles/WebTrafficImages/Web0.png"

# ETags to check if the map image file is updated on server
etag_old = ""
etag_new = ""

# We will upload one video per day
today = datetime.date.today()

# Create tmp directory
myTempDir = tempfile.mkdtemp(prefix="TTM2Youtube")

# File index on temp directory
myFileNum = 1

# Generate video for upload by calling avconv via a subprocess
def myFuncGenerateVid():
	myCommandLine = [
		'avconv',
		'-y',
		'-i',
		myTempDir + "/%08d.jpg",
		'-r', '24',
		myTempDir + "/output.mp4"]
	pipe = subprocess.Popen(myCommandLine, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
	return

# Upload the video to Youtube
def myFuncUpload2Youtube():
	return

# Erase temp files
def myFuncClearTemp():
	return

# Read the PNG file from site and write to ########.png in temp directory
def myFuncGetMap(index):
	myMap = urllib2.urlopen("http://" + myHost + myMapURL).read()
	myFile = open(myTempDir + "/" + str(index).zfill(8) + ".jpg", 'wb')
	# Some messages for debuging
	print datetime.datetime.now(), "Writing:", myFile.name
	myFile.write(myMap)
	myFile.close()
	return

# Retrieve ETag of the map PNG image to see if it is updated
def myFuncGetETag():
	myHTTPConnection = httplib.HTTPConnection(myHost)
	myHTTPConnection.request("HEAD", myMapURL,headers={"Cache-Control":"no-cache"})
	myResponse = myHTTPConnection.getresponse()
	myHTTPConnection.close()
	return myResponse.getheader("etag")

while True:

	# Store the new ETag header in etag_new
	etag_new = myFuncGetETag()
	# Do we have a new refreshed map?
	if etag_new != etag_old:
		
		# Retrieve new file from server
		myFuncGetMap(index=myFileNum)

		# Increase file index for next map image, update ETag for last file
		myFileNum+=1
		etag_old=etag_new

	# Upload the video on date change and clear temp, otherwise wait for 15 seconds to check for a new map
	if today != datetime.date.today():
		myFuncGenerateVid()
		myFuncUpload2Youtube()
		myFuncClearTemp()
		today = datetime.date.today()
		myFileNum = 1
	else:
		time.sleep(15)
