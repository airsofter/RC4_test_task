from django.db import models


class RobotModel(models.Model):
    name = models.CharField(max_length=2)

    def __str__(self):
        return self.name


class Robot(models.Model):
    serial = models.CharField(max_length=5)
    model = models.ForeignKey(
        RobotModel,
        on_delete=models.PROTECT,
        related_name='robots'
    )
    version = models.CharField(max_length=2)
    created = models.DateTimeField()

    def __str__(self):
        return self.serial
