from django.conf import settings


def template_settings(request):
    return {
        'EMAIL_ENABLED': settings.EMAIL_ENABLED,
    }
