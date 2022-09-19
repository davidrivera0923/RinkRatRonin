from flask import render_template, session,redirect, request,flash
import re
from flask_bcrypt import Bcrypt
from proj_app import app
from proj_app.models.player import Player
from proj_app.models.pond import Pond
bcrypt = Bcrypt(app)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/register", methods=["POST"])
def register():
    is_valid = Player.validate_register(request.form)
    if not is_valid:
        return redirect("/")
    new_player = {
        "first_name": request.form["first_name"],
        "last_name": request.form["last_name"],
        "email": request.form["email"],
        "password": bcrypt.generate_password_hash(request.form["password"]),
    }
    id = Player.save(new_player)
    print(id)
    session['player_id'] = id
    return redirect("/portal_rink_rat_ronin")

@app.route("/login",methods=['POST'])
def login():
    data = {
        "email": request.form['email']
    }
    player = Player.get_by_email(data)
    print("**********************************")
    print(player.id)
    if not player:
        flash("Invalid Email","login")
        return redirect("/")
    
    if not bcrypt.check_password_hash(player.password,request.form['password']):
        flash("Invalid Password","login")
        return redirect("/")
    session['player_id'] = player.id
    return redirect('/portal_rink_rat_ronin')
    

@app.route("/portal_rink_rat_ronin", methods=['GET','POST'])
def dashboard():
    if 'player_id' not in session:
        return redirect("/")
    data = {
        "id": session["player_id"]
    }
    player = Player.get_one(data)
    ponds = Pond.get_all()
    return render_template("portal_rink_rat_ronin.html", player=player,ponds=ponds)

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")