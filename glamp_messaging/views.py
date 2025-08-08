from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Message
from .forms import MessageForm

@login_required
def inbox(request):
    messages = Message.objects.filter(recipient=request.user).order_by('-sent_at')
    return render(request, 'glamp_messaging/inbox.html', {'messages': messages})

@login_required
def view_message(request, message_id):
    message = get_object_or_404(Message, id=message_id, recipient=request.user)
    if not message.is_read:
        message.is_read = True
        message.save()
    return render(request, 'glamp_messaging/view_message.html', {'message': message})

@login_required
def send_message(request):
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user
            message.save()
            return redirect('messaging:inbox')
    else:
        form = MessageForm()
    return render(request, 'glamp_messaging/send_message.html', {'form': form})
