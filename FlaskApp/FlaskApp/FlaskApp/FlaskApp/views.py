"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import Flask, render_template, json, request, session, redirect
from FlaskApp import app
from flask.ext.mysql import MySQL
from werkzeug import generate_password_hash, check_password_hash

mysql = MySQL()
 
app.secret_key = 'why would I tell you my secret key?'

# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = '2698'
app.config['MYSQL_DATABASE_DB'] = 'BucketList'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)

# Default setting
pageLimit = 2

@app.route('/')
@app.route('/home')
def home():
    """Renders the home page."""
    return render_template(
        'index.html',
        title='Home-Page',
        year=datetime.now().year,
    )

@app.route('/contact')
def contact():
    """Renders the contact page."""
    return render_template(
        'contact.html',
        title='Contact Page',
        year=datetime.now().year,
        message='Your contact page.'
    )

@app.route('/about')
def about():
    """Renders the about page."""
    return render_template(
        'about.html',
        title='About Page',
        year=datetime.now().year,
        message='Your application description page.'
    )

@app.route('/showSignUp')
def showSignUp():
    return render_template('signup.html')

@app.route('/signUp', methods = ['POST'])
def signUp():
    
    # read the psoted values from the UI
    _name = request.form['inputName']
    _email = request.form['inputEmail']
    _password = request.form['inputPassword']
    _hashed_password = generate_password_hash(_password)

    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.callproc('sp_createUser',(_name,_email,_hashed_password))    

    # validate the received values
    data = cursor.fetchall()
 
    if len(data) is 0:
        conn.commit()
        return json.dumps({'message':'User created successfully !'})
    else:
        return json.dumps({'error':str(data[0])})


@app.route('/showSignin')
def showSignin():
    return render_template('signin.html')

@app.route('/validateLogin',methods=['POST'])
def validateLogin():
    try:
        _username = request.form['inputEmail']
        _password = request.form['inputPassword']

        con = mysql.connect()
        cursor = con.cursor()
        cursor.callproc('sp_validateLogin',(_username,))
        data = cursor.fetchall()

        if len(data) > 0:
                if check_password_hash(str(data[0][3]),_password):
                    session['user'] = data[0][0]
                    return redirect('/userHome')
                else:
                    return render_template('error.html',error = 'Wrong Email address or Password.')
        else:
            return render_template('error.html',error = 'Wrong Email address or Password.')

    except Exception as e:
        return render_template('error.html',error = str(e))

    finally:
        cursor.close()
        con.close()

@app.route('/userHome')
def userHome():
    if session.get('user'):
        return render_template('userHome.html')
    else:
        return render_template('error.html',error = 'Unauthorized Access')


@app.route('/logout')
def logout():
    session.pop('user',None)
    return redirect('/')

@app.route('/showAddWish')
def showAddWish():
    return render_template('addWish.html')


@app.route('/addWish',methods=['POST'])
def addWish():
    try:
        if session.get('user'):
            _title = request.form['inputTitle']
            _description = request.form['inputDescription']
            _user = session.get('user')
 
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.callproc('sp_addWish',(_title,_description,_user))
            data = cursor.fetchall()
 
            if len(data) is 0:
                conn.commit()
                return redirect('/userHome')
            else:
                return render_template('error.html',error = 'An error occurred!')
 
        else:
            return render_template('error.html',error = 'Unauthorized Access')
    except Exception as e:
        return render_template('error.html',error = str(e))
    finally:
        cursor.close()
        conn.close()


@app.route('/getWish',methods=['POST'])
def getWish():
    try:
        if session.get('user'):
            _user = session.get('user')

            _limit = pageLimit
            _offset = request.form['offset']

            # Connect to MySQL and fetch data
            con = mysql.connect()
            cursor = con.cursor()
            cursor.callproc('sp_GetWishByUser',(_user,))
            wishes = cursor.fetchall()

            wishes_dict = []
            for wish in wishes:
                wish_dict = {
                    'Id': wish[0],
                    'Title': wish[1],
                    'Description': wish[2],
                    'Date': wish[4]}
                wishes_dict.append(wish_dict)

            return json.dumps(wishes_dict)
        else:
            return render_template('error.html', error = 'Unauthorized Access')
    except Exception as e:
        return render_template('error.html', error = str(e))

@app.route('/getWishById',methods=['POST'])
def getWishById():
    try:
        if session.get('user'):
 
            _id = request.form['id']
            _user = session.get('user')
 
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.callproc('sp_GetWishById',(_id,_user))
            result = cursor.fetchall()
 
            wish = []
            wish.append({'Id':result[0][0],'Title':result[0][1],'Description':result[0][2]})
 
            return json.dumps(wish)
        else:
            return render_template('error.html', error = 'Unauthorized Access')
    except Exception as e:
        return render_template('error.html',error = str(e))

@app.route('/updateWish', methods=['POST'])
def updateWish():
    try:
        if session.get('user'):
            _user = session.get('user')
            _title = request.form['title']
            _description = request.form['description']
            _wish_id = request.form['id']
 
 
 
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.callproc('sp_updateWish',(_title,_description,_wish_id,_user))
            data = cursor.fetchall()
 
            if len(data) is 0:
                conn.commit()
                return json.dumps({'status':'OK'})
            else:
                return json.dumps({'status':'ERROR'})
    except Exception as e:
        return json.dumps({'status':'Unauthorized access'})
    finally:
        cursor.close()
        conn.close()

@app.route('/deleteWish',methods=['POST'])
def deleteWish():
    try:
        if session.get('user'):
            _id = request.form['id']
            _user = session.get('user')
 
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.callproc('sp_deleteWish',(_id,_user))
            result = cursor.fetchall()
 
            if len(result) is 0:
                conn.commit()
                return json.dumps({'status':'OK'})
            else:
                return json.dumps({'status':'An Error occured'})
        else:
            return render_template('error.html',error = 'Unauthorized Access')
    except Exception as e:
        return json.dumps({'status':str(e)})
    finally:
        cursor.close()
        conn.close()