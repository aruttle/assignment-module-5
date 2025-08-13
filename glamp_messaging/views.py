from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Message
from .forms import MessageForm


@login_required
def inbox(request):
    # Show newest first; prefetch sender for fewer queries
    inbox_qs = (
        Message.objects
        .filter(recipient=request.user)
        .select_related("sender")
        .order_by("-sent_at")
    )
    return render(request, "glamp_messaging/inbox.html", {"messages": inbox_qs})


@login_required
def view_message(request, message_id):
    msg = get_object_or_404(Message, id=message_id, recipient=request.user)
    if not msg.is_read:
        msg.is_read = True
        msg.save(update_fields=["is_read"])
    return render(request, "glamp_messaging/view_message.html", {"message": msg})


@login_required
def send_message(request):
    if request.method == "POST":
        form = MessageForm(request.POST)
        if form.is_valid():
            msg = form.save(commit=False)
            msg.sender = request.user
            msg.save()
            messages.success(request, "Message sent.")
            # IMPORTANT: use the correct namespace from config.urls include()
            return redirect("glamp_messaging:inbox")
        else:
            messages.error(request, "Please fix the errors below.")
    else:
        form = MessageForm()

    return render(request, "glamp_messaging/send_message.html", {"form": form})
