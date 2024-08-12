from django.contrib.auth.models import Group, Permission
from django.core.management import BaseCommand


class Command(BaseCommand):
    help = 'Создание группы и разрешений для модераторов'

    def handle(self, *args, **kwargs):

        moderator_group, created = Group.objects.get_or_create(name='Moderators')

        for model_name in ['lesson', 'course']:
            model_perms = Permission.objects.filter(content_type__model=model_name)
            for perm in model_perms:
                if not perm.codename.startswith(('add_', 'delete_')):
                    moderator_group.permissions.add(perm)

        if created:
            self.stdout.write(self.style.SUCCESS(f'Группа "{moderator_group.name}" успешно создана.'))
