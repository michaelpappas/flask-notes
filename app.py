"""Flask app for Cupcakes"""

from flask import Flask, redirect, render_template, flash, session
from models import db, connect_db, User
from forms import RegisterForm, LoginForm, CSRFProtectForm

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///fnotes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)

app.config['SECRET_KEY'] = "I'LL NEVER TELL!!"


@app.get("/")
def get_homepage():
    """
    Redirect to /register
    """
    return redirect("/register")


@app.route("/register", methods=["GET", "POST"])
def register():
    """
    GET:
    Show a form that when submitted will register/create a user.
    This form should accept a username, password, email, first_name,
    and last_name.

    POST: Flash message and automatically log the user in and redirect to their
          profile page.

    """

    form = RegisterForm()

    print("session===", session)

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data

        # todo move
        user = User.register(
            username=username,
            pwd=password,
            email=user.email,
            first_name=user,
            last_name=last_name
        )

        db.session.add(user)
        db.session.commit()

        session["username"] = user.username

        flash("User successfully created!")
        return redirect(f"/users/{user.username}")
    else:
        return render_template("register.html", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    """
    Show a form that when submitted will login a user. This form should accept a username and a password.

    """
    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.login(username,password)

        if user:
            session["username"] = user.username
            return redirect(f"/users/{user.username}")
        else:
            form.username.errors = ["Bad name/password"]

    return render_template("login.html", form = form)


@app.get("/users/<username>")
def user_detail(username):
    """ Displays a template that shows information about that user """

    user = User.query.get_or_404(username)
    logout_form = CSRFProtectForm()

    if "username" in session:
        return render_template("user_detail.html", user=user, logout_form=logout_form)
    else:
        flash("You need to log in!")
        return redirect("/")


@app.post("/logout")
def logout():
    """ Clears any information from the session and redirect to / """

    form = CSRFProtectForm()

    if form.validate_on_submit():
        session.pop("username", None)

    return redirect("/")
