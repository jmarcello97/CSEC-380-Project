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
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://root:root@db:3306/users"
db = SQLAlchemy(app)


# create the folders when setting up your app
#os.makedirs(os.path.join(app.instance_path, 'video'), exist_ok=True)
os.makedirs('static/videos', exist_ok=True)

class users(db.Model):
    __tablename__ = "User"
    UserID = db.Column('UserID', db.Integer, primary_key=True, nullable=False, autoincrement=True)
    Username = db.Column('Username', db.String(15))
    PasswordHash = db.Column('PasswordHash', db.String(200))
    DisplayName = db.Column('DisplayName', db.String(15))
    #data = db.Column()
    def __init__(self,UserID, Username, PasswordHash, DisplayName ):
        self.UserID = UserID
        self.Username = Username
        self.PasswordHash = PasswordHash
        self.DisplayName = DisplayName



class Video(db.Model):
    __tablename__ = "Video"
    VideoID = db.Column("VideoID", db.Integer, primary_key= True, autoincrement=True)
    UserID = db.Column('UserID', db.Integer, ForeignKey_key=("User.UserID"), nullable=False)
    URL = db.Column('URL', db.String(60))
    Name = db.Column('Name', db.String(100))
    UploadDate = db.Column('UploadDate', db.DateTime)


    def __init__(self,VideoID, UserID, URL, Name, UploadDate  ):
        self.VideoID = VideoID
        self.UserID = UserID
        self.URL = URL
        self.Name = Name
        self.UploadDate = UploadDate

#used for seassion config
secKey = os.urandom(24)
app.secret_key = secKey
#time.sleep(30)
#conn = MySQLdb.connect(host="db", user="root", passwd="root", db="users", port = 3306)
#c = conn.cursor()

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
	try:
		if request.method == 'POST':
			# Fetch form data
			username = request.form['username']
			password = request.form['password']
			#try:
			data=users.query.filter_by(Username=username).first()
			#except Exception as e:
			#	flash(e)
			#data = c.execute("SELECT * FROM User WHERE username = %s", [username])
			#data = c.fetchone()[2]
			if sha256_crypt.verify(password, str(data.PasswordHash)):
				session['username'] = username
				flash("you are now logged in")

				return redirect(url_for("upload"))

			else:
				error = "Invalid credentials, try again."

	except Exception as e:
		#error = "Invalid credentials, try again."
		return render_template("index.html", error = error)

	return render_template('index.html', error = error)

@app.route('/logout')
def logout():
    # remove the username from the session if it's there
	#dropSession()
	#username=session['username']
	session.pop("username", None)
	return redirect(url_for('index'))

@app.route("/video/<filename>")
def video(filename):
	if 'username' in session:
		#return app.send_static_file(filename)
		#filename = os.path.join('static', filename)
		return render_template("video_viewing_screen.html",video_name=filename)
		#return redirect(filename)
		#return render_template(filename)
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
	error=''
	try:
		if 'username' in session:
			if request.method == 'POST':
				#f = request.files['file']
				if 'file' in request.files.keys():
			# when saving the file
					f = request.files['file']
					f.save("static/videos/{}".format(f.filename))

					data=users.query.filter_by(Username=session['username']).first()
					new_video = Video(VideoID = None, UserID = data.UserID, URL = "local", Name = f.filename, UploadDate = datetime.today().strftime('%Y-%m-%d'))
					db.session.add(new_video)
					db.session.commit()
                    #i = Video.insert()
                    #i.execute(UserID=data.UserID, URL = "Local", Name = f.filename, UploadDate = datetime.today().strftime('%Y-%m-%d'))

				#f2 = request.form['link11']
				if 'link11' in request.form.keys():
					url = request.form['link11']
					#reqGet = requests.get(url)
					filename123 = url.split("/")[-1]
					#with open(filename123,'wb') as vid:
					#	shutil.copyfileobj(reqGet.raw, "static/videos/"+vid)
					urllib.request.urlretrieve(url, "static/videos/"+filename123)
					data = users.query.filter_by(Username=session['username']).first()
					new_video = Video(VideoID = None, UserID = data.UserID, URL = "local", Name = filename123, UploadDate = datetime.today().strftime('%Y-%m-%d'))
					db.session.add(new_video)
					db.session.commit()


			videos = []
			for video in os.listdir("static/videos"):
				video_uploader = Video.query.filter_by(Name=video).first()
				video_uploader = users.query.filter_by(UserID=video_uploader.UserID).first()
				videos.append((video, video_uploader.Username))
			return render_template('upload.html', videos=videos)

	except Exception as e:
		return render_template("upload", error = e)


		#        f.save(secure_filename(f.filename))

	#videos = os.listdir("static/videos")
	#return render_template('test_upload.html')
	#return render_template('upload.html', videos=videos)
	#if 'username' in session:
	#	if request.method == 'POST':
	#		#f = request.files['file']
	#		f2 = request.form['link11']

	#		if f2:
	#			url = request.form['link11']
	#			reqGet = requests.get(url)
	#			filename123 = url.split("/")[-1]
	#			os.path.join(app.instance_path, "video", filename123)
	#		with open(filename123,'wb') as vid:
				#shutil.copyfileobj(reqGet.raw, vid)

                #urllib.request.urlretrieve(url_link, 'video_name.mp4')
                #v = pafy.new(str(url))
                #s = v.allstreams[len(v.allstreams)-1]
                #filename = s.download(os.path.join(app.instance_path, 'video', secure_filename(v.title)))
	#return render_template('index.html')

@app.route('/delete_video/<filename>')
def delete_video(filename):
	if 'username' in session:
		#os.remove("static/videos/{}".format(filename))
		print(session['username'], file=sys.stdout)
		data=users.query.filter_by(Username=session['username']).first()
		video=Video.query.filter_by(UserID=data.UserID,Name=filename).first()
		if video != None:
			os.remove("static/videos/{}".format(filename))
			db.session.delete(video)
			db.session.commit()
		else:
			return "Don't delete other people's videos!"
		return redirect(url_for('upload'))
	return "test"

if __name__ == '__main__':
	#app.run()
	app.run(host='0.0.0.0', debug=True)
    #port = int(os.environ.get('PORT', 5000))
    #app.run(app, host='0.0.0.0', port=port)

