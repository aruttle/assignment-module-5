from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect


@login_required
def project_list(request):
    """
    Staff/superusers only. Non-staff get a friendly message and are sent home.
    """
    if not (request.user.is_staff or request.user.is_superuser):
        messages.error(request, "Projects is a staff-only area.")
        return redirect('core:home')

    return render(request, 'glamp_projects/project_list.html')
