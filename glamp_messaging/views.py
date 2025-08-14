from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages as flash

from .models import Message
from .forms import MessageForm


@login_required
def inbox(request):
    """
    Show messages where the logged-in user is the recipient.
    If something goes wrong (DB, etc.), render the same template
    with an error banner instead of 500'ing.
    """
    inbox_messages = []
    inbox_error = None
    try:
        inbox_messages = (
            Message.objects
            .filter(recipient=request.user)
            .select_related("sender", "recipient")
            .order_by("-sent_at")
        )
        # Touch the queryset so DB errors surface here
        _ = list(inbox_messages[:1])
    except Exception as e:
        inbox_error = str(e)
        print("INBOX ERROR:", repr(e))

    return render(
        request,
        "glamp_messaging/inbox.html",
        {"inbox_messages": inbox_messages, "inbox_error": inbox_error},
    )


@login_required
def view_message(request, message_id):
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
    if request.method == "POST":
        form = MessageForm(request.POST, user=request.user)
        if form.is_valid():
            msg = form.save(commit=False)

            # Non-admins can only message admins
            if not (request.user.is_staff or request.user.is_superuser):
                if not (msg.recipient.is_staff or msg.recipient.is_superuser):
                    flash.error(request, "You can only message the admin team.")
                    return redirect("glamp_messaging:send_message")

            msg.sender = request.user
            msg.save()
            flash.success(request, "Message sent.")
            return redirect("glamp_messaging:inbox")
    else:
        form = MessageForm(user=request.user)
        if (
            not (request.user.is_staff or request.user.is_superuser)
            and form.fields["recipient"].queryset.count() == 0
        ):
            flash.error(request, "There are no admin accounts available to receive messages.")

    return render(request, "glamp_messaging/send_message.html", {"form": form})


@login_required
def delete_message(request, message_id):
    m = get_object_or_404(Message, id=message_id)

    # Only sender or recipient can delete
    if m.sender_id != request.user.id and m.recipient_id != request.user.id:
        flash.error(request, "You don't have permission to delete this message.")
        return redirect("glamp_messaging:inbox")

    if request.method == "POST":
        m.delete()
        flash.success(request, "Message deleted.")
        return redirect("glamp_messaging:inbox")

    return render(request, "glamp_messaging/confirm_delete.html", {"message_obj": m})
