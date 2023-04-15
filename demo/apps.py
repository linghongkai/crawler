from django.apps import AppConfig




class DemoConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'demo'

    def ready(self):
        from demo import start_spider_thread
        start_spider_thread()
