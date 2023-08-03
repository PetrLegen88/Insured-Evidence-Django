from django.contrib.auth.models import User
from django.db import models
from enum import Enum


class RoleEnum(Enum):
    Policyholder = 'insurer'
    Insured = 'insured'

    @classmethod
    def choices(cls):
        return [(key.value, key.name) for key in cls]


class Insured(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='insured', null=True, blank=True)
    first_name = models.CharField(max_length=100)
    profile_photo = models.ImageField(upload_to='profile_photos', blank=True, null=True)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    role = models.CharField(max_length=20, choices=RoleEnum.choices(), null=True)
    street = models.CharField(max_length=100)
    city = models.CharField(max_length=64)
    zipcode = models.CharField(max_length=16)
    phone = models.CharField(max_length=16)
    is_policyholder = models.BooleanField(default=False)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return f"({self.id}) {self.first_name} {self.last_name}"


class Insurance(models.Model):
    INSURANCE_TYPE = (
        ('home', 'Home insurance'),
        ('car', 'Car insurance'),
        ('property', 'Property insurance'),

    )
    insurance = models.ManyToManyField(Insured, related_name='insurance')
    type = models.CharField(max_length=32, choices=INSURANCE_TYPE)
    subject = models.CharField(max_length=32)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    valid_from = models.DateField()
    valid_until = models.DateField()

    class Meta:
        ordering = ['id']

    def __str__(self):
        insured_names = [f"{insured.first_name} {insured.last_name}" for insured in self.insurance.all()]
        insured_list = ", ".join(insured_names)
        return f"{insured_list}: {self.subject}"


class InsuranceEvent(models.Model):
    STATUS_CHOICES = (
        ('PENDING', 'Pending'),
        ('APPROVED', 'Approved'),
        ('REJECTED', 'Rejected'),
        ('IN_PROGRESS', 'In Progress'),
        ('COMPLETED', 'Completed'),
    )
    insurance = models.ForeignKey(Insurance, on_delete=models.CASCADE, null=True)
    subject = models.CharField(max_length=32, null=True)
    description = models.TextField()
    status = models.CharField(max_length=32, choices=STATUS_CHOICES)
    note = models.TextField(blank=True, null=True)
    date_submitted = models.DateField()
    date_completed = models.DateField(null=True, blank=True)
    total_payout = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return f'{self.insurance} - {self.subject}'


class Report(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    events = models.ManyToManyField(InsuranceEvent, related_name='reports')

    def __str__(self):
        return self.name
