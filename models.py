from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable =False)
    # Ein User kann viele Filme haben
    movies = db.relationship('Movie', backref='user', cascade="all, delete-orphan", lazy=True)

    def __repr__(self):
        return f"<User {self.name}>"

class Movie(db.Model):
    __tablename__ = 'movies'

    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100), nullable =False)
    director = db.Column(db.String(100), nullable = False)
    year = db.Column(db.Integer)
    poster_url = db.Column(db.String(200), nullable = False)
    # Fremdschlüssel verweist auf die Tabelle 'users'
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)


