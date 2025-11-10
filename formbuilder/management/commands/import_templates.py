import json
from django.core.management.base import BaseCommand, CommandError
from formbuilder.models import FormTemplate

class Command(BaseCommand):
    help = 'Import form templates from a JSON file (list of templates).'

    def add_arguments(self, parser):
        parser.add_argument('path', help='Path to JSON file containing templates')

    def handle(self, *args, **options):
        path = options['path']
        try:
            with open(path, 'r', encoding='utf-8') as fh:
                data = json.load(fh)
        except Exception as exc:
            raise CommandError(f'Failed to read JSON: {exc}')

        if not isinstance(data, list):
            raise CommandError('JSON must be a list of templates.')

        created = 0
        updated = 0
        for tpl in data:
            if not isinstance(tpl, dict) or 'name' not in tpl or 'fields' not in tpl:
                self.stdout.write(self.style.ERROR(f'Skipping invalid template entry: {tpl}'))
                continue
            name = tpl['name']
            fields = tpl['fields']
            if not isinstance(fields, list):
                self.stdout.write(self.style.ERROR(f'Invalid fields for template "{name}", expected list.'))
                continue
            obj, is_created = FormTemplate.objects.update_or_create(name=name, defaults={'fields': fields})
            if is_created:
                created += 1
            else:
                updated += 1
            self.stdout.write(self.style.SUCCESS(f'Imported/updated template: {name}'))
        self.stdout.write(self.style.SUCCESS(f'Done. Created: {created}, Updated: {updated}'))
