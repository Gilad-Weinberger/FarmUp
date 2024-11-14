from django.core.management.base import BaseCommand
from base.models import Field, Line

class Command(BaseCommand):
    help = 'Create a specified number of Line objects for a given Field identified by its field_id (string)'

    def add_arguments(self, parser):
        parser.add_argument(
            'field_id',
            type=str,  # Change this to `str` since field_id is a CharField
            help='The field_id of the Field to add lines to'
        )
        parser.add_argument(
            'num_lines',
            type=int,
            help='The number of Line objects to create in the specified Field'
        )

    def handle(self, *args, **kwargs):
        field_id = kwargs['field_id']
        num_lines = kwargs['num_lines']
        
        # Fetch the field based on field_id (which is a CharField)
        try:
            field = Field.objects.get(field_id=field_id)
            self.stdout.write(self.style.SUCCESS(f'Found Field with field_id: {field.field_id}'))
        except Field.DoesNotExist:
            self.stdout.write(self.style.ERROR(f'No Field matches the specified field_id: {field_id}'))
            return
        
        # Create the specified number of Line objects
        for line_number in range(1, num_lines + 1):
            Line.objects.create(field=field, line_number=line_number)
        
        self.stdout.write(self.style.SUCCESS(f'Successfully created {num_lines} Line objects for Field with field_id {field.field_id}'))
