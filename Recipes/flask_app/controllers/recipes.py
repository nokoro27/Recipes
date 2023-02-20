from flask_app import app
from flask import render_template, redirect, request, session
from flask_app.models.user import User
from flask_app.models.recipe import Recipe


@app.route('/')
def mainPage():
    return render_template('login.html')

@app.route('/register', methods=["POST"])
def registerNewUser():
    #call User model to input new user in database redirect to users/id
    data = {
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'], 
        "email" : request.form['email'], 
        "password" : request.form['password1'], 
        "confirm_password" : request.form['password2'],
    }
    session['first_name'] = data["first_name"]
    session['last_name'] = data["last_name"]
    session['email'] = data["email"]

    print("Form Data", data)
    id = User.insertNewUser(data)

    if User.validateRegistration(data):
        session['id'] = id
        return redirect(f'/users/{id}')
    else: 
        return redirect('/')

@app.route('/login', methods=["POST"])
def loginUser():
    #match email and password to user in the database and redirect to users/id
    data = {
        "email" : request.form['email'],
        "password": request.form['password']
    }
    user = User.validateLogin(data)

    session['email'] = data['email']

    if not user:
        return redirect('/')

    session['id'] = user.id

    return redirect(f'/users/{session["id"]}')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

@app.route('/users/<int:id>')
def userDashboard(id):
    #Display user's recipes with options to logout, view more, create a new one , view instrutions, edit or delete
    if not 'id' in session:
        print('id not in session... redirecting')
        return redirect('/')

    if session["id"] != id:
        print('id in session, but incorrect id redirecting to session id')
        return redirect(f'/users/{session["id"]}')

    user = User.getUserbyId(id)

    recipes = Recipe.getAllRecipes()

    return render_template('user_dashboard.html', user= user, recipes = recipes)