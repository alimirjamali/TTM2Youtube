TTM2Youtube
===========
### Tehran Traffic Map to Youtube Video

This program generates videos of [Tehran Traffic Map](http://31.24.237.150/TTCCTrafficWebSite/PublicUsers/GraphicalTrafficMap/Default.aspx) and uploads it to Youtube. Videos are created on daily basis.

### Tehran Traffic Map images

Traffic Map images are available as JPEG files on Tehran Traffic Control Web Server (file extention in URL is incorrectly specified as PNG). This is an example of a traffic map downloaded in rush hour:

![](SampleMap.png)

The JPEG file is updated by server's ASPX code approximately every 5 minutes. Live example here:

![](http://31.24.237.150/TTCCTrafficWebSite/UploadedFiles/WebTrafficImages/Web0.png)

### Further development

This project should be updated to support higher quality maps from [tehrantrafficmap.ir](http://tehrantrafficmap.ir/) site.

### Development notes

It might be possible to generate video directly from Python without calling avconv externally. Some good resources to look into:

http://zulko.github.io/blog/2013/09/27/read-and-write-video-frames-in-python-using-ffmpeg/

