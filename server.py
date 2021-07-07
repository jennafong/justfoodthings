from flask import (Flask, render_template, request, flash, session, redirect, url_for)
from flask_login import LoginManager, current_user, login_user, logout_user, login_required
# remove if you don't end up using this
from pprint import pformat

import os
import requests
import json
import my_secrets
from random import randint
import crud

app = Flask(__name__)
app.secret_key = 'SECRETSECRETSECRET'
login = LoginManager(app)
login.login_view = '/loginpage'

import model


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
        # could make an array of days =
        for hours in yelp_hours_list:
            if hours['day'] == 0:
                days_dict['Monday'] = business_hours(hours)
            if hours['day'] == 1:
                days_dict['Tuesday'] = business_hours(hours)
            if hours['day'] == 2:
                days_dict['Wednesday'] = business_hours(hours)
            if hours['day'] == 3:
                days_dict['Thursday'] = business_hours(hours)
            if hours['day'] == 4:
                days_dict['Friday'] = business_hours(hours)
            if hours['day'] == 5:
                days_dict['Saturday'] = business_hours(hours)
            if hours['day'] == 6:
                days_dict['Sunday'] = business_hours(hours)

        return days_dict

    return dict(day_determiner = day_determiner)

@app.route('/')
def homepage():
    """Show the homepage."""

    return render_template('homepage.html')

@app.route('/loginpage')
def login_page():
    """Show the login/create account page."""

    return render_template('login.html')

@login.user_loader
def load_user(id):
    return model.User.query.get(int(id))

@app.route("/login", methods = ['GET', 'POST'])
def loginuser():
    """Log user in and add user info to session"""

    if current_user.is_authenticated:
            return redirect('/')

    user_email = request.form['user_email']
    user_password = request.form['password']

    user = crud.get_user_by_email(user_email)

    if user == None:
        flash('That login doesn\'t exist. Sorry bro.')
        return redirect('/loginpage')
    else:
        if user is None or not user.check_password(user_password):
            flash('Invalid username or password.')
            return redirect('/loginpage')
        else:
            login_user(user)
            flash('Login Successful')
            return redirect('/')

@app.route('/users', methods = ['POST'])
def create_login():

    user_email = request.form['user_email']
    user_name = request.form['username']
    user_password = request.form['password']

    user = crud.get_user_by_email(user_email)
    suggested_username = crud.get_user_by_username(user_name)

    if user != None:
        flash('Email already in use; please use another.')
        return redirect('/loginpage') 
    if suggested_username != None:
        flash('Username already taken; please use another.')
        return redirect('/loginpage')  
    else:
        crud.create_user(user_email, user_name, user_password)
        flash('Account created! Please log in to access your account.')
        return redirect('/loginpage')

@app.route('/logout')
def logout():
        logout_user()
        flash('See you next time, space foodie!')
        return redirect('/')

@app.route('/api/search-businesses', methods=['POST'])
def search_businesses():
    """Grab a location and radius from the homepage form and return yelp results."""
    
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

@app.route('/iwenthere/<id>', methods = ['GET', 'POST'])
@login_required
def i_went_here(id):
    """Page for users to rate a restaurant and write something about it."""

    endpoint_url = f"https://api.yelp.com/v3/businesses/{id}"
    payload = {'Authorization': f'bearer {API_KEY}'}

    response = requests.get(url = endpoint_url, headers = payload)

    detail_data = response.json()

    return render_template('iwenthere.html',
                           data = detail_data)


@app.route('/rating/<id>', methods = ['GET', 'POST'])
@login_required
def rate_restaurant(id):
    """Get a restaurant rating. Save it to db. Display it to User."""

    endpoint_url = f"https://api.yelp.com/v3/businesses/{id}"
    payload = {'Authorization': f'bearer {API_KEY}'}

    response = requests.get(url = endpoint_url, headers = payload)

    detail_data = response.json()

    user = current_user
    score = request.form.get('submit_button')

    # need to check if restaurant is already in db
    if crud.check_for_restaurant(detail_data['id']):
        user = current_user.id
        restaurant = crud.get_restaurant_id(detail_data['id'])
        crud.replace_rating(score, user, restaurant)
        return redirect(f'/iwenthere/{id}')
    else:
        restaurant = crud.create_restaurant(detail_data['name'], detail_data['id'], detail_data['url'])

        crud.create_rating(score, user, restaurant)

        return redirect(f'/iwenthere/{id}')

        # if request.form['submit_button'] == 'Excellent': 
        #     crud.create_rating("Excellent", user, restaurant)
        #     return redirect(f'/iwenthere/{id}')
                            
        # elif request.form['submit_button'] == 'Good':
        #     crud.create_rating("Good", user, restaurant)
        #     return redirect(f'/iwenthere/{id}')
            
        # elif request.form['submit_button'] == 'Neutral':
        #     crud.create_rating("Neutral", user, restaurant)
        #     return redirect(f'/iwenthere/{id}')

        # elif request.form['submit_button'] == 'Bad':
        #     crud.create_rating("Bad", user, restaurant)
        #     return redirect(f'/iwenthere/{id}')
            
        # elif request.form['submit_button'] == 'Abhorrent':
        #     crud.create_rating("Abhorrent", user, restaurant)
        #     return redirect(f'/iwenthere/{id}')

@app.route('/account')
@login_required
def show_account_details():
    """Shows details of a user's account."""
    user_email = current_user.email 
    user_name = current_user.username

    return render_template('account.html',
                            email = user_email,
                            username = user_name)

if __name__ == '__main__':
    model.connect_to_db(app)
    app.debug = True
    app.run(host='0.0.0.0')