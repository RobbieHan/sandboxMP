import logging

from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.signals import user_logged_in, user_logged_out, user_login_failed

from .models import Role, Menu

error_logger = logging.getLogger('sandbox_error')
info_logger = logging.getLogger('sandbox_info')


@receiver(post_save, sender=Menu)
def create_menu(sender, instance, **kwargs):
    queryset = Role.objects.filter(id=1)
    try:
        admin_role = queryset.get()
        admin_role.permissions.add(instance)
    except queryset.model.DoesNotExist as e:
        error_logger.error(e)


@receiver(user_logged_in)
def user_logged_in_handler(sender, request, user, **kwargs):
    ip = request.META.get('REMOTE_ADDR')
    msg = 'login user: {user}, remote ip: {ip}, action: login, status: successed'.format(
        user=user.username,
        ip=ip,
    )
    info_logger.info(msg)


@receiver(user_logged_out)
def user_logged_out_handler(sender, request, user, **kwargs):
    ip = request.META.get('REMOTE_ADDR')
    msg = 'login user: {user}, remote ip: {ip}, action: logout, status: successed'.format(
        user=user.username,
        ip=ip,
    )
    info_logger.info(msg)


@receiver(user_login_failed)
def user_login_failed_handler(sender, credentials, request, **kwargs):
    msg = 'logout failed for: {credentials}'.format(
        credentials=credentials,
    )

    info_logger.info(msg)

