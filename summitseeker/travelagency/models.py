from django.db import models

# Create your models here.
class TravelAgency(models.Model):
    name = models.CharField(max_length=50)
    address = models.CharField(max_length=50)
    num_of_trips = models.IntegerField()
    duration = models.CharField(max_length=50)
    price = models.CharField(max_length=50)
    average_rating = models.FloatField()

    def __str__(self):
        return f'{self.name}-{self.price}-{self.average_rating}'

# I hope that contact number of two travel agencies are not same 
class ContactNumber(models.Model):
    contact_num = models.BigIntegerField(primary_key=True)
    travelagency = models.ForeignKey('TravelAgency',on_delete=models.CASCADE)
    