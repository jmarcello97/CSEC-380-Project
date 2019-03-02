from flask import Flask, render_template, request, redirect
from flask_mysqldb import MySQL
from flask_socketio import SocketIO
import os
app = Flask(__name__, template_folder="template")

# Configure db
#mysql = MySQL(app)

@app.route('/')
def index():
    if request.method == 'POST':
        # Fetch form data
        userDetails = request.form
        username = userDetails['username']
        password = userDetails['password']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO users(username, password) VALUES(%s, %s)",(username, password))
        mysql.connection.commit()
        cur.close()
        return redirect('/index.html')
    return render_template('index.html')
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
