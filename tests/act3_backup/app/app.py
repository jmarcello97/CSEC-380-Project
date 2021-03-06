from flask import Flask, flash, render_template, request, url_for, redirect, session, g
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
#from flask_mysqldb import MySQL
import MySQLdb
from flask_sqlalchemy import SQLAlchemy
from MySQLdb import escape_string as thwart
from passlib.hash import sha256_crypt
import os
import time

time.sleep(30)
app = Flask(__name__, template_folder="template")
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://root:root@db:3306/users"
db = SQLAlchemy(app)

class users(db.Model):
    __tablename__ = "User"
    UserID = db.Column('UserID', db.Integer, primary_key=True)
    Username = db.Column('Username', db.String(15))
    PasswordHash = db.Column('PasswordHash', db.String(200))
    DisplayName = db.Column('DisplayName', db.String(15))
    #data = db.Column()


    def __init__(self,UserID, Username, PasswordHash, DisplayName ):
        self.UserID = UserID
        self.Username = Username
        self.PasswordHash = PasswordHash
        self.DisplayName = DisplayName

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
@limiter.limit("7000/day;300/hour;5/minute")
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

				return redirect(url_for("video"))

			else:
				error = "Invalid credentials, try again."

	except Exception as e:
		#error = "Invalid credentials, try again."
		return render_template("index.html", error = error)

	return render_template('index.html', error = error)

@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    dropSession()
    return redirect(url_for('/'))

@app.route("/video")
def video():
	if 'username' in session:
		return render_template("video_viewing_screen.html")
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


if __name__ == '__main__':
	#app.run()
	app.run(host='0.0.0.0', debug=True)
    #port = int(os.environ.get('PORT', 5000))
    #app.run(app, host='0.0.0.0', port=port)
