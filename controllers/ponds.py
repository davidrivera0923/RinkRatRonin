from flask import render_template, session, flash, redirect, request , jsonify
import os
from proj_app import app
from proj_app.models.player import Player
from proj_app.models.pond import Pond
from werkzeug.utils import secure_filename


UPLOAD_FOLDER = '/Users/davidrivera/Desktop/CodingDojo_Assignments/proj_algos/solo_proj/proj_app/static/images'

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/get_data')
def get_data():
    return jsonify(message="RRR Data")


@app.route('/add_pond')
def add_pond():
    if 'player_id' not in session:
        return redirect('/logout')
    data = {
        "id":session['player_id']
    }
    return render_template('add_pond.html',player=Player.get_one(data))


@app.route('/create/pond', methods=['POST'])
def create_pond():
    if 'player_id' not in session:
       return redirect('/logout')
    if not Pond.validate_pond(request.form):
       return redirect('/add_pond')
    file = request.files['file']
    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        data = {
            "location":request.form['location'],
            "occur":request.form['occur'],
            "description":request.form['description'],
            "photo_upload":'/static/images/'+ filename,
            "player_id":session['player_id']
        }
        Pond.save(data)
    return redirect('/portal_rink_rat_ronin')


    

@app.route('/show/pond/<int:id>')
def show_pond(id):
    if 'player_id' not in session:
        return redirect('/logout')
    data = {
         "id":id
         
    }
    player_data = {
                "id":session['player_id']
    }
    return render_template('show_pond.html', ponds=Pond.get_one_with_players(data),players=Player.get_one(player_data))

@app.route('/edit/pond/<int:id>')
def edit_pond(id):
    if 'player_id' not in session:
        return redirect('/logout')
    data = {
         "id":id
    }
    user_data = {
              "id":session['player_id']
    }  
    return render_template('edit_pond.html', pond=Pond.get_one_with_players(data),player=Player.get_one(user_data))

@app.route('/update/pond',methods=['POST'])
def update_pond():
    if 'player_id' not in session:
       return redirect('/logout')
    if not Pond.validate_pond(request.form):
        return redirect('/new/pond')
    file = request.files['file']
    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

    data = {
         "location":request.form['location'],
         "occur":request.form['occur'],
         "description":(request.form['description']),
         "photo_upload":"/static/images/"+ filename,
         "player_id":session['player_id'],
         "id":request.form['id']

    }
    Pond.update(data)
    return redirect("/portal_rink_rat_ronin")


@app.route('/delete/pond/<int:id>')
def destroy_pond(id):
    if 'player_id' not in session:
        return redirect('/logout')
    data = {
         "id":id
    }
    Pond.destroy(data)
    return redirect('/portal_rink_rat_ronin')
