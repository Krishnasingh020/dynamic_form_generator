import json
from django.core.management.base import BaseCommand
from formbuilder.models import FormTemplate

class Command(BaseCommand):
    help = 'Export all form templates to a JSON file (list).'

    def add_arguments(self, parser):
        parser.add_argument('path', help='Output path for JSON file')

    def handle(self, *args, **options):
        path = options['path']
        templates = FormTemplate.objects.all()
        out = []
        for t in templates:
            out.append({'name': t.name, 'fields': t.fields})
        try:
            with open(path, 'w', encoding='utf-8') as fh:
                json.dump(out, fh, indent=2, ensure_ascii=False)
        except Exception as exc:
            self.stderr.write(f'Failed to write file: {exc}')
            return
        self.stdout.write(self.style.SUCCESS(f'Exported {len(out)} templates to {path}'))
