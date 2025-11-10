from django.contrib import admin
from .models import FormTemplate, FormSubmission

@admin.register(FormTemplate)
class FormTemplateAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at', 'is_active')
    readonly_fields = ('created_at',)
    search_fields = ('name',)

@admin.register(FormSubmission)
class FormSubmissionAdmin(admin.ModelAdmin):
    list_display = ('template', 'submitted_at')
    readonly_fields = ('submitted_at',)
    search_fields = ('template__name',)
