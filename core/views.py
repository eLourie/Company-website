import logging
from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils.translation import gettext as _
from .models import Project
from .forms import ContactForm
from .services import send_all_notifications

logger = logging.getLogger(__name__)


def home(request):
    demo_projects = Project.objects.filter(category='demo')[:3]
    return render(request, 'core/home.html', {
        'demo_projects': demo_projects,
    })


def about(request):
    return render(request, 'core/about.html')


def projects(request):
    demo_projects = Project.objects.filter(category='demo')
    completed_projects = Project.objects.filter(category='completed')
    partner_projects = Project.objects.filter(category='partner')
    return render(request, 'core/projects.html', {
        'demo_projects': demo_projects,
        'completed_projects': completed_projects,
        'partner_projects': partner_projects,
    })


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            contact_message = form.save()

            # Send notifications (Telegram + Email)
            try:
                send_all_notifications(contact_message)
            except Exception as e:
                logger.error(f"Failed to send notifications: {e}")

            messages.success(request, _('Your message has been sent successfully!'))
            return redirect('contact')
    else:
        form = ContactForm()

    return render(request, 'core/contact.html', {
        'form': form,
    })
