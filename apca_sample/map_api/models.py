from django.db import models

# Create your models here.
class Unemployment(models.Model):
    geoid = models.IntegerField()
    county = models.CharField(max_length=100)
    year = models.IntegerField()
    labor_force = models.IntegerField()
    value = models.PositiveIntegerField()
    rate = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return self.county, self.year, self.rate