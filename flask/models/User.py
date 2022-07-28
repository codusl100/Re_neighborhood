import db as db


class User(db.Model):
    username = db.Column(db.String(150), unique = True, nullable = False)
    password = db.Column(db.String(200), nullable = False)
    address = db.Column(db.String(500), nullable = False)