from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import Group
from .models import User
from .roles import MANDANT


# срабатывает автоматически после каждого сохранения User
@receiver(post_save, sender=User)
def assign_default_group(sender, instance, created, **kwargs):
    # created=True только при первом создании, а не при каждом изменении профиля
    if created:
        # ищем группу Mandant, если её ещё нет, создаём
        mandant_group, _ = Group.objects.get_or_create(name=MANDANT)
        # новый пользователь по умолчанию становится клиентом
        instance.groups.add(mandant_group)