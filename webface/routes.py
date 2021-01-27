from . import app
from flask import render_template, request, Flask, session, redirect, url_for
from datetime import timedelta
from pony.orm import db_session
from random import choice
import functools

app.secret_key = "hello"
app.permanent_session_lifetime = timedelta(minutes=5)


def login_required(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if "user" in session:
           return func(*args, **kwargs)
        else: 
            return redirect(url_for("login"))

    return wrapper

@app.route("/login/", methods=["POST", "GET"])
def login():
    title = "Login"
    if request.method == "POST":
        session.permanent = True
        user  =request.form["nm"]
        session["user"] = user
        return redirect(url_for("uvod"))
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


@app.route("/citaty/")
@login_required
def citaty():
    title = "Citáty"
    return render_template("citaty.html.j2", title=title)

@app.route("/fakta/")
@login_required
def fakta():
    title = "Fakta"
    return render_template("fakta.html.j2", title=title)

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


