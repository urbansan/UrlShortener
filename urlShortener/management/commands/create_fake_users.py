from django.core.management.base import BaseCommand, CommandError
from urlShortener.backend import randomusersAPI

#The class must be named Command, and subclass BaseCommand
class Command(BaseCommand):
    # Show this when the user types help
    help = "My test command"


    def add_arguments(self, parser):
        parser.add_argument('number_of_users', nargs=1, type=int, 
                help = 'give the number of random users you want to generate (max 5000)'
            )

# A command must define handle()
    def handle(self, *args, **options):
        number_of_users = min(options['number_of_users'][0], 5000)
        
        randomusersAPI.purgeUsers()
        randomusersAPI.UserToDB(number_of_users)

        string_to_return = 'Added / replaced ' + str(number_of_users) + ' random users'
        self.stdout.write(string_to_return)