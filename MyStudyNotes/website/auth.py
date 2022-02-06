from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash  # store password as hash that cannot be translated back into plain text
from . import db
from flask_login import login_user, login_required, logout_user, current_user  # current_user is used to access all information about the current logged in user

auth = Blueprint("auth",__name__)

@auth.route("/login", methods = ['GET','POST'])  # Make sure login accepts POST request
def login():
	# Get information from the login form
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
	# find the user by email
        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)  # log the user in and keep the user logged in so the user doesnt have to log in everytime they go to the website
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Email does not exist.', category='error')

    return render_template("login.html", user=current_user)


@auth.route('/logout')
@login_required  # ensure the user cannot logged out unless they are logged in
def logout():
    logout_user()
    return redirect(url_for('auth.login'))  # Bring the user back to the log in page after they log out


@auth.route("/sign-up", methods = ['GET','POST'])
def sign_up():
	# Get information from the sign up form
	if request.method == 'POST':
		email = request.form.get('email')
		first_name = request.form.get('firstName')
		password1 = request.form.get('password1')
		password2 = request.form.get('password2')

		user = User.query.filter_by(email=email).first()
		if user:
			flash('Email already exists.', category='error')
		elif len(email) < 10:
			flash('Email must be greater than 10 characters.', category='error')
		elif len(first_name) < 2:
			flash('First name must be greater than 1 character.', category='error')
		elif password1 != password2:
			flash('Passwords don\'t match.', category='error')
		elif len(password1) < 7:
			flash('Password must be at least 7 characters.', category='error')
		else:
			# add user to the database
			new_user = User(email=email, first_name=first_name, password=generate_password_hash(password1, method='sha256'))
			db.session.add(new_user)
			db.session.commit()
			login_user(new_user, remember=True)  # After signing up, the system automaticaly logs the user in
			flash('Account created!', category='success')
			return redirect(url_for('views.home'))  # After sign up is successful, redirect to home page
	return render_template("sign_up.html", user=current_user)