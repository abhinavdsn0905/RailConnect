from django.db import models

# Create your models here.
class Train(models.Model):
    train_number = models.CharField(max_length=10, unique=True)
    train_name = models.CharField(max_length=100)
    source = models.CharField(max_length=100)
    destination = models.CharField(max_length=100)
    departure_time = models.TimeField()
    arrival_time = models.TimeField()
    total_seats = models.IntegerField()
    available_seats = models.IntegerField()
    price = models.IntegerField()

    def __str__(self):
        return self.train_name