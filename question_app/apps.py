from django.apps import AppConfig


class QuestionAppConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "question_app"

    def ready(self):
        import hash_app.signals  # Mengimpor signals ketika aplikasi siap
