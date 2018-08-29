from sms.models import *


def is_application_expire(app_id):
    app = Application.objects.get(pk=int(app_id), status='Active')
    sms_count = TextMessageHistory.objects.filter(application=app).count()
    if sms_count < app.max_limit:
        return True
    else:
        return False
