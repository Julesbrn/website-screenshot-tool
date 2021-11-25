from UrlScreenShot import ScreenshotMulti, ScreenShotSingle, str2
from flask import Flask
from markupsafe import escape
from flask import url_for
from flask import request
from flask import render_template
from flask import jsonify, send_file
import base64
from io import BytesIO
from urllib.parse import unquote

#./angular/siteScreenShot/dist/siteScreenShot

app = Flask(__name__)
print("This should run on startup")

@app.route('/', methods=['GET'])
def root():
	return render_template('index.html') # Return index.html 

@app.route('/getImg/<string:url>')
def show_post(url):
	#we need to double encode so that flask url parser wont break.
	#https://stackoverflow.com/questions/24519076/python-flask-url-encoded-leading-slashes-causing-404-or-405
	url = unquote(url)
	tmp = ScreenShotSingle(url)

	print("Got the url: " + url)
	rawbytes = base64.b64decode(tmp[0])
	buffer = BytesIO()
	buffer.write(rawbytes)
	buffer.seek(0)
	return send_file(buffer, as_attachment=False,
					 attachment_filename='file.jpg',
					 mimetype='image/jpeg')

@app.route("/ping")
def ping():
	return "PONG"

#def debugLog(msg, logFile = "/opt/log/py.log"):
#	f = open(logFile, "a")
#	f.write(msg)
#	f.close()

#debugLog("Python started")