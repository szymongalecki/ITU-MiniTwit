**Author: Marcus Gunnebo**
### Django Unit Tests
We chose Django Unit Tests in our project because they help us ensure our app works correctly. Unit Tests provide an automated way to check our code, so we can be sure our app is working properly. It also makes sense to use Django built in functionality when we use Django as framework.

### Coverage
1. Models - These tests cover the fields of the User, Follower, and Message models in the MiniTwit application. They test that the email and username fields are correct for the User model, as well as the who_id and whom_id fields for the Follower model, and the author_id and text fields in the Message model. We don't have any custom functions to test in the models.
2. Forms - This set of tests covers the CustomUserCreationForm and the CustomUserChangeForm, which are forms used to create and update users in the Django application. The tests check that the form correctly validates the data that is passed to it, ensuring that all required fields are present and that the passwords match.
3. Views - This set of tests covers the functionality of the the different views on the MiniTwit application. Specifically, it tests the response when the page is loaded, the number of messages that should be displayed, the content of a message, and the functionality of the follow and unfollow buttons.

### How to run the tests
1. Change directory to `/ITU_MiniTwit`
2. Run `python manage.py test MiniTwit/tests`