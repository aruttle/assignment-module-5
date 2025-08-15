from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.db.models import Prefetch, Q

from .models import GlampProject
from .forms import ProjectForm


def _staff_gate(request):
    """Return a redirect response if user is not allowed; None if OK."""
    if not request.user.is_authenticated:
        return redirect(f"{reverse('users:login')}?next={request.get_full_path()}")
    if not (request.user.is_staff or request.user.is_superuser):
        messages.error(request, "Projects is a staff-only area.")
        return redirect('core:home')
    return None


def project_list(request):
    guard = _staff_gate(request)
    if guard:
        return guard

    qs = GlampProject.objects.all().prefetch_related(
        Prefetch("stakeholders")
    )

    q = (request.GET.get("q") or "").strip()
    status = (request.GET.get("status") or "").strip()

    if q:
        qs = qs.filter(Q(name__icontains=q) | Q(description__icontains=q))
    if status:
        qs = qs.filter(status=status)

    context = {
        "projects": qs,
        "q": q,
        "status": status,
        "status_choices": GlampProject.STATUS_CHOICES,
    }
    return render(request, "glamp_projects/project_list.html", context)


def project_detail(request, pk):
    guard = _staff_gate(request)
    if guard:
        return guard

    project = get_object_or_404(GlampProject.objects.prefetch_related("stakeholders"), pk=pk)
    return render(request, "glamp_projects/project_detail.html", {"project": project})


def project_create(request):
    guard = _staff_gate(request)
    if guard:
        return guard

    if request.method == "POST":
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save()
            messages.success(request, "Project created.")
            return redirect("projects:project_detail", pk=project.pk)
        messages.error(request, "Please fix the errors below.")
    else:
        form = ProjectForm()
    return render(request, "glamp_projects/project_form.html", {"form": form, "is_create": True})


def project_edit(request, pk):
    guard = _staff_gate(request)
    if guard:
        return guard

    project = get_object_or_404(GlampProject, pk=pk)
    if request.method == "POST":
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            messages.success(request, "Project updated.")
            return redirect("projects:project_detail", pk=project.pk)
        messages.error(request, "Please fix the errors below.")
    else:
        form = ProjectForm(instance=project)
    return render(request, "glamp_projects/project_form.html", {"form": form, "project": project, "is_create": False})


def project_delete(request, pk):
    guard = _staff_gate(request)
    if guard:
        return guard

    project = get_object_or_404(GlampProject, pk=pk)
    if request.method == "POST":
        project.delete()
        messages.success(request, "Project deleted.")
        return redirect("projects:project_list")
    return render(request, "glamp_projects/confirm_delete.html", {"project": project})
