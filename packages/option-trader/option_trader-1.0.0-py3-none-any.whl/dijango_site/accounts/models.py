from django.db import models

class IBConnection(models.Model):
    host = models.GenericIPAddressField(default='127.0.0.1')
    port = models.IntegerField(default=7497)
    ClientID = models.IntegerField(default=0)
    LogLevel = models.IntegerField(default=5)
    status = models.TextField(default='Not connected')
