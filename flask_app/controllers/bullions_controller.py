from flask_app import app
from flask import render_template, request, redirect, flash, session
from flask_app.models.bullion_model import Bullion

@app.route('/dashboard')
def display_bullions():
    if 'email' not in session: #<============Validate user logged in (permission to view page) with validated email via session. If not redirect to login
        return redirect('/')
    list_bullions = Bullion.get_all_with_users()
    return render_template('dashboard.html', list_bullions = list_bullions)

    # Routes to create sighting html page after validation of user email in session
@app.route('/bullion/new')
def display_create_bullion():
    if 'email' not in session: #<============Validate user logged in (permission to view page) with validated email via session. If not redirect to login
        return redirect('/')
    return render_template("create_bullion.html")

@app.route('/bullion/create', methods = ['POST'])
def create_bullion():
    if Bullion.validate_bullion(request.form) == False: #<===========Validate all inputs from request form via the validate_sighting staticmethod in the sighting_model
        return redirect('/bullion/new')
    # Create the data dict from the validated request form inputs
    data = {
        **request.form,
        "user_id" : session['user_id']
    }
    Bullion.create(data) #<============== Pass the data to the Sighting.create method in the sighting_model
    return redirect('/dashboard')

@app.route ('/bullion/<int:id>/update')
def display_update_bullion(id):
    if 'email' not in session: #<============Validate user logged in (permission to view page) with validated email via session. If not redirect to login
        return redirect('/')
    data = {
        "id" : id
    }
    current_bullion = Bullion.get_one_with_user(data)
    return render_template("update_bullion.html", current_bullion = current_bullion )

@app.route('/bullion/update/<int:id>', methods =['POST'])
def update_bullion(id):
    if bullion.validate_bullion(request.form) == False: #<===========Validate all inputs from request form via the validate_recipe staticmethod in the sighting_model
        return redirect(f'/bullion/{id}/update')
    sighting_data = { #<================grabs data from request form and creates an instance
        **request.form,
        "id" : id,
        "user_id" : session['user_id']
    }
    Bullion.update_one(bullion_data)
    return redirect('/dashboard')

@app.route('/bullion/<int:id>')
def display_one(id):
    if 'email' not in session: #<============Validate user logged in (permission to view page) with validated email via session. If not redirect to login
        return redirect('/')
    data = {
        "id" : id
    }
    current_bullion = Bullion.get_one_with_user(data) #<======== id from data dict is passed into the Sighting.get_one_with_user and set to current_sighting
    return render_template("bullion.html", current_bullion = current_bullion)

@app.route ('/bullion/<int:id>/delete')
def delete_bullion(id):
    data = {
        "id" : id
    }
    Bullion.delete_one(data)
    return redirect('/dashboard')