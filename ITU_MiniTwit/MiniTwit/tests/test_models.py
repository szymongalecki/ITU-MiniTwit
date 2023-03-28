from django.test import TestCase
from MiniTwit.models import User, Follower, Message

class UserTestCase(TestCase):
    def setUp(self):
        User.objects.create(username="testuser1", email="testuser1@gmail.com")
        User.objects.create(username="testuser2", email="testuser2@gmail.com")

    def test_email1(self):
        user1 = User.objects.get(username="testuser1")
        self.assertEqual(user1.email, "testuser1@gmail.com")

    def test_email2(self):
        user2 = User.objects.get(username="testuser2")
        self.assertEqual(user2.email, "testuser2@gmail.com")

    def test_name1(self):
        user1 = User.objects.get(email="testuser1@gmail.com")
        self.assertEqual(user1.username, "testuser1")

    def test_name2(self):
        user2 = User.objects.get(email="testuser2@gmail.com")
        self.assertEqual(user2.username, "testuser2")

class FollowerTestCase(TestCase):
    def setUp(self):
        User.objects.create(username="testuser1", email="testuser1@gmail.com")
        User.objects.create(username="testuser2", email="testuser2@gmail.com")

        user1 = User.objects.get(username="testuser1")
        user2 = User.objects.get(username="testuser2")

        Follower.objects.create(who_id=user1, whom_id=user2)
        Follower.objects.create(who_id=user2, whom_id=user1)

    def test_who_id(self):
        user1 = User.objects.get(username="testuser1")
        user2 = User.objects.get(username="testuser2")

        follower1 = Follower.objects.get(who_id=user1)
        follower2 = Follower.objects.get(who_id=user2)

        self.assertEqual(follower1.whom_id, user1)
        self.assertEqual(follower2.whom_id, user2)


    def test_who_id(self):
        user1 = User.objects.get(username="testuser1")
        user2 = User.objects.get(username="testuser2")

        follower1 = Follower.objects.get(whom_id=user1)
        follower2 = Follower.objects.get(whom_id=user2)

        self.assertEqual(follower1.who_id, user2)
        self.assertEqual(follower2.who_id, user1)

class MessageTestCase(TestCase):
    def setUp(self):
        User.objects.create(username="testuser", email="testuser@gmail.com")
        user = User.objects.get(username="testuser")
        Message.objects.create(author_id=user,text="hello twitter")
        
    def test_author_id(self):
        user = User.objects.get(username="testuser")
        message = Message.objects.get(author_id=user)
        self.assertEqual(message.author_id, user)

    def test_text(self):
        user = User.objects.get(username="testuser")
        message = Message.objects.get(author_id=user)
        self.assertEqual(message.text, "hello twitter")

    def test_flagged(self):
        user = User.objects.get(username="testuser")
        message = Message.objects.get(author_id=user)
        self.assertEqual(message.flagged, False)
