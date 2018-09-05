from django.db import models
from django.conf import settings
from django.utils import timezone
from django.dispatch import receiver
from django.db.models.signals import post_save

from rest_framework.authtoken.models import Token


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


class Application(models.Model):
    """
    Application model
    """
    name = models.CharField('Name', max_length=128, blank=False, null=False)
    app_admin = models.ForeignKey(settings.AUTH_USER_MODEL,  verbose_name = 'Owner Of Application', related_name='application',\
                                  on_delete=models.CASCADE)
    max_limit = models.PositiveIntegerField(default=0)
    status = models.CharField(max_length=10, choices=settings.STATUS_CHOICES, default='Active')
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name = "Application"
        verbose_name_plural = "Applications"

    def __str__(self):
        return self.name

    def delete(self):
        """
        Delete application
        """
        self.status = 'Delete'
        self.save()


class TextMessageHistory(models.Model):
    """
    TextMessageHistory model
    """
    application = models.ForeignKey('Application', related_name='text_message_history', blank=True, null=True,\
                                    on_delete=models.SET_NULL)
    send_to = models.CharField('Send To', max_length=20, blank=False, null=False)
    text_message = models.TextField(null=False, blank=False)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return 'Sent to %s at %s' % (self.send_to, self.created_at)
