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

@app.route('/api/search-businesses')
def search_businesses():
    """Grab a category and location from form and return yelp results."""
    search_param = request.args.get("general-search")
    address = request.args.get("address")
    radius = request.args.get("mile_radius")
    
    #yelp uses meters, so i'm converting my miles roughly to meters
    radius = int(radius) * 1609

    endpoint_url ='https://api.yelp.com/v3/businesses/search'
    payload = {'Authorization': f'bearer {API_KEY}'}

    parameters = {'term':search_param,
                  'limit': 50,
                  'radius': radius,
                  'location': address}

    response = requests.get(url = endpoint_url, params = parameters, headers = payload)
    
    the_info = response.json()

    return the_info


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0')