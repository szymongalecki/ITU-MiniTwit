from django.shortcuts import render
from .models import Message, User, Follower

def timeline(request):
    if request.user.is_authenticated:
        user = User.objects.get(id=request.user.id)
        follower = Follower.objects.filter(who_id = user.id).values_list('whom_id')
        messages = Message.objects.filter(author_id__in = follower)
    else:
        user = None
        messages = Message.objects.get()
    context = {
        "messages":messages,
        "user":user
    }
    return render(request, 'MiniTwit/timeline.html', context)