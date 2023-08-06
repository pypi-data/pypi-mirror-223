from django.conf import settings
from django.conf.global_settings import DEFAULT_FROM_EMAIL

APPOINTMENT_CLIENT_MODEL = getattr(settings, 'APPOINTMENT_CLIENT_MODEL', 'auth.User')
APPOINTMENT_BASE_TEMPLATE = getattr(settings, 'APPOINTMENT_BASE_TEMPLATE', 'base_templates/base.html')
APPOINTMENT_WEBSITE_NAME = getattr(settings, 'APPOINTMENT_WEBSITE_NAME', 'Website')
APPOINTMENT_PAYMENT_URL = getattr(settings, 'APPOINTMENT_PAYMENT_URL', None)
APPOINTMENT_THANK_YOU_URL = getattr(settings, 'APPOINTMENT_THANK_YOU_URL', None)
APPOINTMENT_SLOT_DURATION = getattr(settings, 'APPOINTMENT_SLOT_DURATION', 30)
APPOINTMENT_BUFFER_TIME = getattr(settings, 'APPOINTMENT_BUFFER_TIME', 0)
APPOINTMENT_LEAD_TIME = getattr(settings, 'APPOINTMENT_LEAD_TIME', (9, 0))
APPOINTMENT_FINISH_TIME = getattr(settings, 'APPOINTMENT_FINISH_TIME', (18, 30))
APP_DEFAULT_FROM_EMAIL = getattr(settings, 'DEFAULT_FROM_EMAIL', DEFAULT_FROM_EMAIL)
APP_TIME_ZONE = getattr(settings, 'TIME_ZONE', 'America/New_York')
