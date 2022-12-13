"""Flask app for Cupcakes"""

from flask import Flask, redirect, render_template, flash, jsonify, request, session
# from flask_debugtoolbar import DebugToolbarExtension

from models import db, connect_db, User

from forms import RegisterForm

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///fnotes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)

app.config['SECRET_KEY'] = "I'LL NEVER TELL!!"
# app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
# debug = DebugToolbarExtension(app)


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

    POST:

    """

    form = RegisterForm()

    print("session===", session)

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data

        user = User.register(username=username, pwd=password)
        user.email = email
        user.first_name = first_name
        user.last_name = last_name
        db.session.add(user)
        db.session.commit()

        session["username"] = user.username

        flash("User successfully created!")
        return redirect("/secret")
    else:
        return render_template("register.html", form=form)


@app.post("/api/cupcakes")
def create_cupcake():
    """
    Create a cupcake with flavor, size, rating and image data from the body of
    the request.
    Return: {cupcake: {id, flavor, size, rating, image}}

    """
    flavor = request.json["flavor"]
    size = request.json["size"]
    rating = request.json["rating"]
    image = request.json["image"] or None

    new_cupcake = Cupcake(
        flavor=flavor,
        size=size,
        rating=rating,
        image=image
    )

    db.session.add(new_cupcake)
    # flask abstracts and returns the new instance
    db.session.commit()

    serialized = new_cupcake.serialize()

    return (jsonify(cupcake=serialized), 201)

@app.patch("/api/cupcakes/<int:cupcake_id>")
def update_cupcake(cupcake_id):
    """update the information on a cupcake

    returns an object with the form
    {cupcake: {id, flavor, size, rating, image}}. """

    cupcake = Cupcake.query.get_or_404(cupcake_id)

    # NOTE: KADEEM SAID WE ARE ON FIRE TODAY 12/12/2022
    #  QUADRUPLE FIRE

    # BOSS way
    cupcake.flavor = request.json.get("flavor", cupcake.flavor)
    cupcake.size = request.json.get("size", cupcake.size)
    cupcake.rating = request.json.get("rating", cupcake.rating)
    cupcake.image = request.json.get("image", cupcake.image)

    # NOOB way
    # flavor = request.json["flavor"] or None
    # size = request.json["size"] or None
    # rating = request.json["rating"] or None
    # image = request.json["image"] or None

    # if flavor:
    #     cupcake.flavor=flavor
    # if size:
    #     cupcake.size=size
    # if rating:
    #     cupcake.rating=rating
    # if image:
    #     cupcake.image=image


    db.session.commit()

    serialized = cupcake.serialize()

    return (jsonify(cupcake=serialized), 200)

@app.delete("/api/cupcakes/<int:cupcake_id>")
def delete_cupcake(cupcake_id):
    """removes cupcake record from table
    returns {deleted: cupcake-id}"""

    cupcake = Cupcake.query.get_or_404(cupcake_id)

    db.session.delete(cupcake)
    db.session.commit()

    return (jsonify(deleted=cupcake_id), 200)

@app.get("/")
def render_homepage():
    """sets up the root page"""

    return render_template("index.html")