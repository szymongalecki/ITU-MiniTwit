from django.test import TestCase
from MiniTwit.models import User, Follower, Message
from django.utils import timezone

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

        Follower.objects.create(who=user1, whom=user2)
        Follower.objects.create(who=user2, whom=user1)

    def test_who(self):
        user1 = User.objects.get(username="testuser1")
        user2 = User.objects.get(username="testuser2")

        follower1 = Follower.objects.get(who=user1)
        follower2 = Follower.objects.get(who=user2)

        self.assertEqual(follower1.whom, user1)
        self.assertEqual(follower2.whom, user2)


    def test_who(self):
        user1 = User.objects.get(username="testuser1")
        user2 = User.objects.get(username="testuser2")

        follower1 = Follower.objects.get(whom=user1)
        follower2 = Follower.objects.get(whom=user2)

        self.assertEqual(follower1.who, user2)
        self.assertEqual(follower2.who, user1)

class MessageTestCase(TestCase):
    def setUp(self):
        User.objects.create(username="testuser", email="testuser@gmail.com")
        user = User.objects.get(username="testuser")
        Message.objects.create(author=user,text="hello twitter",pub_date=timezone.now())
        
    def test_author(self):
        user = User.objects.get(username="testuser")
        message = Message.objects.get(author=user)
        self.assertEqual(message.author, user)

    def test_text(self):
        user = User.objects.get(username="testuser")
        message = Message.objects.get(author=user)
        self.assertEqual(message.text, "hello twitter")

    def test_flagged(self):
        user = User.objects.get(username="testuser")
        message = Message.objects.get(author=user)
        self.assertEqual(message.flagged, False)
