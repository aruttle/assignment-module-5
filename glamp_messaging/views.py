from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages as flash
from .models import Message
from .forms import MessageForm

@login_required
def inbox(request):
    items = (
        Message.objects
        .select_related('sender', 'recipient')
        .filter(recipient=request.user)
        .order_by('-sent_at')
    )
    return render(request, 'glamp_messaging/inbox.html', {'items': items})

@login_required
def view_message(request, message_id):
    message = get_object_or_404(Message, id=message_id, recipient=request.user)
    if not message.is_read:
        # Small optimization: avoid race by updating only this row
        Message.objects.filter(pk=message.pk, is_read=False).update(is_read=True)
        message.is_read = True
    return render(request, 'glamp_messaging/view_message.html', {'message': message})

@login_required
def send_message(request):
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.sender = request.user
            obj.save()
            flash.success(request, "Message sent.")
            return redirect('glamp_messaging:inbox')
    else:
        form = MessageForm()
    return render(request, 'glamp_messaging/send_message.html', {'form': form})
