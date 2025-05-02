import sqlite3
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from helpers import login_required

app = Flask(__name__)
app.secret_key = ''

def get_db():
    conn = sqlite3.connect("mirumin.db", check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

@app.route("/", methods=["GET", "POST"])
#@login_required
def store():

    db = get_db()

    Stickers = db.execute("SELECT * FROM items WHERE categoria = ?;", ("Sticker",))
    Llaveros = db.execute("SELECT * FROM items WHERE categoria = ?;", ("Llavero",))
    Pines = db.execute("SELECT * FROM items WHERE categoria = ?;", ("Pin",))

    return render_template("index.html", stickers=Stickers, llaveros=Llaveros, pines=Pines)


@app.route("/login", methods=["GET", "POST"])
def login():
    """ let user log in """

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if not username:
            flash("must provide username")
            return redirect("/login")

        if not password:
            flash("must provide password")
            return redirect("/login")

        db = get_db()
        cursor = db.execute("SELECT * FROM users WHERE username = ?", (username,))
        rows = cursor.fetchall()

        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], password):
            flash("invalid username and/or password")
            return redirect("/login")

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """ Let user register """

    if request.method == "POST":

        # Get form's values
        username = request.form.get("username")
        password = request.form.get("password")
        confirm_password = request.form.get("confirmation")

        # Check that all fields are filled
        if not username:
            flash("must provide username")
            return redirect("/register")
        if not password:
            flash("must provide password")
            return redirect("/register")

        # Check that password and confirm_password match
        if password != confirm_password:
            flash("password don´t match")
            return redirect("/register")

        # Check that there is no duplicate username
        db = get_db()
        try:
            db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", 
                    (username, generate_password_hash(password)))
            db.commit()
        except ValueError:
            flash("username already exists")
            return redirect("/register")

        return redirect("/login")

    else:
        return render_template("register.html")
    
@app.route("/logout")
def logout():

    # Forget any user_id
    session.clear()

    return redirect("/login")

@app.route("/comisiones", methods=["GET", "POST"])
#@login_required
def comisiones():
    return render_template("comisiones.html")

@app.route("/contactanos", methods=["GET", "POST"])
#@login_required
def contactanos():
    return render_template("contactanos.html")

@app.route("/quienes-somos", methods=["GET", "POST"])
#@login_required
def quienes_somos():
    return render_template("quienes_somos.html")

@app.route("/search", methods=["GET", "POST"])
#@login_required
def search():
    return render_template("search.html")

@app.route("/shopping_cart", methods=["GET", "POST"])
#@login_required
def shopping_cart():
    return render_template("shopping_cart.html")

@app.route("/stickers", methods=["GET", "POST"])
#@login_required
def stickers():
    return render_template("stickers.html")

@app.route("/llaveros", methods=["GET", "POST"])
#@login_required
def llaveros():
    return render_template("llaveros.html")

@app.route("/pins", methods=["GET", "POST"])
#@login_required
def pines():
    return render_template("pins.html")


if __name__ == '__main__':
    app.run(debug=True)