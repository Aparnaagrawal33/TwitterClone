import random
from django.conf import settings
from django.http import HttpResponse, Http404, JsonResponse 
from django.shortcuts import render, redirect
from django.utils.http import is_safe_url

from .forms import TweetForm
from .models import Tweet

ALLOWED_HOSTS = settings.ALLOWED_HOSTS

# Create your views here.
def home_view(request, *args, **kwargs):
    print(request.user or None)
    #return HttpResponse("<h1>Hello World</h1>")
    return render(request,"pages/home.html", context={}, status=200)


def tweet_create_view(request, *args, **kwargs):
    user = request.user
    #print('Ajax is:' ,request.is_ajax())
    if not request.user.is_authenticated:
        user = None
        if request.is_ajax:
            return JsonResponse({},status = 401)
        return redirect (settings.LOGIN_URL)

    form= TweetForm(request.POST or None)
    print('post data is' , request.POST)
    next_url = request.POST.get('next') or None
    print("Next Url",next_url)
    if form.is_valid():
        obj= form.save(commit = False)

        #DO other form related logic
        obj.user = user
        obj.save()

        if request.is_ajax() :
            return JsonResponse(obj.serialize(), status = 201) # 201 is for created items
        if next_url!= None and is_safe_url(next_url, ALLOWED_HOSTS):
            return redirect(next_url)
        form = TweetForm()

        if form.errors:
            if request.is_ajax:
                return JsonResponse(form.errors, status = 400)
                
    return render(request,"components/form.html", context={"form":form})

def tweet_list_view(request, *args, **kwargs):
    """
    REST API VIEW
    consume by javascript/java/swift/ios/Android
    return JSON data
    """
    
    qs = Tweet.objects.all()
    tweets_list =[x.serialize() for x in qs]
    data={
        "isUser":False,
        "response": tweets_list
    }
    return JsonResponse(data)

def tweet_detail_view(request,tweet_id, *args, **kwargs):
    """
    REST API VIEW
    consume by javascript/java/swift/ios/Android
    return JSON data
    """
    data={
        "id": tweet_id,
        #"image_path": obj.image.url 
    }
    status = 200
    try:
        obj = Tweet.objects.get(id=tweet_id)
        data["content"]= obj.content
      
    except:
        data['message']="Not Found"
        status :  404
    return JsonResponse(data, status=status) #json.dumps content_type='application/json'
    
    #return HttpResponse(f"<h1>Hello {tweet_id} -{obj.content}</h1>")

