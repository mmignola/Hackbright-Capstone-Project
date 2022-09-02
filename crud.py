"""CRUD operations."""

from model import db, User, Project, Update, connect_to_db


def create_user(fname, lname, email, password):
    """Create and return a new user."""

    user = User(
        fname = fname, 
        lname = lname, 
        email = email, 
        password = password
        )

    return user


def create_project(user, pattern_link, proj_name, craft_type, proj_type, difficulty, free_pattern, proj_status):
    """Create and return a new project."""

    project = Project(
        user = user, 
        pattern_link = pattern_link,
        proj_name = proj_name,
        craft_type = craft_type, 
        proj_type = proj_type,
        difficulty = difficulty,
        free_pattern = free_pattern,
        proj_status = proj_status
        )

    return project


def create_update(project, update_name, percent_done, notes):
    """Create and return a new update."""

    update = Update(
        project = project, 
        update_name = update_name,
        percent_done = percent_done,
        # update_pic_path = update_pic_path,
        notes = notes
        )

    return update


def get_user_by_email(email):
    """Return a user, given their email."""

    return User.query.filter(User.email == email).first()


def get_users_projects(email):
    """Return a list of a given user's projects."""

    user = get_user_by_email(email)

    return Project.query.filter(Project.user == user).all()


def get_proj_by_id(proj_id):
    """Returns a project given its id."""

    return Project.query.get(proj_id)
    

def get_update_by_id(update_id):
    """Returns an update given its id."""

    return Update.query.get(update_id)


def get_updates_by_proj(proj_id):
    """Returns updates for a given project."""

    project = get_proj_by_id(proj_id)

    return Update.query.filter(Update.project == project).all()


def filter_projects(email, craft_type, proj_type, difficulty, proj_status):
    """Returns a list of projects based on selected filters."""

    user = get_user_by_email(email)

    return Project.query.filter(Project.user == user, Project.craft_type.like(craft_type), Project.proj_type.like(proj_type), Project.difficulty.like(difficulty), Project.proj_status.like(proj_status)).all()



if __name__ == '__main__':
    from server import app
    connect_to_db(app)

