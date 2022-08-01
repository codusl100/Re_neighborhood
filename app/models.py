from flask_sqlalchemy import SQLAlchemy

import flask_bcrypt

db = SQLAlchemy()
class Fcuser(db.Model):
    __tablename__ = 'fcuser'
    id = db.Column(db.Integer, primary_key=True)
    useremail = db.Column(db.String(32), unique=True, nullable=False, index=True)
    username = db.Column(db.String(8), unique=True, nullable=False, index=True)
    password = db.Column(db.String(64), nullable=False)

    @property
    def password(self):
        raise AttributeError('password: write-only field')

    @password.setter
    def password(self, password):
        self.password_hash = flask_bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return flask_bcrypt.check_password_hash(self.password_hash, password)

    def __repr__(self):
        return "<user '{}'>".format(self.username)