from flask import (Flask, render_template, request, flash, session, redirect)

# remove if you don't end up using this
from pprint import pformat
import os
import requests
import json
import my_secrets
from random import randint


app = Flask(__name__)
app.secret_key = 'SECRETSECRETSECRET'

# This configuration option makes the Flask interactive debugger
# more useful (you should remove this line in production though)
app.config['PRESERVE_CONTEXT_ON_EXCEPTION'] = True


API_KEY = os.environ['YELP_KEY']


def military_to_standard(num):
    """Converts a number from miliary time (0000) to standard time 12:00 AM"""
    biz_hours = int(num[0:2])
    biz_minutes = int(num[2:4])

    if biz_minutes < 10:
        biz_minutes = f'0{biz_minutes}'

    if biz_hours <= 12:
        return f"{biz_hours}:{biz_minutes} AM"

    else: 
        the_pms = biz_hours - 12
        return f"{the_pms}:{biz_minutes} PM"
        

def business_hours(yelp_hours_dict):
    """Takes in the yelp data for business hours,
    {'is_overnight': False, 'start': '1700', 'end': '2100', 'day': 2},
    and returns either '24 hours', standard/normal 
    time, or 'Closed' for any given day."""

    if yelp_hours_dict['is_overnight'] == True:
        return 'Open 24 Hours'
    
    elif yelp_hours_dict['is_overnight'] == False:
        return f"{military_to_standard(yelp_hours_dict['start'])} - {military_to_standard(yelp_hours_dict['end'])}"

   

@app.context_processor
def format_biz_hours():
    def day_determiner(yelp_hours_list):
        """Takes in a list of dictionaries containing yelp hours dictionaries,
        [{'is_overnight': False, 'start': '1700', 'end': '2100', 'day': 2},...],
        and returns a dictionary containing a business's hours."""
        
        days_dict = {
            'Monday': 'Closed',
            'Tuesday': 'Closed',
            'Wednesday': 'Closed',
            'Thursday': 'Closed',
            'Friday': 'Closed',
            'Saturday': 'Closed',
            'Sunday': 'Closed'
        }
        # update dictionary with provided times from dictionaries in the list
        # possibly need to index or have a counter because the day determines the hours
        for hours in yelp_hours_list:
            hours['day']

        return days_dict
        # days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        # days_abbr = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
        # count = 0

        # while count >= 6:
        #     #get a list of dictionaries
        #     #loop through. print the day name. if the item we are looking at is not for the right day, print closed
        #     # if the item we are looking at IS for the right day print the time using the biz hour conversion function
        #     # for to do later default to closed and if it has a 'day' then replace with hours


        #     # for dict in yelp_hours_list:
        #     #     if dict.get('day', count) is count:
        #     #         return f'{days[count]}: {business_hours(dict)}'
        #     #     else:
        #     #         return f'{days[count]}: Closed'
        #     #     count += 1

    return dict(day_determiner = day_determiner)


@app.route('/')
def homepage():
    """Show the homepage."""

    return render_template('homepage.html')

@app.route('/api/search-businesses', methods=['POST'])
def search_businesses():
    """Grab a location and radius from form and return yelp results."""
    
    address = request.form.get("address")
    city = request.form.get("city")
    state = request.form.get("state")
    radius = request.form.get("mile_radius")
    
    #yelp uses meters, so i'm converting my miles roughly to meters
    radius = int(radius) * 1609

    endpoint_url ='https://api.yelp.com/v3/businesses/search'
    payload = {'Authorization': f'bearer {API_KEY}'}

    parameters = {'term':'restaurants',
                  'limit': 10,
                  'radius': radius,
                  'location': f"{address}, {city}, {state}"}

    response = requests.get(url = endpoint_url, params = parameters, headers = payload)
    
    business_data = response.json()
    my_data = business_data['businesses']

    if request.form['submit_button'] == 'nearby':  
        return render_template('nearby.html',
                               my_data = my_data)
    elif request.form['submit_button'] == 'random':
        rando_num = randint(0,9)
        return redirect(f'/details/{my_data[rando_num]["id"]}')
        
    elif request.form['submit_button'] == 'ideas':
        return render_template('ideas.html',
                               my_data = my_data)

@app.route('/details/<id>')
def show_details(id):    
    """Shows more details about a singular restaurant."""

    endpoint_url = f"https://api.yelp.com/v3/businesses/{id}"
    payload = {'Authorization': f'bearer {API_KEY}'}

    response = requests.get(url = endpoint_url, headers = payload)

    detail_data = response.json()

    return render_template('details.html',
                           data = detail_data)


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0')