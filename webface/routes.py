from . import app
from flask import render_template, request, Flask, session, redirect, url_for
from datetime import timedelta
from pony.orm import db_session, select
from random import choice
import functools
from .models import Uzivatel, Fakt, Citat
from werkzeug.security import check_password_hash, generate_password_hash

app.secret_key = "hello"
app.permanent_session_lifetime = timedelta(minutes=5)

@app.route('/register/', methods=["GET","POST"])
@db_session
def register():
    if request.method == "POST":
        name = request.form.get("nm")
        password = request.form.get("pswd")
        password_again = request.form.get("pswd2")
        if name:
            if not Uzivatel.get(login = name):
                if password == password_again:
                    user = Uzivatel(login = name, password = generate_password_hash(password))
                    session["user"] = user.login
                    return redirect(url_for("uvod"))
    return render_template("register.html.j2") 

def login_required(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if "user" in session:
           return func(*args, **kwargs)
        else: 
            return redirect(url_for("login"))

    return wrapper

@app.route("/login/", methods=["POST", "GET"])
@db_session
def login():
    title = "Login"
    if request.method == "POST":
        session.permanent = True
        user  =request.form["nm"]
        password = request.form["pswd"]
        if user and password:
            if Uzivatel.get(login = user):
                user_db = Uzivatel.get(login = user)
                if check_password_hash(user_db.password, password):
                    session["user"] = user
                    return redirect(url_for("uvod"))
        return render_template("login_user.html.j2", title=title)            
    else:
        if "user" in session:
            return redirect(url_for("uvod"))
        return render_template("login_user.html.j2", title=title)

@app.route("/user/")
def user():
    if "user" in session:
        user = session["user"]
        return f"<h1>{user}</h1>"
    else:
        return redirect(url_for("login"))

@app.route("/logout/")
def logout():
    session.pop("user", None)
    return redirect(url_for("login"))
     
@app.route("/")
@login_required
def uvod():
    title = "Úvod"
    return render_template("uvod.html.j2", title=title)


@app.route("/citaty/", methods=["POST", "GET"])
@login_required
@db_session
def citaty():
    title = "Citáty"
    if request.method == "POST":
        citat = request.form.get("citat")
        autor = request.form.get("autor")
        if citat and autor:
            Citat(text = citat, autor = autor)
            return redirect(url_for("citaty"))
    return render_template("citaty.html.j2", title=title, citaty = list(select(e for e in Citat)))

@app.route("/fakta/", methods=["POST", "GET"])
@login_required
@db_session
def fakta():
    title = "Fakta"
    if request.method == "POST":
        fakt = request.form.get("fakt")
        if fakt:
            Fakt(text = fakt)
            return redirect(url_for("fakta"))
    return render_template("fakta.html.j2", title=title, fakta = list(select(e for e in Fakt)))

@app.route("/kalkulacka/")
@login_required
def kalkulacka():
    title = "Kalkulačka"
    cislo1 = request.args.get("cislo1")
    cislo2 = request.args.get("cislo2")
    a = request.args.get("a")
    b = request.args.get("b")
    c = request.args.get("c")
    try:
        scitani = round(float(cislo1) + float(cislo2), 2)
        odcitani = round(float(cislo1) - float(cislo2), 2)
        nasobeni = round(float(cislo1) * float(cislo2), 2)
        deleni = round(float(cislo1) / float(cislo2), 2)
        zbytek_po_deleni = round(float(cislo1) % float(cislo2), 2)
        
        
    except (TypeError, ValueError):
        scitani = ""
        odcitani = ""
        nasobeni = ""
        deleni = ""
        zbytek_po_deleni = ""
        

    try:
        mocnina = round(float(a)**float(b), 2)

    except (TypeError, ValueError):
        mocnina = ""

    try:
        odmocnina_cisla = (float(c))**0.5

    except (TypeError, ValueError):
        odmocnina_cisla = ""

       

    return render_template("kalkulacka.html.j2",
                            title=title,
                            scitani=scitani,
                            odcitani=odcitani,
                            nasobeni=nasobeni,
                            deleni=deleni,
                            zbytek_po_deleni=zbytek_po_deleni,
                            mocnina=mocnina,
                            odmocnina_cisla=odmocnina_cisla
                        )


