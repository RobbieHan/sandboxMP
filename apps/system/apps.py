from django.apps import AppConfig


class SystemConfig(AppConfig):
    name = 'system'

    def ready(self):
        from .signals import create_menu
        from .signals import user_logged_in_handler
        from .signals import user_logged_out_handler
        from .signals import user_login_failed_handler
