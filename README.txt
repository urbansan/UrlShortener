
Author: Krzysztof Urbańczyk
email: urbansanek@gmail.com

URL Shortener is web application that lets you create an alias for other URLs.

Modules used:
- urlShortener.Backend - custom module used for addapting randomuser.me API and direct radom user generation do the DB
- other modules are available as standard in Python 2.7.6 (this case)

functionalities:
- generate 1-5000 radom users in the DB by ./manage.py create_fake_users [1-5000]
- models.random_users is a secondery key in models.user_urls with cascading deletion. Generating new users will purge the old user set and all URL with it.
- forms are based on models.

Handled exceptions:
- If there are no fake users in DB.
- If there are no more unique IDs for the SHORT_URL_MAX_LEN size of the short_url.
