from django.db import models
from model.validators import validate_year


class Model(models.Model):
    name = models.CharField(max_length=100)
    issue_year = models.IntegerField(validators=[validate_year])
    body_style = models.CharField(max_length=60)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]
        verbose_name = "model"
        verbose_name_plural = "models"
