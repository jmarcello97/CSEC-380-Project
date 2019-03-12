from flask import Flask, flash, render_template, request, url_for, redirect
#from flask_mysqldb import MySQL
import MySQLdb
from MySQLdb import escape_string as thwart
from passlib.hash import sha256_crypt
import os
import time
app = Flask(__name__, template_folder="template")
app.secret_key = os.urandom(24)

time.sleep(30)
conn = MySQLdb.connect(host="db", user="root", passwd="root", db="users", port = 3306)
c = conn.cursor()
# Configure db
#mysql = MySQL(app)


#@app.route('/')
#def homepage():
	#return render_template("login.html")

@app.route("/video")
def video():
	return render_template("video_viewing_screen.html")

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
				#session['logged_in'] = True
				#session['username'] = request.form['username']
				flash("you are now logged in")

				return redirect(url_for("video"))

			else:
				error = "Invalid credentials, try again."

	except Exception as e:
		#error = "Invalid credentials, try again."
		return render_template("index.html", error = error)

	return render_template('index.html', error = error)

"""
@app.route('/users')
def users():
    cur = mysql.connection.cursor()
    resultValue = cur.execute("SELECT * FROM users")
    if resultValue > 0:
        userDetails = cur.fetchall()
        return render_template('users.html',userDetails=userDetails)
"""
if __name__ == '__main__':
	#app.run()
	app.run(host='0.0.0.0', debug=True)
    #port = int(os.environ.get('PORT', 5000))
    #app.run(app, host='0.0.0.0', port=port)
