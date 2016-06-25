import requests
import json
import pdb
from ..models import random_users

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

    url = 'http://api.randomuser.me/?results=' + str(how_many)
    api_data = requests.get(url)
    user_data = json.loads(api_data.text)

    users = []
    for i in range(len(user_data['results'])):
        users.append(
            random_users(
                user_name = user_data['results'][i]['login']['username'],
                first_name = user_data['results'][i]['name']['first'].title(),
                last_name = user_data['results'][i]['name']['last'].title(),
                email = user_data['results'][i]['email'],
                password = user_data['results'][i]['login']['password']    
            )
        )

    random_users.objects.bulk_create(users)
    
def usersFromDB():
    cursor = random_users.objects.all()
    users = []
    for i in range(len(cursor)):
        users.append({'first_name' : cursor[i].first_name})


    return users