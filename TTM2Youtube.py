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
import os

# Currently Tehran Traffic Map is not available via a Domain address. Here is the server's IP:
myHost = "31.24.237.150"
# The URL for the map image (JPEG)
# Note that the .png in URL is not correct and the actual data format is JPEG
myMapURL = "/TTCCTrafficWebSite/UploadedFiles/WebTrafficImages/Web0.png"

# We will upload one video per day
today = datetime.date.today()

# Create tmp directory
myTempDir = tempfile.mkdtemp(prefix="TTM2Youtube")

# Generate video for upload by calling avconv via a subprocess
def myFuncGenerateVid():
	myCommandLine = [
		'avconv',
		'-y',
		'-i',
		myTempDir + "/%08d.jpg",
		'-r', '24',
		'-b', '8M',
		'-filter:v', '"setpts=4.0*PTS"',
		myTempDir + "/output.mp4"]
	pipe = subprocess.Popen(myCommandLine, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
	return

# Upload the video to Youtube
def myFuncUpload2Youtube():
	return

# Erase temp files
def myFuncClearTemp(TempDir):
	if os.path.exists(TempDir): 
		print "Ereasing temp directory"
		# shutil.rmtree(myTempDir)
		TempDir = tempfile.mkdtemp(prefix="TTM2Youtube")
	return

# Read the PNG file from site and write to ########.png in temp directory
def myFuncGetMap():
	try:
		myMap = urllib2.urlopen("http://" + myHost + myMapURL).read()
		myFile = open(myTempDir + "/" + str(myFuncGetMap.index).zfill(8) + ".jpg", 'wb')
		# Some messages for debuging
		print datetime.datetime.now(), "Writing:", myFile.name
		myFile.write(myMap)
		myFile.close()
		myFuncGetMap.index = myFuncGetMap.index+1
	except:
		print "Error getting map image from site"
	return
myFuncGetMap.index=1

# If there is a new map PNG image on the server, return true.
def myFuncIsUpdated():
	myHTTPConnection = httplib.HTTPConnection(myHost)
	myHTTPConnection.request("HEAD", myMapURL,headers={"Cache-Control":"no-cache"})
	try:
		myResponse = myHTTPConnection.getresponse()
		myHTTPConnection.close()
		myFuncIsUpdated.etag_new = myResponse.getheader("etag")
		if myFuncIsUpdated.etag_new != myFuncIsUpdated.etag_old:
			myFuncIsUpdated.etag_old = myFuncIsUpdated.etag_new
			return True
		else:
			return False
	except httplib.BadStatusLine:
		print "Error getting response from server"
		return False
myFuncIsUpdated.etag_new = ""
myFuncIsUpdated.etag_old = ""

while True:

	# Do we have a new refreshed map?
	if myFuncIsUpdated():
		# Retrieve new file from server
		myFuncGetMap()

	# Upload the video on date change and clear temp, otherwise wait for 30 seconds to check for a new map
	if today != datetime.date.today():
		myFuncGenerateVid()
		myFuncUpload2Youtube()
		myFuncClearTemp(myTempDir)
		today = datetime.date.today()
		myFuncGetMap.index = 1
	else:
		time.sleep(30)
