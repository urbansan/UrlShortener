import requests
import json
import pdb
from ..models import random_users
from django.db.utils import IntegrityError

def getUsers(how_many):

    url = 'http://api.randomuser.me/?results=' + str(how_many)

    api_data = requests.get(url)

    user_data = json.loads(api_data.text)

    users = []
    for i in range(len(user_data['results'])):
        users.append({
            'user_name' : user_data['results'][i]['login']['username'],
            'first_name' : user_data['results'][i]['name']['first'].title(),
            'last_name' : user_data['results'][i]['name']['last'].title(),
            'email' : user_data['results'][i]['email'],
            'password' : user_data['results'][i]['login']['password']    
        })

    return users

def purgeUsers():
    to_delete = random_users.objects.all()
    to_delete.delete()

def UserToDB(how_many):

    if how_many == 0:
        return 0

    url = 'http://api.randomuser.me/?results=' + str(min(how_many, 5000))
    api_data = requests.get(url)
    user_data = json.loads(api_data.text)
    nonunique = 0
    users_inserted = 0

    users = []
    for i in range(len(user_data['results'])):
        
        try:
            user_to_save = random_users(
                username = user_data['results'][i]['login']['username'],
                first_name = user_data['results'][i]['name']['first'].title(),
                last_name = user_data['results'][i]['name']['last'].title(),
                email = user_data['results'][i]['email'],
                password = user_data['results'][i]['login']['password']    
            )
        
            user_to_save.save()
            users_inserted += 1
            if users_inserted % 20 == 0:
                print 'added', users_inserted, 'unique users'
        except IntegrityError:
            if nonunique > 100:
                print 'to many nonunique usernames were fetched from randomuser.me:', nonunique
                break
            nonunique += 1
            print 'encountered nonunique user nr', nonunique

    return users_inserted + UserToDB(nonunique)



    # random_users.objects.bulk_create(users)
    
def usersFromDB():
    cursor = random_users.objects.all()
    users = []
    for i in range(len(cursor)):
        users.append({'first_name' : cursor[i].first_name})


    return users