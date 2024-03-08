from django.db import models


class Contact(models.Model):
    """ Model for email subscription """

    email = models.EmailField()
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.email
