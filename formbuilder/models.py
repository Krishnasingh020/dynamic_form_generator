from django.db import models
from django.utils import timezone

class FormTemplate(models.Model):
    name = models.CharField(max_length=200)
    # fields is expected to be a list of dicts describing fields
    fields = models.JSONField()
    created_at = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class FormSubmission(models.Model):
    template = models.ForeignKey(FormTemplate, on_delete=models.CASCADE, related_name='submissions')
    data = models.JSONField()
    submitted_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Submission {self.pk} for {self.template.name}"
