from django.contrib.auth import get_user_model
from django.test import TestCase
from .models import Tweet
from rest_framework.test import APIClient

# Create your tests here.
User = get_user_model()
class TweetTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username = 'abc', password = 'abc1234')
        self.user2 = User.objects.create_user(username = 'xyz', password = 'abc987')
        
        Tweet.objects.create(content = 'my first Tweet', user = self.user)
        Tweet.objects.create(content = 'my third Tweet', user = self.user)
        Tweet.objects.create(content = 'my fourth Tweet', user = self.user2)
        self.currentCount = Tweet.objects.all().count()
        
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
        client.login(username=self.user.username, password='abc1234')
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
        self.assertEqual(len(response.json()), 5)
        
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
        response = client.post("/api/tweets/action/", {"id":2, "action":"retweet"})
        self.assertEqual(response.status_code,201)
        data = response.json()
        new_tweet_id = data.get("id")
        self.assertNotEqual(2, new_tweet_id)
        self.assertEqual(self.currentCount+1, new_tweet_id)
        
    def test_tweet_create_api_view(self):
        request_data = {"content":"This is my test tweet"}
        client = self.get_client()
        response = client.post("/api/tweets/create/", request_data)
        self.assertEqual(response.status_code, 201)
        response_data = response.json()
        new_tweet_id = response_data.get("id")
        self.assertEqual(self.currentCount+1, new_tweet_id)
     
    def test_tweet_detail_api_view(self):
        client = self.get_client()
        response = client.get("/api/tweets/1/")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        _id =  data.get("id")
        self.assertEqual(_id,1)
    
    def test_tweet_delete_api_view(self):
        client = self.get_client()
        response = client.delete("/api/tweets/1/delete/")
        self.assertEqual(response.status_code, 200)
        response = client.delete("/api/tweets/1/delete/")
        self.assertEqual(response.status_code, 404)
        response = client.delete("/api/tweets/3/delete/")
        self.assertEqual(response.status_code, 401)
        
        
        
        
        


       
    
        
    
    
        
        
    
        
    
    
    
    

