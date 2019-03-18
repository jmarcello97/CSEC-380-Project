from flask import Flask, flash, render_template, request, url_for, redirect, session, g
#from flask_mysqldb import MySQL
import MySQLdb
from MySQLdb import escape_string as thwart
from passlib.hash import sha256_crypt
import os
import time


app = Flask(__name__, template_folder="template")
#used for seassion config
secKey = os.urandom(24)
app.secret_key = secKey
time.sleep(30)
conn = MySQLdb.connect(host="db", user="root", passwd="root", db="users", port = 3306)
c = conn.cursor()

@app.route('/', methods=["GET","POST"])
def index():
	error = ''
	try:
		if request.method == 'POST':
			# Fetch form data
			username = request.form['username']
			password = request.form['password']
			#flash(username)
			#flash(password)
			data = c.execute("SELECT * FROM User WHERE username = %s", [username])
			data = c.fetchone()[2]
			if sha256_crypt.verify(password, str(data)):
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
