from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages as flash
from .models import Message
from .forms import MessageForm


@login_required
def inbox(request):
    """
    Show messages where the logged-in user is the recipient.
    Extra defensive: select_related + try/except so a bad row
    won't 500 the whole page.
    """
    try:
        qs = (
            Message.objects
            .filter(recipient=request.user)
            .select_related("sender", "recipient")
            .order_by("-sent_at")
        )
    except Exception as e:
        # Log to server console and show a friendly message
        print("INBOX ERROR:", repr(e))
        flash.error(request, "Sorry, we couldn’t load your inbox.")
        qs = []

    return render(request, "glamp_messaging/inbox.html", {"inbox_messages": qs})


@login_required
def view_message(request, message_id):
    """
    Only the recipient can view. Mark as read safely.
    """
    m = get_object_or_404(
        Message.objects.select_related("sender", "recipient"),
        id=message_id,
        recipient=request.user,
    )
    if not m.read:
        m.read = True
        m.save(update_fields=["read"])
    return render(request, "glamp_messaging/view_message.html", {"message_obj": m})


@login_required
def send_message(request):
    """
    Send a message; show a success toast then redirect to inbox.
    """
    if request.method == "POST":
        form = MessageForm(request.POST)
        if form.is_valid():
            msg = form.save(commit=False)
            msg.sender = request.user
            msg.save()
            flash.success(request, "Message sent!")
            return redirect("glamp_messaging:inbox")
    else:
        form = MessageForm()
    return render(request, "glamp_messaging/send_message.html", {"form": form})
