from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import date


class Department(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self): return self.name


class User(AbstractUser):
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True)


class Trainee(models.Model):
    trainee_id = models.CharField(max_length=50, blank=True, null=True, verbose_name="ID")
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    speciality = models.CharField(max_length=100)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)

    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)

    PAID = 'Paid'
    UNPAID = 'Unpaid'
    PAYMENT_CHOICES = [(PAID, 'Paid'), (UNPAID, 'Unpaid')]
    paid = models.CharField(max_length=10, choices=PAYMENT_CHOICES, default=UNPAID)

    group = models.CharField(max_length=50, blank=True)
    note = models.TextField(blank=True)

    def __str__(self): return self.name

    @property
    def days_left(self):
        if self.end_date:
            return (self.end_date - date.today()).days
        return 0

class Registration(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    documnts = models.CharField(max_length=50)
    national_id = models.CharField(max_length=10)