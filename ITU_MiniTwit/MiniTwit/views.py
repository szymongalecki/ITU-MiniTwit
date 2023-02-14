import time
from django.shortcuts import render
from .models import Message, User, Follower

def timeline(request):
    if request.user.is_authenticated:
        user = User.objects.get(id=request.user.id)
        follower = Follower.objects.filter(who_id = user.id).values_list('whom_id')
        messages = Message.objects.filter(author_id__in = follower)
        view = "timeline"
    else:
        return public_timeline(request)
    context = {
        "view":view,
        "messages":messages,
        "user":user
    }
    return render(request, 'MiniTwit/timeline.html', context)

def public_timeline(request):
    if request.user.is_authenticated:
        user = User.objects.get(id=request.user.id)
    else:
        user = None
    messages = Message.objects.all()
    view = "public_timeline"
    context = {
        "view":view,
        "messages":messages,
        "user":user
    }
    return render(request, 'MiniTwit/timeline.html', context)

def user_profile_timeline(request, pk):
    profile_user = User.objects.get(username=pk)
    messages = Message.objects.filter(author_id = profile_user.id)
    if request.user.is_authenticated:
        user = User.objects.get(id=request.user.id)
        if Follower.objects.filter(who_id = user.id, whom_id = profile_user.id).exists():
            followed = True
        else:
            followed = False
    else:
        user = None
        followed = False
    context = {
        "profile_user":profile_user,
        "view":"profile_user_timeline",
        "messages":messages,
        "user":user,
        "followed":followed
    } 
    return render(request, 'MiniTwit/timeline.html', context)

def login(request):
    return render(request, 'MiniTwit/login.html', {})

def logout(request):
    return render(request, 'MiniTwit/login.html', {})

def follow_user(request, pk):
    user = User.objects.get(id=request.user.id)
    profile_user = User.objects.get(username=pk)
    following = Follower(who_id = user, whom_id = profile_user)
    following.save()
    return user_profile_timeline(request, profile_user.username)

def unfollow_user(request, pk):
    user = User.objects.get(id=request.user.id)
    profile_user = User.objects.get(username=pk)
    Follower.objects.filter(who_id = user.id, whom_id = profile_user.id).delete()
    return user_profile_timeline(request, profile_user.username)

def add_message(request, pk):
    user = User.objects.get(username=pk)
    message = Message(author_id = user.id, text = request.form['text'], pub_date = int(time.time()))
    message.save()
    return timeline(request)
