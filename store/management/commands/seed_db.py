from django.core.management.base import BaseCommand
from django.db import connection
from pathlib import Path
import os


class Command(BaseCommand):
    help = 'Populates the database with collections and products'

    def handle(self, *args, **options):
        print('Populating the database...')
        current_dir = os.path.dirname(__file__)
        file_path = os.path.join(current_dir, 'seed.sql')
        sql = Path(file_path).read_text()

        # Split SQL script into individual statements
        statements = sql.split(';')

        with connection.cursor() as cursor:
            for statement in statements:
                if statement.strip():  # Avoid executing empty statements
                    cursor.execute(statement)
        
        self.stdout.write(self.style.SUCCESS('Database populated successfully'))
