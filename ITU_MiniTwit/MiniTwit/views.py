from django.shortcuts import render
from .models import Message, User

def timeline(request):
    messages = Message.objects.filter()
    user = User.objects.get(id=request.user.id)
    context = {
        "messages":messages,
        "user":user
    }
    return render(request, 'MiniTwit/timeline.html', context)