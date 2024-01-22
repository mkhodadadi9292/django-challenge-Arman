# django-challenge

The volleyball Federation decided to use an online selling platform for the next season, and our company has been chosen
for implementing that.

# Requirements

Our system should have REST APIs for the following tasks:

- User signup and login
- Adding a new stadium
- Defining matches
- Defining the place of seats for each match
- Buying seats of a match (There is no need for using a payment gateway)

# Implementation details

We don't need a GUI for this system. You can use the Django admin.
Try to write your code as **reusable** and **readable** as possible. Also, don't forget to **document your code** and
clear the reasons for all your decisions in the code.
Using API documentation tools is a plus.
Don't forget that many people trying to buy tickets for a match. So try to implement your code in a way that could
handle the load. If your solution is not sample enough for implementing fast, you can just describe it in your
documents.

Please fork this repository and add your code to that. Don't forget that your commits are so important. So be sure that
you're committing your code often with a proper commit message.

## All dependencies

- Redis has been applied as message broker and cache system
- Celery has been applied as task queue
- MySQL or Sqlite has been applied as database (default database is `MySQL`)

## ---------------------------------------

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

## Admin Panel

- All models are available in the admin panel.

## Endpoints

- User can signup and login by JWT token.(joser library is used in order to handle authentication) these endpoints
  starts with
  `/auth/` (swagger is available but it might not show some endpoints)
- Admin can add new stadiums, define new match and set tickets (according to Price and status)
- I also define Wallet to withdraw or charge money for registered users.
- Permission are applied to each endpoints. (ordinary users can access `/api/ticket/{ticket_id}/canceled`,
  `/api/ticket/{ticket_id}/reserve`, `/api/wallet/{wallet_id}/charge`, `/api/wallet/{wallet_id}/purchase`)

- Following list of endpoints are available for management of Ticket
  `{
  "ticket": "http://127.0.0.1:8000/api/ticket/",
  "stadium": "http://127.0.0.1:8000/api/stadium/",
  "seat": "http://127.0.0.1:8000/api/seat/",
  "match": "http://127.0.0.1:8000/api/match/",
  "wallet":"http://127.0.0.1:8000/api/wallet/",
  "price": "http://127.0.0.1:8000/api/price/",
  }`
- Transaction table is available in order to see the details.

## Important Note:

- ERD diagram is available beside the current file.
- There is prepared command to populate database with mock data.(this data is not sensible necessarily) you can run
  through `python manage.py generate_mock_data `
- all important endpoints like reservation and purchase are done through transaction mode.
- at the `\reserve` initiate_conversion(ticket.id) method is deactivated.
- I think there are some other ways to handle reserved tickets without purchasing (we can call it orphan ticket) like
  crone jobs, or event handlers builtin PostgreSQL or MySQL.
- If have much more time I would implement throttling (In order to secure endpoints) , pagination and design useful
  endpoints