from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_page
from .models import Message

@login_required
@cache_page(60)  # Cache view for 60 seconds
def message_list(request):
    messages = Message.objects.filter(receiver=request.user).select_related('sender')
    return render(request, 'messaging/message_list.html', {'messages': messages})


@login_required
def delete_user(request):
    request.user.delete()
    return redirect('home')  # Replace 'home' with your landing page URL name
