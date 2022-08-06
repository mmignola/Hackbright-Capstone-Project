"""Server for project organization app."""

from flask import Flask, render_template, request, flash, session, redirect
from model import connect_to_db, db
import crud

from jinja2 import StrictUndefined

app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def homepage():
    """View homepage."""

    return render_template('homepage.html')


@app.route('/users', methods=["POST"])
def create_user():
    """Create a new user."""

    fname = request.form.get("fname")
    lname = request.form.get("lname")
    email = request.form.get("email")
    password = request.form.get("password")

    user = crud.get_user_by_email(email)

    if user:
        flash("An account already exists under that email.")
    else:
        user = crud.create_user(fname, lname, email, password)
        db.session.add(user)
        db.session.commit()
        flash("Account created! Please log in.")

    return redirect('/')


@app.route('/login', methods=['POST'])
def process_login():
    """Process user login."""

    email = request.form.get('email')
    password = request.form.get('password')

    user = crud.get_user_by_email(email)

    if not user or user.password != password:
        flash("The email or password entered was incorrect.")
        return redirect('/')
    else:
        session["user_email"] = user.email
        flash(f"Welcome back, {user.fname}!")
        return redirect('/user_profile')


@app.route('/user_profile')
def profile():
    """View user's profile."""

    return render_template('user_profile.html')


@app.route('/projects', methods=["POST"])
def create_project():
    """Create a new project."""

    logged_in_email = session.get('user_email')

    if logged_in_email is None:
        flash(f"You must be logged in to create a project.")
    else:

        user = crud.get_user_by_email(logged_in_email)
        proj_name = request.form.get('proj_name')
        pattern_link = request.form.get('pattern_link')
        craft_type = request.form.get('craft_type')
        proj_type = request.form.get('proj_type')
        difficulty = request.form.get('difficulty')
        free_pattern = request.form.get('free_pattern')
        proj_status = request.form.get('proj_status')

        project = crud.create_project(user, pattern_link, proj_name, craft_type, proj_type, difficulty, bool(free_pattern), proj_status)
        db.session.add(project)
        db.session.commit()

        flash(f"Created project {proj_name}.")

    return redirect('/user_profile')



if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)