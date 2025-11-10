from django.shortcuts import get_object_or_404, render
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.http import require_http_methods
from django.middleware.csrf import get_token
import json

from .models import FormTemplate, FormSubmission
from .utils import form_from_template


def render_form(request, pk):
    """
    GET: Render a page with the dynamic form. Includes CSRF token (cookie).
    """
    tpl = get_object_or_404(FormTemplate, pk=pk, is_active=True)
    FormClass = form_from_template(tpl)
    form = FormClass()
    # ensure CSRF cookie is set
    get_token(request)
    return render(request, 'formbuilder/render.html', {'form': form, 'template': tpl})


@require_http_methods(['POST'])
def submit_form(request, pk):
    """
    POST: Accept JSON payload via AJAX. Validate using generated FormClass.
    On success store FormSubmission and return JSON {'ok': True}.
    On failure return {'ok': False, 'errors': {...}} with status 400.
    """
    tpl = get_object_or_404(FormTemplate, pk=pk, is_active=True)
    FormClass = form_from_template(tpl)

    try:
        payload = json.loads(request.body.decode())
    except Exception:
        return HttpResponseBadRequest('Invalid JSON')

    # Basic normalization: convert empty strings to None for optional numeric fields if desired
    # but here we pass raw payload and let Django handle type conversions/validation.
    form = FormClass(payload)
    if form.is_valid():
        FormSubmission.objects.create(template=tpl, data=form.cleaned_data)
        return JsonResponse({'ok': True})
    else:
        # form.errors is an ErrorDict - convert to plain dict
        errors = {k: v.get_json_data() for k, v in form.errors.items()}
        # simpler front-end friendly format:
        simple_errors = {k: [e['message'] for e in v] for k, v in form.errors.items()}
        return JsonResponse({'ok': False, 'errors': simple_errors}, status=400)

def index(request):
    templates = FormTemplate.objects.filter(is_active=True).order_by('-created_at')
    return render(request, 'formbuilder/index.html', {'templates': templates})

