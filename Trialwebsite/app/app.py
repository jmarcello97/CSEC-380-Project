from flask import Flask, render_template, request, redirect
#from flask_mysqldb import MySQL
import MySQLdb
from flask_socketio import SocketIO
from passlib.hash import sha256_crypt
import os
import time
app = Flask(__name__, template_folder="template")

time.sleep(30)
conn = MySQLdb.connect(host="db", user="root", passwd="root", db="users", port = 3306)
c = conn.cursor()
# Configure db
#mysql = MySQL(app)

@app.route('/')
def index():

	error = ''
	if request.method == 'POST':
		# Fetch form data
		userDetails = request.form
		username = userDetails['username']
		password = userDetails['password']
		data = c.execute("SELECT * FROM users WHERE username = (%s)", thwart(username))
		data = c.fetchone()[2]

		if sha256_crypt.verify(password, data):
			session['logged_in'] = True
			session['username'] = request.form['username']

			flash("you are now logged in")

			return redirect(url_for("index.html"))

	else:
		error = "Invalid credentials, try again."

	#gc.collect()
        #cur = mysql.connection.cursor()
        #cur.execute("INSERT INTO users(username, password) VALUES(%s, %s)",(username, password))
        #mysql.connection.commit()
        #cur.close()
	#return redirect('/index.html')
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
    app.run(host='0.0.0.0', debug=True)
    #port = int(os.environ.get('PORT', 5000))
    #app.run(app, host='0.0.0.0', port=port)
