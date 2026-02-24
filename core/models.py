from django.db import models
from django.utils.translation import gettext_lazy as _


class Project(models.Model):
    CATEGORY_CHOICES = [
        ('demo', 'Демонстрационный'),
        ('completed', 'Выполненный'),
        ('partner', 'Компания-партнёр'),
    ]

    title = models.CharField(_('Title'), max_length=200)
    description = models.TextField(_('Description'))
    image = models.ImageField(_('Image'), upload_to='projects/', blank=True)
    image_url = models.URLField(_('Image URL'), blank=True, help_text=_('External image URL (takes priority over uploaded image)'))
    url = models.URLField(_('URL'), blank=True)
    technologies = models.CharField(_('Technologies'), max_length=300)
    completed_date = models.DateField(_('Completed Date'))
    featured = models.BooleanField(_('Featured'), default=False)
    category = models.CharField(_('Category'), max_length=20, choices=CATEGORY_CHOICES, default='demo')

    def get_image_url(self):
        """Return image URL, preferring external URL over uploaded file"""
        if self.image_url:
            return self.image_url
        elif self.image:
            return self.image.url
        return None

    class Meta:
        verbose_name = _('Project')
        verbose_name_plural = _('Projects')
        ordering = ['-completed_date']

    def __str__(self):
        return self.title


class ContactMessage(models.Model):
    name = models.CharField(_('Name'), max_length=100)
    email = models.EmailField(_('Email'))
    subject = models.CharField(_('Subject'), max_length=200)
    message = models.TextField(_('Message'))
    created_at = models.DateTimeField(_('Created At'), auto_now_add=True)
    is_read = models.BooleanField(_('Is Read'), default=False)

    class Meta:
        verbose_name = _('Contact Message')
        verbose_name_plural = _('Contact Messages')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} - {self.subject}"
