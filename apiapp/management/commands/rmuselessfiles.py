from django.core.management import BaseCommand
from main  import tasks


class Command(BaseCommand):
    help = '''Schedule this in cronjob to remove img directories that haven't been used for 1 hour.
        Preferred format: */10 * * * * python /path/to/your/project/manage.py removeImgdir
        don't forget to : chmod +x /path/to/your/project/management/commands/removeImgdir.py
        '''
    def handle(self, *args, **options):
        tasks.delete_useless_files()
        self.stdout.write(self.style.SUCCESS('Image directories cleanup Done.'))