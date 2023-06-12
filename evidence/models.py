from django.db import models
from django.contrib.auth.models import User


class Insured(models.Model):
    ROLE_CHOICES = (
        ('insurer', 'Insurer'),
        ('insured', 'Insured'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    street = models.CharField(max_length=100)
    city = models.CharField(max_length=64)
    zipcode = models.IntegerField()
    phone = models.CharField(max_length=16)

    def __str__(self):
        return self.user.first_name + self.user.last_name


class Insurance(models.Model):
    INSURANCE_TYPE = (
        ('home', 'Home insurance'),
        ('car', 'Car insurance'),
        ('property', 'Property insurance'),

    )
    insurance = models.ForeignKey(Insured, on_delete=models.CASCADE)
    type = models.CharField(max_length=32, choices=INSURANCE_TYPE)
    subject = models.CharField(max_length=32)
    amount = models.IntegerField()
    valid_from = models.DateTimeField()
    valid_until = models.DateTimeField()

    def __str__(self):
        return f'{self.insurance} {self.subject}'


class InsuranceEvent(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
    )
    insurance = models.ForeignKey(Insurance, on_delete=models.CASCADE)
    description = models.TextField()
    date = models.DateField()
    status = models.CharField(max_length=32, choices=STATUS_CHOICES)
    note = models.TextField(blank=True, null=True)

    def __str__(self):
        return f'Insurance event: {self.description}'
