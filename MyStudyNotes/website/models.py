# A database for users and a database for notes
from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class Note(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	data = db.Column(db.String(100000000))
	subject = db.Column(db.String(10))
	date = db.Column(db.DateTime(timezone = True), default=func.now())  # telling the databse to include time whenever a new record is created
	# Use a foreign key to establish a relationship between the notes table and the users table
	user_id = db.Column(db.Integer, db.ForeignKey("user.id"))

class User(db.Model, UserMixin):
	id = db.Column(db.Integer, primary_key = True)  # set User ID to be the primary key. ID has type int.
	email = db.Column(db.String(150), unique=True)  # max lenght of email is 150 characters, no pair of users can have the same email.
	password = db.Column(db.String(150))
	first_name = db.Column(db.String(150))
	# Establish a one to many relationship so a user (in the User table) can find their notes (in the Note table)
	notes = db.relationship("Note")