from flask_app import app
from flask import render_template, request, redirect, flash, session
from flask_app.models.user_model import User
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)

# Displaying the login page/route
@app.route('/')
def display_login():
    return render_template('login.html')

# Validating registration inputs from the route/form
@app.route('/user/registration', methods = ['POST'])
def process_registration():
    # Validate the registration html-form using the static validate_registration method in the user_model
    if User.validate_registration(request.form) == False: 
        return redirect('/') 
    # Validate if the user email already exists
    user_exists = User.get_one_to_validate_email(request.form)
    if user_exists != None:
        flash("This email already exists!", "error_registration_email")
        return redirect ('/')
    # Data to be sent to model from html request-form after password has been hashed using Bcrypt
    data = {
        **request.form,
        "password" : bcrypt.generate_password_hash(request.form['password'])#<=====password being hashed by Decrypt
    }
    #Create the user and start session after validation of email. Use the User.create class method from user_model to create user from data created from login.html form
    user_id = User.create(data) #<========= id sent from query in class method User.create. Set instance user_id to be used for session
    # Setting session values: these can change depending on wireframe
    session['first_name'] = data["first_name"] #<====== creating session first_name from request.form data
    session['last_name'] = data["last_name"] #<====== creating session first_name from request.form data
    session['email'] =  data["email"]#<======== creating session email from request.form data
    session['user_id'] = user_id #<============ creating session user_id from class method
    return redirect('/dashboard') #<============= If all validation passes - send user to recipes page

# Validating login inputs from the route/form
@app.route('/user/login', methods = ['POST'])
def process_login():
    current_user = User.get_one_to_validate_email(request.form) #<===current_user instance from User class validation method
    if current_user != None: #<====== If current_user exists
        if not bcrypt.check_password_hash(current_user.password, request.form['password']): #<=========check if password entered matches hashed password in db for current_user 
            flash("Wrong credentials", "error_login_credentials")
            return redirect('/')
        # Setting session values: these can change depending on wireframe
        session['first_name'] = current_user.first_name #<====== creating session first_name from current_user instance (user from db)
        session['email'] =  current_user.email#<======== creating session email from from current_user instance(user from db)
        session['user_id'] = current_user.id #<============ creating session user_id from current_user instance(user from db)
        return redirect('/dashboard') #<============= If all validation passes - send user to sightings page
    else:
        flash("Wrong credentials", "error_login_credentials")
        return redirect('/')

@app.route('/user/logout')
def process_logout():
    session.clear()
    return redirect('/')