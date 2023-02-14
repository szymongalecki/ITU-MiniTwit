from django.shortcuts import render
from .models import Message, User, Follower

def timeline(request):
    if request.user.is_authenticated:
        user = User.objects.get(id=request.user.id)
        follower = Follower.objects.filter(who_id = user.id).values_list('whom_id')
        messages = Message.objects.filter(author_id__in = follower)
        view = "user_timeline"
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

def user_timeline(request, pk):
    profile_user = User.objects.get(username=pk)
    messages = Message.objects.filter(author_id = profile_user.id)
    if request.user.is_authenticated:
        user = User.objects.get(id=request.user.id)
        if Follower.objects.filter(who_id = user.id).filter(whom_id = profile_user.id).exists():
            followed = True
        else:
            followed = False
    else:
        user = None
    context = {
        "profile_user":profile_user,
        "view":"profile_user_timeline",
        "messages":messages,
        "user":user,
        "followed":followed
    } 
    print(context)
    return render(request, 'MiniTwit/timeline.html', context)

def login(request):
    return render(request, 'MiniTwit/login.html', {})

def logout(request):
    return render(request, 'MiniTwit/login.html', {})

def follow_user(request):
    return render(request, 'MiniTwit/login.html', {})

def unfollow_user(request):
    return render(request, 'MiniTwit/login.html', {})

def add_message(request):
    return render(request, 'MiniTwit/login.html', {})
