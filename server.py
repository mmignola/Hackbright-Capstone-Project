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
        flash(f"Login successful.")
        return redirect('/user_profile')


@app.route('/user_profile')
def profile():
    """View user's profile."""

    logged_in_email = session.get('user_email')
    projects = crud.get_users_projects(logged_in_email)
    user = crud.get_user_by_email(logged_in_email)

    return render_template('user_profile.html', projects = projects, user = user)


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

        if "http" not in pattern_link:
            flash("Please try again with a valid link.")
            return redirect('/user_profile')

        project = crud.create_project(user, pattern_link, proj_name, craft_type, proj_type, difficulty, bool(free_pattern), proj_status)
        db.session.add(project)
        db.session.commit()

        flash(f"Created project {proj_name}.")

    return redirect('/user_profile')


@app.route('/user_profile/<proj_id>')
def show_project_details(proj_id):
    """Show details of a given project."""

    project = crud.get_proj_by_id(proj_id)

    return render_template('project_details.html', project = project)


@app.route('/updates/<proj_id>', methods=['POST'])
def create_update(proj_id):
    """Create a new project update."""

    project = crud.get_proj_by_id(proj_id)
    update_name = request.form.get('update_name')
    percent_done = request.form.get('percent_done')
    notes = request.form.get('notes')

    update = crud.create_update(project, update_name, percent_done, notes)
    db.session.add(update)
    db.session.commit()

    flash(f"Created update {update_name}.")

    return redirect('/user_profile')



@app.route('/filter')
def filter_page():
    """Show filter options."""

    return render_template('filter_projects.html')


@app.route('/filter_results', methods=['POST'])
def filter_results():
    """Generates filtered list of user's projects."""

    email = session.get('user_email')
    
    craft_type = request.form.get("craft_type")
    proj_type = request.form.get('proj_type')
    difficulty = request.form.get('difficulty')
    proj_status = request.form.get('proj_status')

    filtered_projects = crud.filter_projects(email, craft_type, proj_type, difficulty, proj_status)
    return render_template('filter_results.html', filtered_projects = filtered_projects)



if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)