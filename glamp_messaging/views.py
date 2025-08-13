# glamp_messaging/views.py
from django.contrib import messages as flash
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .forms import MessageForm
from .models import Message


@login_required
def inbox(request):
    """
    Show only the user's received messages.
    Use a safe ordering and avoid any 'messages' name collision.
    """
    try:
        qs = (
            Message.objects
            .filter(recipient=request.user)
            .select_related("sender", "recipient")
            .order_by("-id")  # safe on every DB; avoids sent_at mismatches
        )
        ctx = {"inbox_messages": qs}
        return render(request, "glamp_messaging/inbox.html", ctx)
    except Exception as e:
        # Surface the real error in logs and show a friendly page instead of 500
        print("INBOX ERROR:", repr(e))
        flash.error(request, "Sorry, we couldn’t load your inbox.")
        return render(request, "glamp_messaging/inbox.html", {"inbox_messages": []})


@login_required
def view_message(request, message_id):
    m = get_object_or_404(
        Message.objects.select_related("sender", "recipient"),
        id=message_id,
        recipient=request.user,
    )
    if not m.is_read:
        m.is_read = True
        m.save(update_fields=["is_read"])
    return render(request, "glamp_messaging/view_message.html", {"message": m})


@login_required
def send_message(request):
    if request.method == "POST":
        form = MessageForm(request.POST)
        if form.is_valid():
            m = form.save(commit=False)
            m.sender = request.user
            m.save()
            flash.success(request, "Message sent.")
            return redirect("glamp_messaging:inbox")
    else:
        form = MessageForm()
    return render(request, "glamp_messaging/send_message.html", {"form": form})
