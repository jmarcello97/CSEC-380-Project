from flask import Flask, flash, render_template, request, url_for, redirect, session, g
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import MySQLdb
from flask_sqlalchemy import SQLAlchemy
from MySQLdb import escape_string as thwart
from passlib.hash import sha256_crypt
import os
import time
from werkzeug import secure_filename
import urllib.request
import shutil
import requests
from datetime import datetime
import sys

time.sleep(30)
app = Flask(__name__, template_folder="template")
conn = MySQLdb.connect(host="db", user="root", passwd="root", db="users", port=3306)
c = conn.cursor()


# create the folders when setting up your app
os.makedirs('static/videos', exist_ok=True)


#used for seassion config
secKey = os.urandom(24)
app.secret_key = secKey

#for limiting the brute force attack
limiter = Limiter (
    app,
    key_func=get_remote_address,
   # default_limits=["28000 per day", "1000 per hour", "20 per minute"]
)
#limiting the  brute force attack
@app.route('/', methods=["GET","POST"])
@limiter.limit("8000/day;400/hour;25/minute")
def index():
	error = ''
	#try:
	if request.method == 'POST':
		# Fetch form data
		not_in_db=False
		username = request.form['username']
		password = request.form['password']
		data = c.execute("SELECT * FROM User WHERE Username = '{}'".format(username))
		if data == 0:
			not_in_db=True

		if not_in_db:
			error = "Invalid username, try again."

		else:
			data = c.fetchone()[2]
			if sha256_crypt.verify(password, str(data)):
				session['username'] = username

				return redirect(url_for("upload"))
			else:
				error = "Invalid password, try again."


	return render_template('index.html', error = error)

@app.route('/logout')
def logout():
    # remove the username from the session if it's there
	session.pop("username", None)
	return redirect(url_for('index'))

@app.route("/video/<filename>")
def video(filename):
	if 'username' in session:
		return render_template("video_viewing_screen.html",video_name=filename)
	else:
		return redirect(url_for("index"))

@app.route("/getSession")
def getSession():
	if "username" in session:
		return  session["user"]
	return "No Session avalibale!"

@app.route("/dropSession")
def dropSession():
	session.pop("username", None)

@app.before_request
def before_request():
	g.user = None
	if "username" in session:
		g.user = session["username"]



@app.route('/upload' , methods = ['GET', 'POST'] )
def upload():
	#error=''
	#try:
	if 'username' in session:
		if request.method == 'POST':
			#f = request.files['file']
			if 'file' in request.files.keys():
			# when saving the file
				f = request.files['file']
				#flash(f.filename)
				if '' != f.filename:
					f.save("static/videos/{}".format(f.filename))

					data = c.execute("SELECT * FROM User WHERE Username = '{}'".format(session['username']))
					insert = c.execute("INSERT INTO Video VALUES(%s, %s, %s, %s, %s)",(c.fetchone()[0], None, "local", f.filename, datetime.today().strftime('%Y-%m-%d')))
					conn.commit()

			if 'link11' in request.form.keys():
				url = request.form['link11']
				if url != '':
					filename123 = url.split("/")[-1]
					urllib.request.urlretrieve(url, "static/videos/"+filename123)

					data = c.execute("SELECT * FROM User WHERE Username = '{}'".format(session['username']))
					insert = c.execute("INSERT INTO Video VALUES(%s, %s, %s, %s, %s)",(c.fetchone()[0], None, "local", filename123, datetime.today().strftime('%Y-%m-%d')))

					conn.commit()

		videos = []
		for video in os.listdir("static/videos"):
			data = c.execute("SELECT * FROM Video WHERE Name = '{}'".format(video))
			video_uploader = c.fetchone()[0]
			video_uploader = c.execute("SELECT * FROM User WHERE UserID = '{}'".format(video_uploader))
			username = c.fetchone()[1]
			videos.append((video, username)) 
		return render_template('upload.html', videos=videos)
	return render_template('index.html')

@app.route('/delete_video/<filename>')
def delete_video(filename):
	if 'username' in session:
		#os.remove("static/videos/{}".format(filename))
		print(session['username'], file=sys.stdout)
		userid = c.execute("SELECT * FROM User WHERE Username = '{}'".format(session['username']))
		userid = c.fetchone()[0]
		video = c.execute("SELECT * FROM Video WHERE UserID = {} AND Name = '{}'".format(userid, filename))
		video = c.fetchone()
		if video != None:
			#os.remove("static/videos/{}".format(filename))
			os.system("rm static/videos/{}".format(filename))
			c.execute("DELETE FROM Video WHERE UserID = {} AND Name = '{}'".format(userid, filename))
			conn.commit()
		else:
			return "Don't delete other people's videos!"
		return redirect(url_for('upload'))
	return "test"

if __name__ == '__main__':
	app.run(host='0.0.0.0', debug=True)

