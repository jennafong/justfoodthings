""" CRUD operations """

from model import db, User, Restaurant, Rating, connect_to_db


def create_user(email, username, password):
    """Create and return a new user."""

    user = User(email=email, username=username)

    user.set_password(password)

    db.session.add(user)
    db.session.commit()

    return user

def show_all_users():
    """ Return a list of all user objects"""

    return User.query.all()

def get_user_by_email(email):
    """Returns user based on email"""

    return User.query.filter(User.email == email).first()

def get_user_by_username(username):
    """Returns user based on username"""

    return User.query.filter(User.username == username).first()

def create_restaurant(restaurant_name, yelp_id, yelp_url):
    """Adds a restaurant to the db so that it can be rated."""

    restaurant = Restaurant(restaurant_name = restaurant_name,
                            yelp_id = yelp_id, yelp_url = yelp_url)
    
    db.session.add(restaurant)
    db.session.commit()

    return restaurant

def check_for_restaurant(restaurant_yelp_id):
    """Checks db for existing restaurant. Returns restaurant_id if
    restaurant exists and False if restaurant does not exist."""
    if Restaurant.query.filter(Restaurant.yelp_id == restaurant_yelp_id).first() is None:
        return False
    else:
        return restaurant_yelp_id

def get_restaurant_id(restaurant_yelp_id):
    """Takes a yelp_id for a restaurant and returns the restaurant_id."""
    
    return Restaurant.query.filter(Restaurant.yelp_id == restaurant_yelp_id).first().restaurant_id
    

def get_rating_by_user_restaurant(user, restaurant):
    """Returns a rating based on user and restaurant."""

    return Rating.query.filter(Rating.user_id == user, Rating.restaurant_id == restaurant).first()

def replace_rating(score, user, restaurant):
    """Only allows a user to have a restaurant listed once."""

    existing_rating = get_rating_by_user_restaurant(user, restaurant)
    existing_rating.update_rating(score)
    db.session.commit()

    return existing_rating


def create_rating(score, user, restaurant):
    """Create and return a new rating.
    user and restaurant should be objects."""

    rating = Rating(score=score, user=user, restaurant=restaurant)

    db.session.add(rating)
    db.session.commit()

    return rating




if __name__ == '__main__':
    from server import app
    connect_to_db(app)
