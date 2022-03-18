from django.db import models


# Create your models here.
class ConferenceRoom(models.Model):
    name = models.CharField(max_length=255)
    capacity = models.PositiveSmallIntegerField()
    alcohol = models.BooleanField(default=False)


class Reservation(models.Model):
    date = models.DateField()
    comment = models.TextField(null=True)
    room_id = models.ForeignKey(ConferenceRoom, on_delete=models.PROTECT)

    class Meta:
        unique_together = ('date', 'room_id')