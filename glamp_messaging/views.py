from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages as flash
from .models import Message
from .forms import MessageForm


@login_required
def inbox(request):
    """
    Show messages where the logged-in user is the recipient.
    Defensive: select_related + try/except so a bad row won't 500 the page.
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
    Compose/send a message. Non-admins may only send to admins.
    """
    if request.method == 'POST':
        form = MessageForm(request.POST, user=request.user)
        if form.is_valid():
            msg = form.save(commit=False)

            # Server-side enforcement: non-admins may only send to admins
            if not (request.user.is_staff or request.user.is_superuser):
                if not (msg.recipient and (msg.recipient.is_staff or msg.recipient.is_superuser)):
                    form.add_error('recipient', 'You can only message the admin team.')
                    return render(request, 'glamp_messaging/send_message.html', {'form': form})

            msg.sender = request.user
            msg.save()
            flash.success(request, "Message sent.")
            return redirect('glamp_messaging:inbox')
        # If invalid, fall through to render with errors
    else:
        form = MessageForm(user=request.user)
        # Helpful notice if there are no admins to message
        if not (request.user.is_staff or request.user.is_superuser) and form.fields['recipient'].queryset.count() == 0:
            flash.error(request, "There are no admin accounts available to receive messages.")

    return render(request, 'glamp_messaging/send_message.html', {'form': form})


@login_required
def delete_message(request, message_id):
    """
    Allow sender or recipient to delete a message.
    GET -> confirm page
    POST -> delete then redirect to inbox with a toast
    """
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
