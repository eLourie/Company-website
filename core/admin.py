from django.contrib import admin
from .models import TeamMember, Project, ContactMessage


@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ('name', 'position', 'email', 'order')
    list_editable = ('order',)
    search_fields = ('name', 'position')
    ordering = ('order', 'name')


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'technologies', 'completed_date', 'featured')
    list_editable = ('featured',)
    list_filter = ('featured', 'completed_date')
    search_fields = ('title', 'description', 'technologies')
    ordering = ('-completed_date',)


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'created_at', 'is_read')
    list_editable = ('is_read',)
    list_filter = ('is_read', 'created_at')
    search_fields = ('name', 'email', 'subject', 'message')
    ordering = ('-created_at',)
    readonly_fields = ('created_at',)
