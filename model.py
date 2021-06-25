"""Models for JustFoodThings app."""

from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin
import my_secrets

db = SQLAlchemy()


# Replace this with your code!


def connect_to_db(flask_app, db_uri='postgresql:///ratings', echo=True):
    flask_app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    flask_app.config['SQLALCHEMY_ECHO'] = echo
    flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    flask_app.config['SECRET_KEY'] = my_secrets.FLASK_SECRET_KEY

    db.app = flask_app
    db.init_app(flask_app)

    print('Connected to the db!')

class User(db.Model):
    """A user."""

    __tablename__ = 'users'

    user_id = db.Column(db.Integer,
                        autoincrement=True,
                        primary_key=True)
    email = db.Column(db.String, unique=True)
    password = db.Column(db.String)

    # ratings = a list of Rating objects

    def __repr__(self):
        return f'<User user_id={self.user_id} email={self.email}>'


class Restaurant(db.Model):
    """A restaurant."""

    __tablename__ = 'restaurants'

    restaurant_id = db.Column(db.Integer,
                        autoincrement=True,
                        primary_key=True)
    restaurant_name = db.Column(db.String)
    yelp_id = db.Column(db.Text)
    yelp_url = db.Column(db.String)

    # ratings = a list of Rating objects

    def __repr__(self):
        return f'<Restaurant restaurant_id={self.restaurant_id} restaurant_name={self.restaurant_name}>'


class Rating(db.Model):
    """A rating."""

    __tablename__ = 'ratings'

    rating_id = db.Column(db.Integer,
                        autoincrement=True,
                        primary_key=True)
    score = db.Column(db.Integer)
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurants.restaurant_id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    # stretch goal data. if implementing, I think i have to delete the db and start over. 
    # blacklist = db.Column(db.Boolean,
    #                      nullable=False,
    #                      default=True)
    # favorite =  db.Column(db.Boolean)

    restaurant = db.relationship('Restaurant', backref='ratings')
    user = db.relationship('User', backref='ratings')

    def __repr__(self):
        return f'<Rating rating_id={self.rating_id} score={self.score}>'

if __name__ == '__main__':
    from server import app

    # Call connect_to_db(app, echo=False) if your program output gets
    # too annoying; this will tell SQLAlchemy not to print out every
    # query it executes.

    connect_to_db(app)