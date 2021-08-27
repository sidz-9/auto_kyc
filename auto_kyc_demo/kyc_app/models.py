from django.db import models

# Create your models here.
class user_details(models.Model):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    mobile_number = models.CharField(max_length=10)
    user_id = models.IntegerField()

    def __str__(self):
        return self.first_name

class pan_db(models.Model):
    name = models.CharField(max_length=40)
    pan_number = models.CharField(max_length=10)
    dob = models.CharField(max_length=10)

    def __str__(self):
        return self.name