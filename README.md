# Academic Notes Organizer
a final project of AP in University of Guilan

## What does it do?
This project is a web application in which you can create new notes and categorize them with your courses.
The main purpose of the project is the local organization of notes and courses you have, but there are some marketplace features that let you see other public courses with the metadata of their public notes, rate, comment and perhaps purchase them in the future.

## How can you run the project?
Well, there are some points about it. You can use the light mode in which you have to clone this `main` branch to your system and run `pip install -r requirements.txt`. I recommend you to use a python virtualenv. Then you can run the project using `python manage.py runserver` and you have the project running (debugging mode) on your `localhost:8000`.

But you can run it using docker and with PostgreSQL if you want. There is a dockerized and postgres-based branch named `production`. It hasn't been merged yet because it's not in the production level. It is in debugging mode and without wsgi. The purpose of the branch is only to show you the way in which project is running in docker. In case you want to use docker, first you should ensure that you have `docker` and `docker compose` installed and ready in your system. Then you can run command `docker compose up --build` in the root of the project. Now you have the project running on your `localhost:8000` again (in debug mode) and you can use it.

The dockerized project has a volume for database data but staticfiles and media is not in professional production mode. So you have to ensure that you are changing the project and docker settings before using it for serious purposes. But it's totally okay if you just want to check it out.


## Refrences
I haven't used anything (even a single chunk) from another project and I have written everything in this project except for `.gitignore`. But I have learned a lot from sources like [geeksforgeeks](https://geeksforgeeks.org), [digitalocean](https://digitalocean.com), [it's foss](https://itsfoss.com), etc.

## TODO
- [x] File management
- [x] markdown preview
- [x] markdown editor
- [x] note list filtering
- [x] Marketplace
- [ ] credit and through model for Marketplace
- [ ] custom 404
- [x] titles for templates
- [x] Switch to PostgreSQL
- [x] Dockerize
- [ ] Switch the project to production mode
