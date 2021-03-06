
Author: Krzysztof Urbańczyk
email: urbansanek@gmail.com

URL Shortener is web application that lets you create an alias for other URLs.
Heroku deployable: https://ten-clouds-interview.herokuapp.com/
bitbucket repo: https://UrbanVirt@bitbucket.org/MakeMeRandom/10clouds_interview.git

Modules used:
- URLShortener.Backend - custom module used for addapting randomuser.me API and direct radom user generation do the DB
- other modules are available as standard in Python 2.7.11 (this case)

functionalities:
- generate 1-5000 radom users in the DB by ./manage.py create_fake_users [1-5000]
- models.RandomUsers is a secondery key in models.UserURLS with cascading deletion. Generating new users will purge the old user set and all URL with it.
- forms are based on models.
- the length of the short URL is defined in URLShortener.views.py: SHORT_URL_MAX_LEN

Handled exceptions:
- If there are no fake users in DB.
- If there are no more unique IDs for the SHORT_URL_MAX_LEN size of the short_url.

local startup (terminal):
1. virtualenv venv in root dir of the project.
2. source venv/bin/activate
3. pip install -r requirements.txt 
4. ./manage.py migrate
5. ./manage.py create_fake_users [1-5000]
6. ./manage.py createsuperuser
7. ./manage.py runserver

