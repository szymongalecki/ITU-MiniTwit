import time
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .forms import CustomUserCreationForm
from .models import Message, User, Follower

def timeline(request):
    if request.user.is_authenticated:
        user = User.objects.get(id=request.user.id)
        follower = Follower.objects.filter(who_id = user.id).values_list('whom_id')
        messages = Message.objects.filter(author_id__in = follower).order_by('-pub_date')
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
    # messages = Message.objects.all().order_by('-pub_date')
    view = "public_timeline"
    messages = Message.objects.all().order_by('-pub_date')
    paginator = Paginator(messages, 10)  # 10 messages per page

    page = request.GET.get('page')
    try:
        messages_page = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        messages_page = paginator.page(1)
    except EmptyPage:
        # If page is out of range, deliver last page of results.
        messages_page = paginator.page(paginator.num_pages)

    context = {
        "view":view,
        "messages":messages,
        "user":user,
        'messages_page': messages_page
    }
    return render(request, 'MiniTwit/timeline.html', context)

def user_profile_timeline(request, pk):
    profile_user = User.objects.get(username=pk)
    messages = Message.objects.filter(author_id = profile_user.id).order_by('-pub_date')
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
    return render(request, 'registration/login.html', {})

def logout(request):
    return render(request, 'registration/login.html', {})

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

def add_message(request):
    user = User.objects.get(id=request.user.id)
    message = Message(author_id = request.user.id, text = request.POST.get('text',''), pub_date = int(time.time()))
    message.save()
    return timeline(request)

class SignUpView(generic.CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("MiniTwit:login")
    template_name = "registration/signup.html"
 