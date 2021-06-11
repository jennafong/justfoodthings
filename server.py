from flask import (Flask, render_template, request, flash, session, redirect)

from pprint import pformat
import os
import requests
import json
import my_secrets


app = Flask(__name__)
app.secret_key = 'SECRETSECRETSECRET'

# This configuration option makes the Flask interactive debugger
# more useful (you should remove this line in production though)
app.config['PRESERVE_CONTEXT_ON_EXCEPTION'] = True


API_KEY = os.environ['YELP_KEY']

@app.route('/')
def homepage():
    """Show the homepage."""

    return render_template('homepage.html')

@app.route('/api/search-businesses', methods=['POST'])
def search_businesses():
    """Grab a category and location from form and return yelp results."""
    
    address = request.form.get("address")
    city = request.form.get("city")
    state = request.form.get("state")
    radius = request.form.get("mile_radius")
    
    #yelp uses meters, so i'm converting my miles roughly to meters
    radius = int(radius) * 1609

    endpoint_url ='https://api.yelp.com/v3/businesses/search'
    payload = {'Authorization': f'bearer {API_KEY}'}

    parameters = {'term':'restaurants',
                  'limit': 5,
                  'radius': radius,
                  'location': f"{address}, {city}, {state}"}

    response = requests.get(url = endpoint_url, params = parameters, headers = payload)
    
    business_data = response.json()

    if request.form['submit_button'] == 'nearby':  
        return render_template('nearby.html',
                               business_data = business_data)
    elif request.form['submit_button'] == 'random':
        return business_data
    elif request.form['submit_button'] == 'ideas':
        pass

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0')