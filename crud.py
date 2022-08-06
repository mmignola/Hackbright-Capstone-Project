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


def create_update(project, percent_done, update_pic_path, notes):
    """Create and return a new update."""

    update = Update(
        project = project, 
        percent_done = percent_done,
        update_pic_path = update_pic_path,
        notes = notes
        )

    return update


def get_user_by_email(email):
    """Return a user, given their email."""

    return User.query.filter(User.email == email).first()
    

if __name__ == '__main__':
    from server import app
    connect_to_db(app)