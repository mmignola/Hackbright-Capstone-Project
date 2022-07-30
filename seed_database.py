"""Script to seed database."""

import os
import json
from random import choice, randint
from datetime import datetime

import crud
import model
import server

os.system('dropdb projects')
os.system('createdb projects')

model.connect_to_db(server.app)
model.db.create_all()


fnames = ['John', 'Joe', 'Mary', 'Beth', 'Chris']
lnames = ['Smith', 'Meyer', 'Briggs', 'Green', 'Adams']

craft_types = ['knit', 'crochet', 'sew']
proj_types = ['sweater', 'scarf', 'hat', 'blanket', 'gloves']
difficulties = ['easy', 'intermediate', 'medium', 'hard']
proj_statuses = ['future', 'in progress', 'complete']



# Create 10 users, each user creates 5 projects and an update for each
for n in range(5):
    fname = fnames[n]
    lname = lnames[n]
    email = f"user{n}@test.com"
    password = "test"

    user = crud.create_user(fname, lname, email, password)
    model.db.session.add(user)

    for n in range(5):
        pattern_link = f'link{n}.com'
        craft_type = choice(craft_types)
        proj_type = choice(proj_types)
        difficulty = choice(difficulties)
        free_pattern = randint(0, 1)
        proj_status = choice(proj_statuses)

        project = crud.create_project(user, pattern_link, craft_type, proj_type, difficulty, free_pattern, proj_status)
        model.db.session.add(project)

        percent_done = randint(0,100)
        update_pic_path = "link"
        notes = "this is an update"

        update = crud.create_update(project, percent_done, update_pic_path, notes)
        model.db.session.add(update)

model.db.session.commit()