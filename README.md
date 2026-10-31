# Hiking Tracker

A Django web application for organizing hiking trips, managing participants, and exploring hiking routes.

## Features

- Browse hiking trips with pagination.
- View route distance and elevation information.
- Manage relationships between hikes and participants.
- Track participant counts and maximum capacity.
- Authentication-protected hiking list.
- Search and filtering functionality.

## Tech Stack

- Python
- Django
- Django ORM
- HTML and Django Templates
- SQL database

## Data Models

- **Hike** — hiking trip details, route, participants, and capacity.
- **Difficulty** — defines the difficulty level associated with a route.
- **Route** — route information, distance, and elevation.
- **Hiker** — hiking participants and their associated trips.

## Installation

```bash
git clone https://github.com/perehinets/hiking-tracker
cd hiking-tracker

python3 -m venv .venv
source .venv/bin/activate

pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Open http://127.0.0.1:8000/ in your browser.


## Purpose

This project demonstrates practical experience with Django models, ORM relationships, class-based views, authentication, pagination, and database queries.
