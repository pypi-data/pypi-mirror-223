from django.db import models
from softdelete.models import SoftDeleteObject


# Create your models here.
class BaseModel(SoftDeleteObject, models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        ordering = ['-id']
