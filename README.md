# Craft Tracker

Craft Tracker was my capstone project for the Hackbright Academy software engineering bootcamp. I've always been a big crafter, and wanted to create a way to organize and track progress on all my projects. Craft Tracker allows users to add projects to their database and label them with attributes (craft type, difficulty, etc) that they can organize them by. Users can also create updates for individual projects to track their progress and make notes. 

## Screenshots

### Login page
![Screen Shot 2023-03-05 at 12 57 50 PM (2)](https://user-images.githubusercontent.com/101783138/222985715-da9c6e32-730c-4d46-aaa0-e8c824d721ea.png)

### User Profile
![Screen Shot 2023-03-05 at 12 58 15 PM](https://user-images.githubusercontent.com/101783138/222985751-3b4dc20f-bddb-421c-8441-46b56834486a.png)

### Project details
![Screen Shot 2023-03-05 at 12 58 49 PM](https://user-images.githubusercontent.com/101783138/222985780-8af5ed6e-16d9-4849-b425-ecf55e2daec2.png)

### Update details
![Screen Shot 2023-03-05 at 12 59 19 PM](https://user-images.githubusercontent.com/101783138/222985799-ce9e6c8f-d301-4727-ae94-5658cdbb36b1.png)

### Filter page
![Screen Shot 2023-03-05 at 12 59 51 PM](https://user-images.githubusercontent.com/101783138/222985808-be2b73f6-0ae6-4e96-95a8-2b9faaf4b461.png)

### Filter results
![Screen Shot 2023-03-05 at 1 00 33 PM](https://user-images.githubusercontent.com/101783138/222985817-d3d7a312-fd05-4ae3-8e8e-ba8c006176d4.png)

### Tech Stack
- Front end: HTML, CSS, Jinja
- Back end: Python, Flask, SQLAlchemy

### Setup/Installation

Create and enter virtual environment:
```sh
> virtualenv env
> source env/bin/activate
```

Install requirements:
```sh
> pip3 install -r requirements.txt
```

Run server.py:
```sh
> python3 server.py
```

(Optional) Seed with sample user data
```sh
> python3 seed_database.py
```
Log in with email: user0@test.com and password: test to see sample user!


## Project Pictures 

<img width="317" alt="Screen Shot 2023-03-05 at 1 25 28 PM" src="https://user-images.githubusercontent.com/101783138/222986957-0448181e-9409-444f-bb8a-ec3203b1e3d1.png">

Some squares from the flower granny square blanket! (The updates are a lie, it's only half done.)

<img width="340" alt="Screen Shot 2023-03-05 at 1 25 38 PM" src="https://user-images.githubusercontent.com/101783138/222986966-b2745146-979c-4722-a972-ec1f1d4ce1c8.png"> <img width="475" alt="Screen Shot 2023-03-05 at 1 25 47 PM" src="https://user-images.githubusercontent.com/101783138/222986970-9c5f55d4-5e85-414a-a789-8157cb4cec51.png">

The simple pullover sweater in two different yarns, one finished and one in progress :)


## Future Features
When I completed this project at Hackbright Academy, there were a number of features I would have liked to include if I had had more time. Since then, I have returned to this project to re-do all the CSS and improve the user interface. Other features I may later add include:

 - Ability for users to add photos to their projects and updates
 - Ability for users to view and follow other users/projects so they can keep up with their friends' progress
 - Comment threads on projects and updates
 - Messaging between users
