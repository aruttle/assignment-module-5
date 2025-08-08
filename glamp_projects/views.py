from django.shortcuts import render

def project_list(request):
    return render(request, 'glamp_projects/project_list.html')
