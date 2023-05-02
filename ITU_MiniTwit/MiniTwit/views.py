import datetime
import time
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views import generic
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth import logout, login
from .forms import CustomUserCreationForm, CustomLoginForm
from .models import Message, User, Follower
from django.views.decorators.http import require_POST, require_GET, require_http_methods


@require_GET
def timeline(request):
    if request.user.is_authenticated:
        user = User.objects.get(id=request.user.id)
        follower = Follower.objects.filter(who=user.id).values_list('whom')
        messages = Message.objects.filter(author__in=follower).order_by('-pub_date')
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
    else:
        return public_timeline(request)
    context = {
        "profile_user": user,
        "view": "my_timeline",
        "messages": messages,
        "user": user,
        'messages_page': messages_page
    }
    return render(request, 'MiniTwit/timeline.html', context)


@require_GET
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
        "profile_user": user,
        "view": view,
        "messages": messages,
        "user": user,
        'messages_page': messages_page
    }
    return render(request, 'MiniTwit/timeline.html', context)


@require_GET
def user_profile_timeline(request, pk):
    profile_user = User.objects.get(id=pk)
    messages = Message.objects.filter(author=profile_user.id).order_by('-pub_date')
    if request.user.is_authenticated:
        user = User.objects.get(id=request.user.id)
        if Follower.objects.filter(who=user.id, whom=profile_user.id).exists():
            followed = True
        else:
            followed = False
    else:
        user = None
        followed = False

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
        "profile_user": profile_user,
        "view": "profile_user_timeline",
        "messages": messages,
        "user": user,
        "followed": followed,
        'messages_page': messages_page

    }
    return render(request, "MiniTwit/timeline.html", context)


@require_http_methods(["GET", "POST"])
def index_login(request):
    if request.method == 'POST':
        form = CustomLoginForm(request=request, data=request.POST)
        if form.is_valid():
            profile_user = form.user_cache
            login(request, user=profile_user)
            return redirect('/')
    else:
        form = CustomLoginForm()

    context = {'form': form}
    return render(request, 'registration/login.html', context)


@require_http_methods(["GET", "POST"])
def index_logout(request):
    logout(request)
    return redirect('/login')


@require_http_methods(["GET", "POST"])
def follow_user(request, pk):
    user = User.objects.get(id=request.user.id)
    profile_user = User.objects.get(username=pk)
    following = Follower(who=user, whom=profile_user)
    following.save()
    return user_profile_timeline(request, profile_user.id)


@require_http_methods(["GET", "POST"])
def unfollow_user(request, pk):
    user = User.objects.get(id=request.user.id)
    profile_user = User.objects.get(username=pk)
    Follower.objects.filter(who=user.id, whom=profile_user.id).delete()
    return user_profile_timeline(request, profile_user.id)


@require_POST
def add_message(request):
    user = User.objects.get(id=request.user.id)
    message = Message(author=user, text=request.POST.get('text', ''),
                      pub_date=datetime.datetime.fromtimestamp(time.time()))
    message.save()
    return timeline(request)


class SignUpView(generic.CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("MiniTwit:login")
    template_name = "registration/signup.html"
