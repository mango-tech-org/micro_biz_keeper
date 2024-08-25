import os

import django


def pytest_configure():
    os.environ.setdefault(
        "DJANGO_SETTINGS_MODULE", "auth_service.settings"
    )
    django.setup()
