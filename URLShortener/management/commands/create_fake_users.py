from django.core.management.base import BaseCommand, CommandError
import requests
from URLShortener.models import RandomUsers
from django.db.utils import IntegrityError
import sys

class Command(BaseCommand):
    help = "My test command"

    def add_arguments(self, parser):
        parser.add_argument('number_of_users', type=int, 
                help = 'give the number of random users you want to generate (max 5000)'
        )

    def handle(self, *args, **options):
        number_of_users = options['number_of_users']
        
        self.purge_users()
        real_number_of_users = self.users_to_db(number_of_users)

        string_to_return = 'Added / replaced ' + str(real_number_of_users) + ' random users'
        self.stdout.write(string_to_return)

    def get_users(self, how_many):
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

    def users_to_db(self, how_many):
        if how_many == 0:
            return 0

        nonunique = 0
        users_inserted = 0

        users = self.get_users(how_many)
        for user in users:
            try:
                user_to_save = RandomUsers.objects.create_user(
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
        return users_inserted + self.users_to_db(nonunique)
        
    def show_users_names(self):
        cursor = RandomUsers.objects.all()
        users = []

        for i in range(len(cursor)):
            users.append({'first_name' : cursor[i].first_name})
            
        return users

    def purge_users(self):
        to_delete = RandomUsers.objects.all()
        to_delete.delete()