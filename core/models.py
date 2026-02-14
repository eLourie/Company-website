from django.db import models
from django.utils.translation import gettext_lazy as _


class TeamMember(models.Model):
    name = models.CharField(_('Name'), max_length=100)
    position = models.CharField(_('Position'), max_length=100)
    bio = models.TextField(_('Biography'))
    photo = models.ImageField(_('Photo'), upload_to='team/', blank=True)
    photo_url = models.URLField(_('Photo URL'), blank=True, help_text=_('External photo URL (takes priority over uploaded photo)'))
    email = models.EmailField(_('Email'), blank=True)
    linkedin = models.URLField(_('LinkedIn'), blank=True)
    order = models.PositiveIntegerField(_('Order'), default=0)

    def get_photo_url(self):
        """Return photo URL, preferring external URL over uploaded file"""
        if self.photo_url:
            return self.photo_url
        elif self.photo:
            return self.photo.url
        return None

    class Meta:
        verbose_name = _('Team Member')
        verbose_name_plural = _('Team Members')
        ordering = ['order', 'name']

    def __str__(self):
        return self.name


class Project(models.Model):
    title = models.CharField(_('Title'), max_length=200)
    description = models.TextField(_('Description'))
    image = models.ImageField(_('Image'), upload_to='projects/', blank=True)
    image_url = models.URLField(_('Image URL'), blank=True, help_text=_('External image URL (takes priority over uploaded image)'))
    url = models.URLField(_('URL'), blank=True)
    technologies = models.CharField(_('Technologies'), max_length=300)
    completed_date = models.DateField(_('Completed Date'))
    featured = models.BooleanField(_('Featured'), default=False)

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
