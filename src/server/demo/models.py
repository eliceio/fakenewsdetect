from django.db import models

# Create your models here.
class DB(models.Model):
    headlineID = models.IntegerField(primary_key=True)
    bodyID = models.IntegerField()
    stance1 = models.FloatField()
    stance2 = models.FloatField()
    stance3 = models.FloatField()
    stance4 = models.FloatField()
