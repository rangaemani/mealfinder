from django.db import models

# Create your models here.

class Meal(models.Model):
    dish = models.CharField(max_length=120)
    thumbnail = models.ImageField()

    def _str_(self):
        return self.dish