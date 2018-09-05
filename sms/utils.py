import plivo

from django.conf import settings

from sms.models import *


def is_application_or_system_admin(request, app_id):
    app = Application.objects.get(pk=int(app_id), status='Active')
    if app.app_admin == request.user or request.user.is_staff:
        return True
    else:
        return False


def is_application_expire(app_id):
    app = Application.objects.get(pk=int(app_id), status='Active')
    sms_count = TextMessageHistory.objects.filter(application=app).count()
    if sms_count < app.max_limit:
        return False
    else:
        return True


def send_sms(send_to, msg):
    client = plivo.RestClient(settings.PLIVO_AUTH_ID, settings.PLIVO_AUTH_TOKEN)
    client.messages.create(src=settings.SENDER_NUMBER, dst=send_to, text=msg, )
    hst = TextMessageHistory.objects.create(send_to=send_to, text_message=msg)
    return hst
