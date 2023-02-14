import time
from django.shortcuts import render
from .models import Message, User, Follower
from werkzeug.security import check_password_hash, generate_password_hash

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

def get_user_id(userName):
    user = User.objects.get(username = userName)
    return user if user else None

def register(request):
    #if request.user:
        #return timeline(request)
    error = None
    if request.method == 'POST':
        if not request.form['username']:
            error = 'You have to enter a username'
        elif not request.form['email'] or \
                 '@' not in request.form['email']:
            error = 'You have to enter a valid email address'
        elif not request.form['password']:
            error = 'You have to enter a password'
        elif request.form['password'] != request.form['password2']:
            error = 'The two passwords do not match'
        elif get_user_id(request.form['username']) is not None:
            error = 'The username is already taken'
        else:
            #newUser = User(username = request.form['username'], email = request.form['email'], password = generate_password_hash(request.form['password']))
            print('user created')
            #newUser.save()
            #flash('You were successfully registered and can login now')
            return render(request, 'MiniTwit/login.html', {})
    return render(request, 'MiniTwit/register.html', {error:error})
