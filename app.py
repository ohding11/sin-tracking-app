#!/usr/bin/env python3

from flask import Flask, render_template, request, redirect, url_for, make_response
from markupsafe import escape
import pymongo
import datetime
from bson.objectid import ObjectId
import os
import subprocess
from pymongo.mongo_client import MongoClient

# instantiate the app
app = Flask(__name__)

# load credentials and configuration options from .env file
# if you do not yet have a file named .env, make one based on the template in env.example
import credentials
config = credentials.get()

# turn on debugging if in development mode
if config['FLASK_ENV'] == 'development':
    # turn on debugging, if in development
    app.debug = True # debug mnode

uri = # left blank in commit for security purposes
# Create a new client and connect to the server
connection = MongoClient(uri)
db = connection["sin-tracking-app"] # store a reference to the database

# set up the routes

@app.route('/')
def home():
    """
    Route for the home page
    """
    entries = db.sins.find({})

    total_footprint = sum(entry['footprint'] for entry in entries)

    return render_template('index.html',total_footprint=total_footprint)

@app.route('/entries')
def read():
    """
    Route for GET requests to the read page.
    Displays some information for the user with links to other pages.
    """
    docs = db.sins.find({}).sort("created_at", -1) # sort in descending order of created_at timestamp
    return render_template('read.html', docs=docs) # render the read template

@app.route('/submit')
def create():
    """
    Route for GET requests to the create page.
    Displays a form users can fill out to create a new document.
    """
    return render_template('create.html') # render the create template


@app.route('/submit', methods=['POST'])
def create_post():
    """
    Route for POST requests to the create page.
    Accepts the form submission data for a new document and saves the document to the database.
    """
    category = request.form['fcat']
    notes = request.form['fnotes']

    if category == "Transportation/Shipping":
        shippingSize = float(request.form['fshipmentsize'])
        shippingDist = float(request.form['fshipmentdist'])
        dataStored = 0
        dataYears = 0
        plastic = 0
        agrLand = 0
        agrYears = 0
    if category == "Data Storage":
        shippingSize = 0
        shippingDist = 0
        dataStored = float(request.form['fdata'])
        dataYears = float(request.form['fdatayears'])
        plastic = 0
        agrLand = 0
        agrYears = 0
    if category == "Plastic Manufacturing":
        shippingSize = 0
        shippingDist = 0
        dataStored = 0
        dataYears = 0
        plastic = float(request.form['fplastic'])
        agrLand = 0
        agrYears = 0
    if category == "Agriculture":
        shippingSize = 0
        shippingDist = 0
        dataStored = 0
        dataYears = 0
        plastic = 0
        agrLand = float(request.form['fagricultureland'])
        agrYears = float(request.form['fagricultureyears'])

    footprint = (shippingSize*shippingDist*0.000000015)+(dataStored*dataYears*0.002)+(plastic*0.0025)+(agrLand*agrYears*1200000)

    doc = {
        'category': category,
        'footprint': footprint,
        'shipping_size': shippingSize,
        'shipping_dist': shippingDist,
        'data_stored': dataStored,
        'data_years': dataYears,
        'plastic': plastic,
        'agr_land': agrLand,
        'agr_years': agrYears,
        'notes': notes,
        "created_at": datetime.datetime.utcnow()
    }
    
    db.sins.insert_one(doc) # insert a new document

    return redirect(url_for('success')) # tell the browser to make a request for the /read route

@app.route('/sucess')
def success():
    """
    Success page after a report is successfully submitted
    """
    return render_template('success.html')

@app.route('/edit/<mongoid>')
def edit(mongoid):
    """
    Route for GET requests to the edit page.
    Displays a form users can fill out to edit an existing record.
    """
    doc = db.sins.find_one({"_id": ObjectId(mongoid)})
    return render_template('edit.html', mongoid=mongoid, doc=doc) # render the edit template


@app.route('/edit/<mongoid>', methods=['POST'])
def edit_post(mongoid):
    """
    Route for POST requests to the edit page.
    Accepts the form submission data for the specified document and updates the document in the database.
    """
    category = request.form['fcat']
    notes = request.form['fnotes']

    if category == "Transportation/Shipping":
        shippingSize = float(request.form['fshipmentsize'])
        shippingDist = float(request.form['fshipmentdist'])
        dataStored = 0
        dataYears = 0
        plastic = 0
        agrLand = 0
        agrYears = 0
    if category == "Data Storage":
        shippingSize = 0
        shippingDist = 0
        dataStored = float(request.form['fdata'])
        dataYears = float(request.form['fdatayears'])
        plastic = 0
        agrLand = 0
        agrYears = 0
    if category == "Plastic Manufacturing":
        shippingSize = 0
        shippingDist = 0
        dataStored = 0
        dataYears = 0
        plastic = float(request.form['fplastic'])
        agrLand = 0
        agrYears = 0
    if category == "Agriculture":
        shippingSize = 0
        shippingDist = 0
        dataStored = 0
        dataYears = 0
        plastic = 0
        agrLand = float(request.form['fagricultureland'])
        agrYears = float(request.form['fagricultureyears'])

    footprint = (shippingSize*shippingDist*0.000000015)+(dataStored*dataYears*0.002)+(plastic*0.0025)+(agrLand*agrYears*1200000)

    doc = {
        'category': category,
        'footprint': footprint,
        'shipping_size': shippingSize,
        'shipping_dist': shippingDist,
        'data_stored': dataStored,
        'data_years': dataYears,
        'plastic': plastic,
        'agr_land': agrLand,
        'agr_years': agrYears,
        'notes': notes,
        "created_at": datetime.datetime.utcnow()
    }

    db.sins.update_one(
        {"_id": ObjectId(mongoid)}, # match criteria
        { "$set": doc }
    )

    return redirect(url_for('read')) # tell the browser to make a request for the /read route


@app.route('/delete/<mongoid>')
def delete(mongoid):
    """
    Route for GET requests to the delete page.
    Deletes the specified record from the database, and then redirects the browser to the read page.
    """
    db.sins.delete_one({"_id": ObjectId(mongoid)})
    return redirect(url_for('read')) # tell the web browser to make a request for the /read route.

@app.route('/webhook', methods=['POST'])
def webhook():
    """
    GitHub can be configured such that each time a push is made to a repository, GitHub will make a request to a particular web URL... this is called a webhook.
    This function is set up such that if the /webhook route is requested, Python will execute a git pull command from the command line to update this app's codebase.
    You will need to configure your own repository to have a webhook that requests this route in GitHub's settings.
    Note that this webhook does do any verification that the request is coming from GitHub... this should be added in a production environment.
    """
    # run a git pull command
    process = subprocess.Popen(["git", "pull"], stdout=subprocess.PIPE)
    pull_output = process.communicate()[0]
    # pull_output = str(pull_output).strip() # remove whitespace
    process = subprocess.Popen(["chmod", "a+x", "flask.cgi"], stdout=subprocess.PIPE)
    chmod_output = process.communicate()[0]
    # send a success response
    response = make_response('output: {}'.format(pull_output), 200)
    response.mimetype = "text/plain"
    return response

@app.errorhandler(Exception)
def handle_error(e):
    """
    Output any errors - good for debugging.
    """
    return render_template('error.html', error=e) # render the edit template


if __name__ == "__main__":
    #import logging
    #logging.basicConfig(filename='/home/ak8257/error.log',level=logging.DEBUG)
    app.run(debug = True)
