from django.db import models

# Create your models here.

class ClientModel(models.Model):
    name = models.CharField(max_length = 40)
    phone = models.CharField(max_length = 40)
    email = models.EmailField()
    message = models.TextField()

    def __str__(self):
        return self.email

        