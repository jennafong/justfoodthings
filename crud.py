""" CRUD operations """

from model import db, User, Restaurant, Rating, connect_to_db


def create_user(email, password):
    """Create and return a new user."""

    user = User(email=email, password=password)

    db.session.add(user)
    db.session.commit()

    return user

def show_all_users():
    """ Return a list of all user objects"""

    return User.query.all()

def get_user_by_email(email):
    """Returns user based on email"""

    return User.query.filter(User.email == email).first()

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
