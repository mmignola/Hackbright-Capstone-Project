"""Models for project organization app."""

from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    """A user."""

    __tablename__ = "users"

    user_id = db.Column(db.Integer, autoincrement = True, primary_key = True)
    fname = db.Column(db.String)
    lname = db.Column(db.String)
    email = db.Column(db.String, unique = True)
    password = db.Column(db.String)

    def __repr__(self):
        """Show info about user."""

        return f"<User user_id={self.user_id} fname={self.fname} lname={self.lname} email={self.email} password={self.password}>"

    
class Project(db.Model):
    """A project."""

    __tablename__ = "projects"

    proj_id = db.Column(db.Integer, autoincrement = True, primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"))
    proj_name = db.Column(db.String)
    pattern_link = db.Column(db.String)
    craft_type = db.Column(db.String)
    proj_type = db.Column(db.String)
    difficulty = db.Column(db.String)
    free_pattern = db.Column(db.Boolean)
    proj_status = db.Column(db.String)

    user = db.relationship("User", backref="projects")

    def __repr__(self):
        """Show info about project."""

        return f"<Project proj_id={self.proj_id} user_id={self.user_id} proj_name={self.proj_name} pattern_link={self.pattern_link} craft_type={self.craft_type} proj_type={self.proj_type}>"


class Update(db.Model):
    """A project update."""

    __tablename__ = "updates"

    update_id = db.Column(db.Integer, autoincrement = True, primary_key = True)
    proj_id = db.Column(db.Integer, db.ForeignKey("projects.proj_id"))
    percent_done = db.Column(db.Integer)
    update_pic_path = db.Column(db.String)
    notes = db.Column(db.Text)

    project = db.relationship("Project", backref="updates")

    def __repr__(self):
        """Show info about project updates."""

        return f"<Update update_id={self.update_id} proj_id={self.proj_id} percent_done={self.percent_done} notes={self.notes}>"


def connect_to_db(flask_app, db_uri="postgresql:///projects", echo=True):
    flask_app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
    flask_app.config["SQLALCHEMY_ECHO"] = echo
    flask_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.app = flask_app
    db.init_app(flask_app)

    print("Connected to the db!")


if __name__ == "__main__":
    from server import app

    # Call connect_to_db(app, echo=False) if your program output gets
    # too annoying; this will tell SQLAlchemy not to print out every
    # query it executes.

    connect_to_db(app)
