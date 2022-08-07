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
        proj_name = f'project {n}'
        pattern_link = f'link{n}.com'
        craft_type = choice(craft_types)
        proj_type = choice(proj_types)
        difficulty = choice(difficulties)
        free_pattern = randint(0, 1)
        proj_status = choice(proj_statuses)

        project = crud.create_project(user, pattern_link, proj_name, craft_type, proj_type, difficulty, free_pattern, proj_status)
        model.db.session.add(project)

        percent_done = randint(0,100)
        update_pic_path = "link"
        notes = "this is an update"

        update = crud.create_update(project, percent_done, update_pic_path, notes)
        model.db.session.add(update)

# Creates my account and default projects
mads = crud.create_user('Madeleine', 'Mignola', 'madeleine.mignola@gmail.com', 'Catsnad12')
model.db.session.add(mads)

daisy_blanket = crud.create_project(mads, 'https://www.etsy.com/listing/933911629/charity-daisy-square-pattern-groovy?ref=yr_purchases', 'Flower Granny Square Blanket', 'crochet', 'blanket', 'intermediate', False, 'in progress')
hue_shift = crud.create_project(mads, 'https://www.knitpicks.com/hue-shift-afghan/p/41112D', 'Hue Shift Afghan', 'knit', 'blanket', 'intermediate', False, 'complete')
model.db.session.add(daisy_blanket, hue_shift)



model.db.session.commit()