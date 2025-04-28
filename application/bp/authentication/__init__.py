# application/bp/authentication/__init__.py

from flask import Blueprint, render_template, redirect, url_for, flash
from application.database import User, db
from application.bp.authentication.forms import RegistrationForm

# Create the Blueprint for authentication
authentication = Blueprint('authentication', __name__, template_folder='templates')

@authentication.route('/registration', methods=['GET', 'POST'])
def registration():
    """Handle user registration"""
    form = RegistrationForm()

    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        # Check if the email already exists in the database
        if User.find_user_by_email(email):
            flash("Already Registered", "warning")
            return redirect(url_for('authentication.registration'))

        # Create a new user
        user = User.create(email, password)
        db.session.add(user)
        db.session.commit()

        flash("Registration Successful", "success")
        return redirect(url_for('authentication.dashboard'))

    return render_template('registration.html', form=form)

@authentication.route('/dashboard')
def dashboard():
    """Display the user dashboard after login or registration"""
    # Placeholder for the dashboard route
    return render_template('dashboard.html')

@authentication.route('/user/<int:user_id>')
def user_by_id(user_id):
    """Display the user details based on the user ID"""
    user = User.find_user_by_id(user_id)
    if user:
        return render_template('user.html', user=user)
    else:
        flash("User not found", "danger")
        return redirect(url_for('authentication.dashboard'))
