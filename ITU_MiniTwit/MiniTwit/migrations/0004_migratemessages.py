import datetime
from django.utils import timezone
from django.db import connections, migrations

def copy_messages(apps, schema_editor):
    # Get a connection to the old database
    old_db = connections['old_db']

    # Execute a SELECT statement to retrieve the data from the old table
    with old_db.cursor() as cursor:
        cursor.execute("SELECT * FROM message limit 100")

        # Iterate over the rows and insert them into the new table
        for row in cursor.fetchall():
            
            
            newMessage = apps.get_model('MiniTwit', 'message')
            new_message = newMessage()
            author = apps.get_model('MiniTwit', 'User').objects.get(id=row[1])
            new_message.author = author
            new_message.text = row[2]
            pub_date = datetime.datetime.fromtimestamp(row[3])
            pub_date = timezone.make_aware(pub_date, timezone.get_default_timezone())
            new_message.pub_date = pub_date
            new_message.flagged = row[4]

            new_message.save()

def copy_followers(apps, schema_editor):
    # Get a connection to the old database
    old_db = connections['old_db']

    # Execute a SELECT statement to retrieve the data from the old table
    with old_db.cursor() as cursor:
        cursor.execute("SELECT * FROM follower limit 100")

        # Iterate over the rows and insert them into the new table
        for row in cursor.fetchall():

            newFollower = apps.get_model('MiniTwit', 'follower')
            new_follower = newFollower()
        
            new_follower.who = apps.get_model('MiniTwit', 'User').objects.get(id=row[0])
            new_follower.whom = apps.get_model('MiniTwit', 'User').objects.get(id=row[1])

            new_follower.save()


class Migration(migrations.Migration):

    dependencies = [
        ('MiniTwit', '0003_migrateusers'),
    ]

    operations = [
        migrations.RunPython(copy_messages),
        migrations.RunPython(copy_followers),
    ]
