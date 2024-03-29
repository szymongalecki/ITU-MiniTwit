# Django Migration Scripts
## Introduction

When developing a Django project, it's common to make changes to your models over time, such as adding or modifying fields. These changes need to be reflected in your database schema, and Django provides a migration framework to help manage this process.

Migration scripts are Python files that describe changes to the database schema. By running these scripts, Django can automatically update your database schema to match your models.

## Getting Started

To start using migration scripts in your Django project, follow these steps:

1. Make changes to your Django models, such as adding a new field or changing the name of a field.
2. Run the **python manage.py makemigrations** command. This analyzes your models and generates new migration files that describe the changes to be made to the database schema. After running this command, you will see a new migration file created in your app/migrations directory. This file will contain Python code that describes the changes to be made to your database schema.
3. Review the generated migration file and make any necessary modifications to it. In some cases, the generated file may not be exactly what you need, so you may need to make changes to it manually.
4. Run the **python manage.py migrate MiniTwit <migration_script>** command to apply the new migration to your database schema. Replace **<migration_script>** with the name of the script you need to run. 
5. Verify that the migration was applied correctly by checking your database schema.

By following these steps, you can implement migration scripts in your Django project to keep your database schema up-to-date with your models.

## Running Migrations

The migrations folder in a Django project contains files that describe changes to be made to the database schema. Each migration file represents a set of changes to the database schema that can be applied using the **migrate** command.

Here are the migration files for our MiniTwit app:

* **0001_user_model.py**: This file generates the User table in the database.
* **0002_message_model.py**: This file generates the Message and Follow tables.
* **0003_migrateusers.py**: This file migrates all the users from the old database to the new one.
* **0004_migratemessages.py**: This file migrates all the messages and follow data from the old database to the new one.

It's important to note that **0003_migrateusers.py** and **0004_migratemessages.py** need to be run in separate runs. This is because we need to migrate all the users before creating the messages and followers tables, as the later tables use the user's IDs as foreign keys.

To run the migrations, we can use the **python manage.py migrate** command followed by the app label and the migration file name. For example, to run the **0003_migrateusers.py migration**, we would use the following command:

```python manage.py migrate MiniTwit 0003_migrateusers.py```

By running the migrations in the correct order, we can ensure that the database schema is updated correctly and all necessary data is migrated.

## Steps to restore the Data with an existing DB
```
docker exec -it <appContainerId> sh
kill 1
docker start <appContainerId>
docker exec -it <appContainerId>
rm MiniTwit/migrations/0003_migrateusers.py MiniTwit/migrations/0004_migratemessages.py
python manager.py migrate --fake
exit 
docker cp MiniTwit/migrations/0003_migrateusers.py <appContainerId>:/usr/src/MiniTwit/migrations
docker cp MiniTwit/migrations/0004_migratemessages.py <appContainerId>:/usr/src/MiniTwit/migrations
docker exec -it <appContainerId>
python manager.py magrate
```
## How to copy the data
On the receiving side (the side that is listening on the port), run the following command:
```
nc -l [port] > [filename]
```
This will start listening on the specified port and redirect the incoming data to the specified filename.

On the sending side, run the following command:
```
nc [ip address] [port] < [filename]
```
This will send the contents of the specified file to the specified IP address and port using nc.

Make sure to replace [port], [ip address], and [filename] with the appropriate values.

Note that this method is not encrypted, so if security is a concern, you should use a different method that provides encryption, such as scp. Also, this method does not compress the files, so it may be slower for large files or over slow network connections.