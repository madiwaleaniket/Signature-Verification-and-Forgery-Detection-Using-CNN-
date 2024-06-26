from django.db import models

# Create your models here.

class Verify_sign(models.Model):
    pname = models.CharField(max_length=70)
    uploaded_doc = models.ImageField()
    match_file = models.CharField(max_length=70)
    match_percentage = models.CharField(max_length=70)

    def __str__(self) -> str:
        return super().__str__()