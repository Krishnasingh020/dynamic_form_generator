"""
Utility that converts a FormTemplate record (fields JSON) into a Django Form class.
The functions are purposely small and readable so it's easy to test and extend.
"""

from django import forms
from django.core.validators import RegexValidator, MinValueValidator, MaxValueValidator

# Supported field types; extend as needed.
FIELD_MAP = {
    'text': forms.CharField,
    'number': forms.IntegerField,
    'email': forms.EmailField,
    'textarea': forms.CharField,
    'select': forms.ChoiceField,
    'checkbox': forms.BooleanField,
}


def _build_widget_and_kwargs(field_cfg):
    """
    Build widget instance and kwargs for the field based on configuration.
    Returns (widget_instance, kwargs_dict).
    """
    ftype = field_cfg.get('type', 'text')
    label = field_cfg.get('label')
    required = bool(field_cfg.get('required', False))
    placeholder = field_cfg.get('placeholder')
    help_text = field_cfg.get('help_text')

    widget_attrs = {}
    if placeholder:
        widget_attrs['placeholder'] = placeholder
    if 'min' in field_cfg:
        widget_attrs['min'] = field_cfg['min']
    if 'max' in field_cfg:
        widget_attrs['max'] = field_cfg['max']
    if 'validation' in field_cfg:
        # For HTML5 pattern attribute (client-side), ensure not None
        widget_attrs['pattern'] = field_cfg['validation']

    # default widget selection
    if ftype == 'textarea':
        widget = forms.Textarea(attrs=widget_attrs)
    elif ftype == 'select':
        widget = forms.Select(attrs=widget_attrs)
    elif ftype == 'checkbox':
        widget = forms.CheckboxInput(attrs=widget_attrs)
    elif ftype == 'number':
        widget = forms.NumberInput(attrs=widget_attrs)
    else:
        widget = forms.TextInput(attrs=widget_attrs)

    kwargs = {
        'label': label or '',
        'required': required,
        'widget': widget,
    }
    if help_text:
        kwargs['help_text'] = help_text

    return widget, kwargs


def _build_validators(field_cfg):
    validators = []
    if 'validation' in field_cfg:
        validators.append(RegexValidator(regex=field_cfg['validation'], message='Invalid format.'))
    if 'min' in field_cfg:
        validators.append(MinValueValidator(field_cfg['min']))
    if 'max' in field_cfg:
        validators.append(MaxValueValidator(field_cfg['max']))
    return validators


def _build_field(field_cfg):
    """
    Convert single field configuration (dict) into (name, form_field_instance).
    Required keys: 'name', 'type' (type can be omitted -> default 'text').
    """
    if 'name' not in field_cfg:
        raise ValueError('Field configuration missing "name"')
    name = field_cfg['name']
    ftype = field_cfg.get('type', 'text')

    FieldClass = FIELD_MAP.get(ftype, forms.CharField)
    _, kwargs = _build_widget_and_kwargs(field_cfg)
    validators = _build_validators(field_cfg)
    if validators:
        # combine existing validators with the new ones (if any)
        kwargs_validators = kwargs.get('validators', [])
        kwargs['validators'] = kwargs_validators + validators

    # handle select choices
    if ftype == 'select':
        choices = field_cfg.get('choices', [])
        # Django ChoiceField expects an iterable of (value, label)
        kwargs['choices'] = [(c, c) if not isinstance(c, (list,tuple)) else tuple(c) for c in choices]

    # For checkboxes Django BooleanField doesn't accept validators or widget in same way;
    # we can still pass widget and required; leave validators empty for checkbox.
    if ftype == 'checkbox':
        # BooleanField expects required bool; it's okay.
        try:
            field_instance = FieldClass(**kwargs)
        except Exception:
            # fallback: create a simple BooleanField
            field_instance = forms.BooleanField(label=kwargs.get('label',''), required=kwargs.get('required', False))
    else:
        field_instance = FieldClass(**kwargs)

    return name, field_instance


def form_from_template(template):
    """
    Build a dynamic django.forms.Form subclass from a FormTemplate instance.
    Raises ValueError on malformed template.
    """
    if not isinstance(template.fields, list):
        raise ValueError('template.fields must be a list')

    fields = {}
    for f in template.fields:
        if not isinstance(f, dict):
            raise ValueError('each field must be a dictionary')
        name, form_field = _build_field(f)
        fields[name] = form_field

    DynamicForm = type(f"DynamicForm_{template.pk}", (forms.Form,), fields)
    return DynamicForm
