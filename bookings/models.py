from django.db import models

# Create your models here.
from trains.models import Train

class Booking(models.Model):
    username = models.CharField(max_length=50)
    train = models.ForeignKey(Train, on_delete=models.CASCADE)
    seats_booked = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.username} - {self.train.train_name}"