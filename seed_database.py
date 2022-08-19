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

craft_types = ['Knitting', 'Crocheting', 'Sewing', 'Quilting', 'Embroidery']
proj_types = ['Sweater', 'Scarf', 'Hat', 'Blanket', 'Bag']
difficulties = ['Easy', 'Intermediate', 'Medium', 'Hard']
proj_statuses = ['Future', 'In progress', 'Complete']



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

        update_name = 'update'
        percent_done = randint(0,100)
        # update_pic_path = "link"
        notes = "this is an update"

        update = crud.create_update(project, update_name, percent_done, notes)
        model.db.session.add(update)

# Creates my account and default projects
mads = crud.create_user('Madeleine', 'Mignola', 'madeleine.mignola@gmail.com', 'Catsnad12')
model.db.session.add(mads)

daisy_blanket = crud.create_project(mads, 'https://www.etsy.com/listing/933911629/charity-daisy-square-pattern-groovy?ref=yr_purchases', 'Flower Granny Square Blanket', 'Crocheting', 'Blanket', 'Intermediate', False, 'In progress')
hue_shift = crud.create_project(mads, 'https://www.knitpicks.com/hue-shift-afghan/p/41112D', 'Hue Shift Afghan', 'Knitting', 'Blanket', 'Intermediate', False, 'Complete')
tote_bag = crud.create_project(mads, 'https://www.youtube.com/watch?v=rcZKM9JUEwQ', 'Tote Bag', 'Sewing', 'Bag', 'Beginner', True, 'Complete')

model.db.session.add(daisy_blanket)
model.db.session.add(hue_shift)
model.db.session.add(tote_bag)

model.db.session.commit()