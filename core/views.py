from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils.translation import gettext as _
from .models import TeamMember, Project
from .forms import ContactForm


def home(request):
    featured_projects = Project.objects.filter(featured=True)[:3]
    return render(request, 'core/home.html', {
        'featured_projects': featured_projects,
    })


def about(request):
    return render(request, 'core/about.html')


def team(request):
    team_members = TeamMember.objects.all()
    return render(request, 'core/team.html', {
        'team_members': team_members,
    })


def projects(request):
    projects_list = Project.objects.all()
    return render(request, 'core/projects.html', {
        'projects': projects_list,
    })


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, _('Your message has been sent successfully!'))
            return redirect('contact')
    else:
        form = ContactForm()

    return render(request, 'core/contact.html', {
        'form': form,
    })
