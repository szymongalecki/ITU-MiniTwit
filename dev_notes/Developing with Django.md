**Author: Marcus Gunnebo**
### Setting up a project and developing with Django
The first steps when rewriting the flask application to the Django framwork was to set up the project.

1. Install Python and Django: Install the latest version of Python and Django by using the Python package manager, Pip.

2. Create the Project: Create a new directory for the project and navigate to that directory in the command line. Then, run the command `django-admin startproject ITU-MiniTwit` to create the project.

3. Create Apps: Create an app for the project by running the command `python manage.py startapp MiniTwit`. This will create a directory for the app with the necessary files.

4. Create Models: Create models from the original schema in the flask application. This include user, follower and message tables.

5. Set Up a Database: We need a database to store the data for the project. After defining the models we can use the command `python manage.py makemigrations` followed by `python manage.py migrate` to set up a database for the project.

6. Create Views: We create views for the project by writing code in the views.py file. These views are responsible for the logic of a Django project. They are Python functions that take an incoming request and return a response.  

7. Create Forms: Create the URLs for the project by writing code in the urls.py file. The forms are objects that allow users to enter data into a web application. They are responsible for validating the data and passing it onto views for further processing.

8. Create URLs: Create the URLs for the project by writing code in the urls.py file. The URLs are used to route requests to the appropriate view. They also provide a way for users to access the application.

9. Test the Project: Use the command `python manage.py runserver`

Resource: https://docs.djangoproject.com/en/4.2/intro/tutorial01/