"""Verify migrations on a disposable copy of db.sqlite3, preserving the original."""
import os
from pathlib import Path
import shutil
import sqlite3
import tempfile


def main():
    project = Path(__file__).resolve().parent
    os.environ['DJANGO_SETTINGS_MODULE'] = 'mvote.settings'
    from django.conf import settings

    with tempfile.TemporaryDirectory(prefix='migration-check-', dir=project) as temporary:
        assert Path(temporary).resolve().is_relative_to(project)
        target = Path(temporary) / 'test.sqlite3'
        shutil.copy2(project / 'db.sqlite3', target)
        tables = ['mysite_product', 'mysite_category', 'mysite_order', 'mysite_orderitem']
        connection = sqlite3.connect(target)
        try:
            counts = {table: connection.execute('SELECT COUNT(*) FROM "%s"' % table).fetchone()[0]
                      for table in tables}
        finally:
            connection.close()
        settings.DATABASES = {
            'default': {'ENGINE': 'django.db.backends.sqlite3', 'NAME': str(target)}}
        import django
        from django.core.management import call_command
        from django.db import connections

        try:
            django.setup()
            call_command('migrate', interactive=False, verbosity=0)
            call_command('makemigrations', 'mysite', check=True, dry_run=True, verbosity=1)
            with connections['default'].cursor() as cursor:
                for table, before in counts.items():
                    cursor.execute('SELECT COUNT(*) FROM "%s"' % table)
                    if cursor.fetchone()[0] != before:
                        raise RuntimeError('Sample data count changed: ' + table)
        finally:
            connections.close_all()
        print('Database COPY: migrations and sample data-count preservation passed')


if __name__ == '__main__':
    main()
