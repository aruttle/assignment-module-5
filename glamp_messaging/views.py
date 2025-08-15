from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from .models import Message
from .forms import MessageForm


def _require_auth(request):
    if not request.user.is_authenticated:
        return redirect(f"{reverse('users:login')}?next={request.get_full_path()}")
    return None


@login_required
def inbox(request):
    """
    Recipient mailbox with archived filter + simple search.

    Supports:
      - ?filter=active|archived|all  (preferred)
      - ?status=archived             (legacy)
      - ?archived=1/true/yes/y       (legacy boolean)
      - ?q=...                       (subject or sender name/email)
    """
    # Primary param
    primary = (request.GET.get("filter") or "").strip().lower()

    # Back-compat params
    status = (request.GET.get("status") or "").strip().lower()
    archived_flag = (request.GET.get("archived") or "").strip().lower()

    # Decide final filter value
    if primary in {"active", "archived", "all"}:
        filter_val = primary
    elif status == "archived":
        filter_val = "archived"
    elif archived_flag in {"1", "true", "yes", "y", "archived"}:
        filter_val = "archived"
    else:
        filter_val = "active"

    q = (request.GET.get("q") or "").strip()

    qs = (
        Message.objects.filter(recipient=request.user)
        .select_related("sender", "recipient")
        .order_by("-sent_at")
    )

    if filter_val == "archived":
        qs = qs.filter(archived=True)
    elif filter_val == "all":
        pass  # no archive filter
    else:
        # default to active
        filter_val = "active"
        qs = qs.filter(archived=False)

    if q:
        qs = qs.filter(
            Q(subject__icontains=q)
            | Q(sender__full_name__icontains=q)
            | Q(sender__email__icontains=q)
        )

    return render(
        request,
        "glamp_messaging/inbox.html",
        {"messages_qs": qs, "filter": filter_val, "q": q},
    )


@login_required
def view_message(request, pk):
    msg = get_object_or_404(
        Message.objects.select_related("sender", "recipient"),
        Q(sender=request.user) | Q(recipient=request.user),
        pk=pk,
    )
    if request.user == msg.recipient and not msg.read:
        msg.read = True
        msg.save(update_fields=["read"])
    can_archive = request.user == msg.recipient
    return render(request, "glamp_messaging/view_message.html", {"msg": msg, "can_archive": can_archive})


@login_required
def send_message(request):
    """
    Compose + send. Non-admin users can only message admins (also enforced on save).
    Supports prefill via GET ?to=<user_id>&subject=...
    """
    initial = {}
    to_param = request.GET.get("to")
    subject_param = request.GET.get("subject")
    if to_param and to_param.isdigit():
        initial["recipient"] = int(to_param)
    if subject_param:
        initial["subject"] = subject_param

    if request.method == "POST":
        form = MessageForm(request.POST, user=request.user)  # <-- pass user
        if form.is_valid():
            msg = form.save(commit=False)
            msg.sender = request.user

            # Enforce non-admin can only message admins
            if not request.user.is_staff and not msg.recipient.is_staff:
                form.add_error("recipient", "You can only message site administrators.")
            else:
                msg.save()
                messages.success(request, "Message sent successfully.")
                return redirect("glamp_messaging:inbox")

        messages.error(request, "Please fix the errors below.")
    else:
        form = MessageForm(initial=initial, user=request.user)  # <-- pass user

    return render(request, "glamp_messaging/send_message.html", {"form": form})


@login_required
def delete_message(request, pk):
    msg = get_object_or_404(
        Message,
        Q(sender=request.user) | Q(recipient=request.user),
        pk=pk,
    )
    if request.method == "POST":
        subject = msg.subject
        msg.delete()
        messages.success(request, f"Message “{subject}” deleted.")
        return redirect("glamp_messaging:inbox")
    return render(request, "glamp_messaging/confirm_delete.html", {"msg": msg})


@login_required
def archive_message(request, pk):
    msg = get_object_or_404(Message, pk=pk)
    if request.user != msg.recipient:
        messages.error(request, "You can only archive messages in your own inbox.")
        return redirect("glamp_messaging:inbox")
    if request.method == "POST":
        if not msg.archived:
            msg.archived = True
            msg.save(update_fields=["archived"])
            messages.success(request, "Message archived.")
        else:
            messages.info(request, "Message is already archived.")
    return redirect("glamp_messaging:inbox")


@login_required
def unarchive_message(request, pk):
    msg = get_object_or_404(Message, pk=pk)
    if request.user != msg.recipient:
        messages.error(request, "You can only unarchive your own messages.")
        return redirect("glamp_messaging:inbox")
    if request.method == "POST":
        if msg.archived:
            msg.archived = False
            msg.save(update_fields=["archived"])
            messages.success(request, "Message moved back to Inbox.")
        else:
            messages.info(request, "Message is already active.")
    return redirect("glamp_messaging:inbox")


@login_required
def reply_message(request, pk):
    msg = get_object_or_404(
        Message.objects.select_related("sender", "recipient"),
        Q(sender=request.user) | Q(recipient=request.user),
        pk=pk,
    )
    to_user = msg.sender if request.user == msg.recipient else msg.recipient
    if not request.user.is_staff and not to_user.is_staff:
        messages.error(request, "You can only message site administrators.")
        return redirect("glamp_messaging:inbox")

    subj = msg.subject or ""
    if not subj.lower().startswith("re:"):
        subj = f"Re: {subj}"
    return redirect(f"{reverse('glamp_messaging:send_message')}?to={to_user.id}&subject={subj}")
