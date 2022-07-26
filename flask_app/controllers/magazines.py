from flask_app import app
from flask import render_template, request, redirect, session, flash
from flask_app.models.magazine import Magazine

@app.route('/dashboard')
def success():
    if 'user_email' not in session:
        return redirect('/')
    magazines = Magazine.get_all_magazines()
    
    return render_template('dashboard.html', magazines=magazines)

@app.route('/magazine/new')
def display_new():
    if 'user_email' not in session:
        return redirect('/')
    return render_template("new_magazine.html")

@app.route('/view_magazine/<int:id>')
def view_magazine(id):
    if 'user_email' not in session:
        return redirect('/')
    data = {
        'id': id
    }
    magazine = Magazine.get_single_magazine(data)
    subscribers = Magazine.get_magazine_subscribers(data)
    return render_template("show_magazine.html", magazine=magazine, subscribers=subscribers)

@app.route('/dashboard/create', methods=['post'])
def create_magazine():
    if 'user_email' not in session:
        return redirect('/')
    #validate

    if Magazine.validate_magazine(request.form) == False:
        print('validation failed')
        return redirect('/magazine/new')
    else:
        #create magazine
        data = {
            'name': request.form['name'],
            'description': request.form['description'],
            'user_id': session['user_id']
        }
        
        Magazine.create_magazine(data)
        return redirect('/dashboard')

@app.route('/delete_magazine/<int:id>')
def delete_magazine(id):
    data = {
        'id': id
    }
    print(data)
    Magazine.delete_magazine(data)
    return redirect('/dashboard')

# @app.route('/edit_user/<int:id>')
# def edit_user(id):
#     if 'user_email' not in session:
#         return redirect('/')
#     data = {
#         'id': id
#     }
#     magazine = Magazine.get_magazine_to_edit(data)
#     print(magazine)
#     return render_template("replant_magazine.html", magazine=magazine)

@app.route('/dashboard/edit/<int:id>', methods={'post'})
def update(id):
    if 'user_email' not in session:
        return redirect('/')
    #validate
    if Magazine.validate_magazine(request.form) == False:
        print('validation failed')
        return redirect(f'/edit_magazine/{id}')
    else:
        #create magazine
        data = {
            'name': request.form['name'],
            'description': request.form['description'],
            'id': id
        }
        
        Magazine.update_magazine(data)
        return redirect(f'/view_magazine/{id}')

@app.route('/subscribe_magazine/<int:id1>/<int:id2>')
def subscribe_magazine(id1, id2):
    if 'user_email' not in session:
        return redirect('/')
    data = {
        'magazine_id': id1,
        'user_id': id2
    }
    subscribers = Magazine.subscribe(data)
    return redirect(f"/view_magazine/{id1}")