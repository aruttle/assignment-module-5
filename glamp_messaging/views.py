from django.contrib import messages
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from .models import Message
from .forms import MessageForm


@login_required
def inbox(request):
    msgs = (
        Message.objects
        .filter(recipient=request.user)
        .select_related("sender")
        .order_by("-sent_at")
    )
    return render(request, "glamp_messaging/inbox.html", {"messages": msgs})


@login_required
def view_message(request, message_id):
    # Fetch with related users to avoid extra queries
    msg = get_object_or_404(
        Message.objects.select_related("sender", "recipient"),
        id=message_id,
    )

    # Allow either recipient or sender to view; forbid others
    if msg.recipient_id != request.user.id and msg.sender_id != request.user.id:
        return HttpResponseForbidden("You do not have permission to view this message.")

    # Only mark read when the RECIPIENT opens it
    if request.user.id == msg.recipient_id and not getattr(msg, "is_read", False):
        try:
            msg.is_read = True
            msg.save(update_fields=["is_read"])
        except Exception:
            # If your model doesn't have is_read, we just ignore
            pass

    return render(request, "glamp_messaging/inbox.html", {"inbox_messages": msgs})



@login_required
def send_message(request):
    if request.method == "POST":
        form = MessageForm(request.POST)
        if form.is_valid():
            m = form.save(commit=False)
            m.sender = request.user
            m.save()
            messages.success(request, "Message sent.")
            return redirect("glamp_messaging:inbox")
        messages.error(request, "Please fix the errors below.")
    else:
        form = MessageForm()
    return render(request, "glamp_messaging/send_message.html", {"form": form})
