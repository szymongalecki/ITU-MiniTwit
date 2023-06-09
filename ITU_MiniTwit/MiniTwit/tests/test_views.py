from django.test import TestCase
from django.utils import timezone
import os
from MiniTwit.models import User, Message, Follower

test_password = os.environ.get("TEST_PASSWORD")
public_page = "/public/"

class MessageListViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        User.objects.create(username="testuser1",email="testuser1@gmail.com")
        user1 = User.objects.get(username="testuser1")
        user1.set_password(test_password)
        user1.save()

        User.objects.create(username="testuser2",email="testuser2@gmail.com")
        user1 = User.objects.get(username="testuser1")

        for message_id in range(5):
            Message.objects.create(
                author=user1,
                text=f'message {message_id}',
                pub_date=timezone.now()
            )
                
    def test_public_timeline_reponse(self):
        response = self.client.get(public_page)
        self.assertEqual(response.status_code, 200)
        
    def test_number_of_messages(self):
        response = self.client.get(public_page)
        self.assertEqual(len(response.context["messages"]),5)

    def test_message_content(self):
        response = self.client.get(public_page)
        self.assertEqual(response.context["messages"].first().text,"message 4")

    def test_follow(self):
        self.client.login(username='testuser1', password=test_password)
        user1 = User.objects.get(username="testuser1")
        user2 = User.objects.get(username="testuser2")
        self.client.get('/testuser2/follow')
        follower = Follower.objects.get(who=user1)
        self.assertEqual(follower.whom,user2)

    def test_unfollow(self):
        self.client.login(username='testuser1', password=test_password)
        user1 = User.objects.get(username="testuser1")
        user2 = User.objects.get(username="testuser2")
        self.client.get('/testuser2/follow')
        follower = Follower.objects.get(who=user1)
        self.assertEqual(follower.whom,user2)
        self.client.get('/testuser2/unfollow')
        follower = Follower.objects.filter(who=user1)
        self.assertEqual(not follower, True)

