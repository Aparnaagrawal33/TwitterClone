from django.contrib.auth import get_user_model
from django.test import TestCase
from .models import Tweet
from rest_framework.test import APIClient

# Create your tests here.
User = get_user_model()
class TweetTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username = 'abc', password = 'abc1234')
        Tweet.objects.create(content = 'my first Tweet', user = self.user)
        Tweet.objects.create(content = 'my third Tweet', user = self.user)
        Tweet.objects.create(content = 'my fourth Tweet', user = self.user)
        
        #User.objects.create_user(username = 'def', password = 'def1234')
        #User.objects.create_user(username = 'pqr', password = 'pqr1234')
        
    def test_user_created(self):
        user = User.objects.get(username = 'abc')
        self.assertEqual(user.username, 'abc')
        
    def test_tweet_created(self):
        tweet_obj = Tweet.objects.create(content = 'my second Tweet', user = self.user)
        self.assertEqual(tweet_obj.id, 4)
        self.assertEqual(tweet_obj.user, self.user)
     
     
    def get_client(self):
        client = APIClient()
        client.login(username=self.user.username, password='1234')
        return client
       
    def test_tweet_list(self):
        client = self.get_client()
        response = client.get("/api/tweets/")
        self.assertEqual(response.status_code,200)
        self.assertEqual(len(response.json()), 3)
        
    def test_action_like(self):
        client = self.get_client()
        response = client.post("/api/tweets/action/", {"id":1, "action":"like"})
        self.assertEqual(response.status_code,200)
        #print(response.json())
        self.assertEqual(len(response.json()), 3)
        
    def test_action_unlike(self):
        client = self.get_client()
        response = client.post("/api/tweets/action/", {"id":2, "action":"like"})
        self.assertEqual(response.status_code,200)
        response = client.post("/api/tweets/action/", {"id":2, "action":"unlike"})
        self.assertEqual(response.status_code,200)
        like_count = response.json().get("likes")
        self.assertEqual(like_count,0)
            
        #self.assertEqual(response.status_code,200)
        
    def test_action_retweet(self):
        client = self.get_client()
        response = client.post("/api/tweets/action/", {"id":1, "action":"retweet"})
        self.assertEqual(response.status_code,201)
    
    
    
    

