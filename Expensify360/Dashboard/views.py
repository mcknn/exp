from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.shortcuts import render, redirect
from Dashboard.forms import *
from Dashboard.models import *


@login_required
def homepage(request):
    context = {}
    groups = request.user.groups.all()
    for g in groups:
        context[g] = list(Group.objects.get(id=g.id).user_set.all())
        context[g].remove(request.user)
    return render(request, 'homepage.html', {'groups': context})


@login_required
def create_org(request):
    if request.method == 'POST':
        form = CreateOrgForm(request.POST)
        if form.is_valid():
            org = Organization.create(
                name=form.cleaned_data['Organization_Name'],
                manager=request.user.username,
            )
            org.save()
            request.user.groups.add(org)
        return redirect('org_success')
    return render(request, 'create_org.html', {'form': CreateOrgForm()})


@login_required
def create_proj(request):
    if request.method == 'POST':
        form = CreateProjForm(request.POST)
        if form.is_valid():
            org_name = request.GET.get('org-name')
            prj = Project.create(
                name=form.cleaned_data['Project_Name'],
                manager=request.user.username,
                org_name=org_name
            )
            prj.save()
            request.user.groups.add(prj)
        return redirect('proj_success')
    return render(request, 'create-proj.html', {'form': CreateProjForm()})


def org_success(request):
    return render(request, template_name='org_success.html')


def proj_success(request):
    return render(request, template_name='proj_success.html')

