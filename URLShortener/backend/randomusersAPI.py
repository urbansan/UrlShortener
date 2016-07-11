import requests
from ..models import RandomUsers
from django.db.utils import IntegrityError
import sys
import pdb

def get_users(how_many):

    url = 'http://api.randomuser.me/?results=' + str(how_many)
    api_data = requests.get(url)
    user_data = api_data.json()

    users = []
    for user_nr in user_data['results']:
        users.append({
            'username' : user_nr['login']['username'],
            'first_name' : user_nr['name']['first'].title(),
            'last_name' : user_nr['name']['last'].title(),
            'email' : user_nr['email'],
            'password' : user_nr['login']['password']    
        })
    return users

def users_to_db(how_many):

    if how_many == 0:
        return 0

    nonunique = 0
    users_inserted = 0

    users = get_users(how_many)
    for user in users:
        try:
            user_to_save = RandomUsers(
                username = user['username'],
                first_name = user['first_name'],
                last_name = user['last_name'],
                email = user['email'],
                password = user['password']
            )
        
            user_to_save.save()
            users_inserted += 1
            if users_inserted % 20 == 0:
                # print '\radded', users_inserted, 'unique users'
                sys.stdout.write('\radded %d unique users, encoutered %d nonuniques' % (users_inserted, nonunique))
                sys.stdout.flush()
        except IntegrityError:
            if nonunique > 100:
                print '\nto many nonunique usernames were fetched from randomuser.me:', nonunique
                break
            nonunique += 1

    sys.stdout.write('\r')
    sys.stdout.flush()
    return users_inserted + users_to_db(nonunique)
    
def show_users_names():
    cursor = RandomUsers.objects.all()
    users = []

    for i in range(len(cursor)):
        users.append({'first_name' : cursor[i].first_name})
        
    return users

def purge_users():
    to_delete = RandomUsers.objects.all()
    to_delete.delete()