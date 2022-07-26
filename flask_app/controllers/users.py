from flask_app import app
from flask import render_template, request, redirect, session, flash
from flask_app.models.user import User
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/register', methods=['post'])
def register():
    if User.validate_user(request.form):
        print("registration OK")
        pw_hash = bcrypt.generate_password_hash(request.form['password'])
        print(pw_hash)

        data = {
            'first_name': request.form['first_name'],
            'last_name': request.form['last_name'],
            'email': request.form['email'],
            'password': pw_hash
        }
        user = User.create_user(data)

        session['user_id'] = user
        session['user_first_name'] = data['first_name']
        session['user_last_name'] = data['last_name']
        session['user_email'] = data['email']
        return redirect("/dashboard")
    else:
        print("Validation Fails")
        return redirect("/")

@app.route('/login', methods=['post'])
def login():
    data = {
        'email': request.form['email']
    }
    user = User.get_user_by_email(data)

    if not user or request.form['email'] == '':
        flash("Email login in is incorrect. Try Again!", "error_message_email")
        print(request.form['password'])
        return redirect('/')
    
    if not bcrypt.check_password_hash(user.password, request.form['password']):
        flash("Invalid Email/Password", "error_message_pw")
        return redirect('/')

    session['user_id'] = user.id
    session['user_first_name'] = user.first_name
    session['user_last_name'] = user.last_name
    session['user_email'] = user.email
    return redirect('/dashboard')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

@app.route('/show_user_account/<int:id>')
def view_account(id):
    if 'user_email' not in session:
        return redirect('/')
    data = {
        'id': id
    }
    user = User.get_user_to_edit(data)
    magazines = User.users_magazines_count(data)
    print(magazines)

    return render_template("account.html", user=user, magazines=magazines)


@app.route('/edit_user', methods=['post'])
def edit_user():
    if User.validate_user_edits(request.form):
        print("registration OK")
    else: 
        print("Validation Fails")
        return redirect(f'/show_user_account/{session["user_id"]}')
    
    data = {
        'id': session['user_id'],
        'first_name': request.form['first_name'],
        'last_name': request.form['last_name'],
        'email': request.form['email']
    }
    
    print(session['user_id'])
    User.update_user(data)


    return redirect(f'/show_user_account/{session["user_id"]}')