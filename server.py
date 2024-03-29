"""Server for project organization app."""

from flask import Flask, render_template, request, flash, session, redirect
from crafttracker.model import connect_to_db, db
import crafttracker.crud as crud

from jinja2 import StrictUndefined

app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def homepage():
    """View homepage."""

    logged_in_email = session.get('user_email')

    if logged_in_email:
        return redirect('/user_profile')

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

    if logged_in_email is None:
        flash("You must be logged in to view a profile.")
        return redirect('/')
    else:
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

    logged_in_email = session.get('user_email')
    project = crud.get_proj_by_id(proj_id)
    updates = crud.get_updates_by_proj(proj_id)

    if logged_in_email is None:
        flash("You must be logged in to view projects.")
        return redirect('/')

    elif logged_in_email != project.user.email:
        flash("You can not view another user's project.")
        return redirect('/user_profile')

    else:
        return render_template('project_details.html', project = project, updates = updates)


@app.route('/user_profile/<proj_id>/delete')
def delete_project(proj_id):
    """Delete a project."""

    logged_in_email = session.get('user_email')
    project = crud.get_proj_by_id(proj_id)
    proj_name = project.proj_name
    updates = crud.get_updates_by_proj(proj_id)
    
    if logged_in_email is None:
        flash(f"You must be logged in to delete a project.")
        return redirect('/')

    elif logged_in_email != project.user.email:
        flash("You can not delete another user's project.")
        return redirect('/user_profile')

    else:
        db.session.delete(project)
        db.session.commit()

        for update in updates:
            db.session.delete(update)
            db.session.commit()

        flash(f"Deleted project {proj_name}.")
        return redirect('/user_profile')


@app.route('/user_profile/<proj_id>/edit')
def edit_project_form(proj_id):
    """View project edit form."""
    
    logged_in_email = session.get('user_email')
    project = crud.get_proj_by_id(proj_id)

    if logged_in_email is None:
        flash(f"You must be logged in to edit a project.")
        return redirect('/')

    elif logged_in_email != project.user.email:
        flash("You can not edit another user's project.")
        return redirect('/user_profile')

    else:
        return render_template('edit_project.html', project = project)


@app.route('/user_profile/<proj_id>/execute_edits', methods=["POST"])
def edit_project(proj_id):
    """Update the details of a project."""

    project = crud.get_proj_by_id(proj_id)

    project.proj_name = request.form.get('proj_name')
    project.pattern_link = request.form.get('pattern_link')
    project.craft_type = request.form.get('craft_type')
    project.proj_type = request.form.get('proj_type')
    project.difficulty = request.form.get('difficulty')
    project.free_pattern = bool(request.form.get('free_pattern'))
    project.proj_status = request.form.get('proj_status') 

    if "http" not in project.pattern_link:
            flash("Please try again with a valid link.")
            return redirect(f'/user_profile/{project.proj_id}/edit')

    db.session.commit()

    flash(f"Edited project {project.proj_name}.")

    return redirect(f"/user_profile/{proj_id}")


@app.route('/updates/<proj_id>', methods=['POST'])
def create_update(proj_id):
    """Create a new project update."""

    logged_in_email = session.get('user_email')

    if logged_in_email is None:
        flash(f"You must be logged in to create an update.")
        return redirect('/')

    else:
        project = crud.get_proj_by_id(proj_id)
        update_name = request.form.get('update_name')
        percent_done = int(request.form.get('percent_done'))
        notes = request.form.get('notes')

        update = crud.create_update(project, update_name, percent_done, notes)
        db.session.add(update)
        db.session.commit()

        flash(f"Created update {update_name}.")
        return redirect(f'/user_profile/{proj_id}')


@app.route('/update/<update_id>')
def show_update_details(update_id):
    """Show details of a project update."""

    logged_in_email = session.get('user_email')

    update = crud.get_update_by_id(update_id)

    if logged_in_email is None:
        flash("You must be logged in to view project updates.")
        return redirect('/')

    elif logged_in_email != update.project.user.email:
        flash("You can not view another user's update.")
        return redirect('/user_profile')

    else:
        return render_template('update_details.html', update = update)


@app.route('/update/<update_id>/delete')
def delete_update(update_id):
    """Delete a project update."""

    logged_in_email = session.get('user_email')
    update = crud.get_update_by_id(update_id)
    update_name = update.update_name
    proj_id = update.project.proj_id

    if logged_in_email is None:
        flash(f"You must be logged in to delete an update.")
        return redirect('/')

    elif logged_in_email != update.project.user.email:
        flash("You can not delete another user's update.")
        return redirect('/user_profile')

    else:
        db.session.delete(update)
        db.session.commit()

        flash(f"Deleted update {update_name}.")
        return redirect(f'/user_profile/{proj_id}')


@app.route('/update/<update_id>/edit')
def edit_udpate_form(update_id):
    """View update edit form."""

    update = crud.get_update_by_id(update_id)
    logged_in_email = session.get('user_email')

    if logged_in_email is None:
        flash(f"You must be logged in to edit an update.")
        return redirect('/')

    elif logged_in_email != update.project.user.email:
        flash("You can not edit another user's update.")
        return redirect('/user_profile')

    else:
        return render_template('edit_update.html', update = update)


@app.route('/update/<update_id>/execute_edits', methods=["POST"])
def edit_update(update_id):
    """Update the details of a project update."""

    update = crud.get_update_by_id(update_id)

    update.update_name = request.form.get('update_name')
    update.percent_done = int(request.form.get('percent_done'))
    update.notes = request.form.get('notes')

    db.session.commit()

    flash(f"Edited update {update.update_name}.")

    return redirect(f"/update/{update.update_id}")


@app.route('/filter')
def filter_page():
    """Show filter options."""
    
    logged_in_email = session.get('user_email')

    if logged_in_email is None:
        flash("You must be logged in to filter projects.")
        return redirect('/')
    else:
        return render_template('filter_projects.html')


@app.route('/filter_results', methods=['POST'])
def filter_results():
    """Generates filtered list of user's projects."""

    email = session.get('user_email')
    
    craft_type = request.form.get("craft_type")
    proj_type = request.form.get('proj_type')
    difficulty = request.form.get('difficulty')
    proj_status = request.form.get('proj_status')

    if email is None:
        flash("You must be logged in to view filter results.")
        return redirect('/')
    else:
        filtered_projects = crud.filter_projects(email, craft_type, proj_type, difficulty, proj_status)
        return render_template('filter_results.html', filtered_projects = filtered_projects)


@app.route('/log_out')
def log_out():
    """Log the user out."""

    session['user_email'] = None

    return redirect('/')


if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)