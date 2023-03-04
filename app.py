from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL, MySQLdb
import MySQLdb.cursors
import re    
# from datetime import datetime

app = Flask(__name__)

app.secret_key = 'xyz123abc'
app.config['MYSQL_HOST']='localhost'
app.config['MYSQL_USER']='root'
app.config['MYSQL_PASSWORD']='root123$'
app.config['MYSQL_DB']='login'

mysql = MySQL(app)



@app.route('/signup', methods=['GET', 'POST'])
def signup():
    message=''
    if request.method =='POST' and request.form['name'] and  request.form['password'] and request.form['email'] and  request.form['confirm_password']:
        username = request.form['name']
        password = request.form['password']
        email = request.form['email']
        confirm_password = request.form['confirm_password']
        if password == confirm_password:
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('SELECT * FROM user_login WHERE email = {};'.format('email') )
            account = cursor.fetchone()
            if account:
                message = 'Account already exists !'
            elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
                message = 'Invalid email address !'
            elif not username or not password or not email:
                message = 'Please fill out the form !'
            else:
                cursor.execute("INSERT INTO user_login (name,email,password) VALUES ('{}', '{}', '{}');".format(username, email, password))
                mysql.connection.commit()
                message = 'You have succesfully registered !'
        else:
            message = "Both passwords doesn't match"
    elif request.method == 'POST':
        message = "Please fill out the form !"
    return render_template('index.html',message = message)   

@app.route('/login', methods =['GET', 'POST'])
def login():
    message = ''
    print(request.method)
    if request.method == 'POST' and request.form['email'] and request.form['password']:
        email = request.form['email']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT * FROM user_login WHERE email = '{}' AND password = '{}';".format(email,password))
        user = cursor.fetchone()
        if user:
            session['loggedin'] = True
            session['id'] = user['id']
            session['name'] = user['name']
            session['email'] = user['email']
            message = 'Logged in successfully !'
            return render_template('user.html', message = message)
        else:
            message = 'Please enter correct email / password !'
    return render_template('index.html', message = message) 

@app.route('/admin_login', methods =['GET', 'POST'])
def admin_login():
    message = ''
    if request.method == 'POST' and request.form['email'] and request.form['password']:
        email = request.form['email']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT * FROM admin_login WHERE email = '{}' AND password = '{}';".format(email,password))
        user = cursor.fetchone()
        if user:
            session['loggedin'] = True
            session['id'] = user['id']
            session['name'] = user['name']
            session['email'] = user['email']
            message = 'Logged in successfully !'
            return render_template('admin.html', message = message)
        else:
            message = 'Please enter correct email / password !'
    return render_template('index.html', message = message)       

@app.route('/user_member')
def user_member():
    return render_template('user-member.html')

@app.route('/user')
def user():
    return render_template('user.html')

@app.route('/user_profile')
def user_profile():
    return render_template('user-profile.html')

@app.route('/user_attendance')
def user_attendance():
    return render_template('user-attendance.html')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/emp_attendance')
def emp_attendance():
    return render_template('admin-emp-attendance.html')

@app.route('/mem_attendance')
def mem_attendance():
    return render_template('admin-mem-attendance.html')

@app.route('/employee')
def employee():
    return render_template('admin-employee.html')

@app.route('/member')
def member():
    return render_template('admin-members.html')

@app.route('/admin')
def admin():
    return render_template('admin.html')

@app.route('/membership', methods=['GET','POST'])
def membership():
    # message=''
    print(request.form)
    
    # if request.method == 'POST' and request.form['fname'] and request.form['lname'] and request.form['address'] and request.form['gender'] and request.form['email'] and request.form['phone'] and request.form['workouts']:
    return "hello world"   

if __name__ == "__main__":
    app.run(debug=True, port=8000)
    