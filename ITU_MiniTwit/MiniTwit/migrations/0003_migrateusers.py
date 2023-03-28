import django.contrib.auth.models
from django.db import connections, migrations
import django.utils.timezone


def copy_users(apps, schema_editor):
    # Get a connection to the old database
    old_db = connections['old_db']

    # Execute a SELECT statement to retrieve the data from the old table
    with old_db.cursor() as cursor:
        cursor.execute("SELECT * FROM user")

        # Iterate over the rows and insert them into the new table
        for row in cursor.fetchall():
            newUser = apps.get_model('MiniTwit', 'User')

            # Copy the relevant data from the old table to the new table
            new_user = newUser()

            # new_user.id = row[0]
            new_user.password = row[3]
            new_user.email = row[2]
            new_user.username = row[1]
            new_user.first_name = row[1].split()[0]  # first name is the first word in the username
            if len(row[1].split()) > 1:
                new_user.last_name = row[1].split()[1]
            else:
                new_user.last_name = ''
            # last name is the second word in the username    
            new_user.is_superuser = False
            new_user.is_staff = False
            new_user.is_active = True
            new_user.date_joined = django.utils.timezone.now()
            new_user.last_login = django.utils.timezone.now()

            new_user.save()

class Migration(migrations.Migration):

    dependencies = [
        ('MiniTwit', '0002_message_model'),
    ]

    operations = [
        migrations.RunPython(copy_users),
    ]
