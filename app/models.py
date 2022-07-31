from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
class Fcuser(db.Model):
    __tablename__ = 'fcuser'
    id = db.Column(db.Integer, primary_key=True)
    useremail = db.Column(db.String(32), unique=True, nullable=False, index=True)
    username = db.Column(db.String(8), unique=True, nullable=False, index=True)
    password = db.Column(db.String(64), nullable=False)