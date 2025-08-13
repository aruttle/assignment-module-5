from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages as django_messages
from .models import Message
from .forms import MessageForm


@login_required
def inbox(request):
    items = (
        Message.objects
        .filter(recipient=request.user)
        .select_related('sender', 'recipient')
        .order_by('-sent_at')
    )
    return render(request, 'glamp_messaging/inbox.html', {'items': items})


@login_required
def view_message(request, message_id):
    message_obj = get_object_or_404(
        Message.objects.select_related('sender', 'recipient'),
        id=message_id,
        recipient=request.user
    )
    if not message_obj.read:
        message_obj.read = True
        message_obj.save(update_fields=['read'])

    return render(request, 'glamp_messaging/view_message.html', {'message_obj': message_obj})


@login_required
def send_message(request):
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            msg = form.save(commit=False)
            msg.sender = request.user
            msg.save()
            django_messages.success(request, 'Message sent.')
            return redirect('glamp_messaging:inbox')
    else:
        form = MessageForm()
    return render(request, 'glamp_messaging/send_message.html', {'form': form})
