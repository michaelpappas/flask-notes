"""Flask app for Cupcakes"""

from flask import Flask, redirect, render_template, flash, session
from models import db, connect_db, User, Note
from forms import RegisterForm, LoginForm, CSRFProtectForm, NoteForm, EditNoteForm

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

        user = User.register(
            username=username,
            pwd=password,
            email=email,
            first_name=first_name,
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

    # We will keep it dry with "Hooks"
    if  "username" not in session or session["username"] != username:
        return redirect("/")

    user = User.query.get_or_404(username)

    csrf_form = CSRFProtectForm()

    if "username" in session:
        return render_template("user_detail.html",
                                user=user,
                                # logout_form=logout_form,
                                csrf_form=csrf_form
                                )
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

@app.post("/users/<username>/delete")
def delete_user(username):
    """ Delete user and redirect to /"""

    # Fail fast why query if not logged in, dont bother to do it

    if  "username" not in session or session["username"] != username:
        return redirect("/")

    user = User.query.get_or_404(username)

    form = CSRFProtectForm()

    if form.validate_on_submit():

        Note.query.filter_by(username=username).delete()

        db.session.delete(user)
        db.session.commit()

        session.pop("username", None)

        flash(f"{username} has been deleted!")
        return redirect("/")


# ================================NOTES=====================================

@app.route("/users/<username>/notes/add", methods=["POST", "GET"])
def add_note(username):
    """ Display a form to add notes. """

    if  "username" not in session or session["username"] != username:
        return redirect("/")

    form = NoteForm()

    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data

        new_note = Note(title=title, content=content, owner=username)
        db.session.add(new_note)
        db.session.commit()

        flash("New note has been added!")
        return redirect(f"/users/{username}")
    else:
        return render_template("add_note.html", form=form)

@app.route("/notes/<int:note_id>/update", methods=["POST", "GET"])
def update_note(note_id):
    """
    GET:
    Show a form that when submitted will edit the note

    POST: Flash message and redirect to profile page.

    """

    note = Note.query.get_or_404(note_id)
    username = note.owner

    if  "username" not in session or session["username"] != username:
        return redirect("/")
    breakpoint()
    form = EditNoteForm(obj=note)

    if form.validate_on_submit():
        note.title = form.data.get("title", note.title)
        note.content = form.data.get("content", note.content)

        db.session.commit()

        flash("New note has been added!")

        return redirect(f"/users/{note.owner}")

    else:
        return render_template("edit_note.html", form = form)

@app.post("/notes/<int:note_id>/delete")
def delete_note(note_id):
    """ Delete note and redirect to profile page"""

    note = Note.query.get_or_404(note_id)
    username = note.owner
    form = CSRFProtectForm()

    if form.validate_on_submit():

        db.session.delete(note)
        db.session.commit()

        flash("Note has been deleted!")
        return redirect(f"/users/{username}")
        # or note.username but not appropriate deletes it from db but it
        # still exists within this function
        # instance in this context still exists



