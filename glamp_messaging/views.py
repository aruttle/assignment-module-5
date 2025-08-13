from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages as dj_messages
from .models import Message
from .forms import MessageForm


@login_required
def inbox(request):
    qs = (
        Message.objects
        .filter(recipient=request.user)
        .select_related("sender", "recipient")
        .order_by("-sent_at")
    )
    return render(request, "glamp_messaging/inbox.html", {"inbox_messages": qs})



@login_required
def view_message(request, message_id):
    # Recipient must match the current user
    msg = get_object_or_404(
        Message.objects.select_related("sender", "recipient"),
        id=message_id,
        recipient=request.user,
    )
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
            # Keep the flash message short so it doesn't look like a duplicate row
            dj_messages.success(request, "Message sent.")
            return redirect("glamp_messaging:inbox")
    else:
        form = MessageForm()
    return render(request, "glamp_messaging/send_message.html", {"form": form})
