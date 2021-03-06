"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import render_template, json, url_for, request
from Bootstrap_lookahead_trial import app

@app.route('/')
@app.route('/home')
def home():
    """Renders the home page."""
    return render_template(
        'index.html'
    )

@app.route('/typeahead',methods = ['POST'])
def typeAhead():
    products = [ { "id" : "0", "name" : "Deluxe Bicycle", "price" : 499.98, "imgurl" : "static\\content\\images\\icon-128.png" },
                 { "id" : "1", "name" : "Super Deluxe Trampoline", "price" : 134.99, "imgurl" : "static\\content\\images\\icon128.png" },
                 { "id" : "2", "name" : "Super Duper Scooter", "price" : 49.95, "imgurl" : "static\\content\\images\\logo_128x128.png" }]

    return json.dumps(products)


@app.route('/starClick',methods = ['POST'])
def starClick():
    _star_num = request.form['star_num']
    _item_name = request.form['item_name']

    return json.dumps({ "hello" : "world"})


@app.route('/contact')
def contact():
    """Renders the contact page."""
    return render_template(
        'contact.html',
        title='Contact',
        year=datetime.now().year,
        message='Your contact page.'
    )

@app.route('/about')
def about():
    """Renders the about page."""
    return render_template(
        'about.html',
        title='About',
        year=datetime.now().year,
        message='Your application description page.'
    )
