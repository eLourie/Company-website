from django import forms
from django.utils.translation import gettext_lazy as _
from .models import ContactMessage


class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'subject', 'message']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': _('Your Name'),
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-input',
                'placeholder': _('Your Email'),
            }),
            'subject': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': _('Subject'),
            }),
            'message': forms.Textarea(attrs={
                'class': 'form-input',
                'placeholder': _('Your Message'),
                'rows': 5,
            }),
        }
