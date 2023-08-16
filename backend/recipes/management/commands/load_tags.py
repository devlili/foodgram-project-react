from django.core.management import BaseCommand

from recipes.models import Tag


class Command(BaseCommand):
    help = 'Заполняем тэги'

    def handle(self, *args, **kwargs):
        data = [
            {'name': 'Завтрак', 'color': '#ed7c26', 'slug': 'breakfast'},
            {'name': 'Обед', 'color': '#24039b', 'slug': 'lunch'},
            {'name': 'Ужин', 'color': '#12a12a', 'slug': 'dinner'}]
        Tag.objects.bulk_create(Tag(**tag) for tag in data)
        self.stdout.write(self.style.SUCCESS('Все тэги загружены'))
