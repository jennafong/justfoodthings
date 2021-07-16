"""Models for JustFoodThings app."""

from flask_sqlalchemy import SQLAlchemy
import my_secrets
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

db = SQLAlchemy()


# Replace this with your code!


def connect_to_db(flask_app, db_uri='postgresql:///restaurant_thoughts', echo=True):
    flask_app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    flask_app.config['SQLALCHEMY_ECHO'] = echo
    flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.app = flask_app
    db.init_app(flask_app)
    

    print('Connected to the db!')

class User(UserMixin, db.Model):
    """A user."""

    __tablename__ = 'users'
  
    id = db.Column(db.Integer,
                        autoincrement=True,
                        primary_key=True)
    username = db.Column(db.String(64),
                         unique=True)                    
    email = db.Column(db.String(120), 
                      unique=True)
    password_hash = db.Column(db.String(128))

    # ratings = a list of Rating objects

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User user_id={self.id} email={self.email}>'



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
    """A rating of a restaurant."""

    __tablename__ = 'ratings'

    rating_id = db.Column(db.Integer,
                        autoincrement=True,
                        primary_key=True)
    score = db.Column(db.String)
    comments = db.Column(db.Text)
    restaurant_id = db.Column(db.Integer, 
                              db.ForeignKey('restaurants.restaurant_id'))
    user_id = db.Column(db.Integer, 
                        db.ForeignKey('users.id'))
    # stretch goal data. if implementing, I think i have to delete the db and start over. 
    # blacklist = db.Column(db.Boolean,
    #                      nullable=False,
    #                      default=True)
    # favorite =  db.Column(db.Boolean)

    restaurant = db.relationship('Restaurant', backref='ratings')
    user = db.relationship('User', backref='ratings')

    def update_rating(self, new_score):
        """Updates an existing rating."""

        self.score = new_score

    def comment(self, comment):
        """Adds a comment to a rating."""

        self.comments = comment

    def __repr__(self):
        return f'<Rating rating_id={self.rating_id} score={self.score}>'

if __name__ == '__main__':
    from server import app

    # Call connect_to_db(app, echo=False) if your program output gets
    # too annoying; this will tell SQLAlchemy not to print out every
    # query it executes.

    connect_to_db(app)