from django.db import models

# Create your models here.

class BaseModel(models.Model):
    """
    A base model for all models. In case you need to prevent XSS,
    override all saves here.
    """
    def save(self, *args, **kw):
        return super(BaseModel, self).save(*args, **kw)

    class Meta:
        abstract = True


