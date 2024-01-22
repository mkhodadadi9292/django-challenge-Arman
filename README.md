# django-challenge


The volleyball Federation decided to use an online selling platform for the next season, and our company has been chosen for implementing that.

# Requirements

Our system should have REST APIs for the following tasks:

- User signup and login
- Adding a new stadium
- Defining matches
- Defining the place of seats for each match
- Buying seats of a match (There is no need for using a payment gateway)

# Implementation details

We don't need a GUI for this system. You can use the Django admin.
Try to write your code as **reusable** and **readable** as possible. Also, don't forget to **document your code** and clear the reasons for all your decisions in the code.
Using API documentation tools is a plus.
Don't forget that many people trying to buy tickets for a match. So try to implement your code in a way that could handle the load. If your solution is not sample enough for implementing fast, you can just describe it in your documents.

Please fork this repository and add your code to that. Don't forget that your commits are so important. So be sure that you're committing your code often with a proper commit message.

## All dependencies
- Redis has been applied as message broker and cache system
- Celery has been applied as  task queue
- MySQL or Sqlite has been applied as database (default database is `MySQL`)
## Installation
- activate virtualenv
- install all python requirments by `pip install -r requirements.txt`
- migrate database through `python manage.py migrate`
**check the following fields** in settings.py
1) `CELERY_BROKER_URL`
2) `CELERY_RESULT_BACKEND`
3) `CELERY_TASK_SERIALIZER`
4) `CELERY_RESULT_SERIALIZER`
5) `CELERY_ACCEPT_CONTENT`
- Change the database backend in setting.py
- Ensure that the database and redis are installed and available.
- Run these commands in separate shells in the same python virtualenv.
1) `celery -A position worker -l info -P gevent`
2) in development mode (`python manage.py runserver`), but you are able to use gunicorne or uwsgi

