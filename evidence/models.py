from django.contrib.auth.models import User
from django.db import models


class Insured(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='insured', null=True)
    ROLE_CHOICES = (
        ('insurer', 'Insurer'),
        ('insured', 'Insured'),
    )

    first_name = models.CharField(max_length=100)
    profile_photo = models.ImageField(upload_to='profile_photos', blank=True, null=True)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, null=True)
    street = models.CharField(max_length=100)
    city = models.CharField(max_length=64)
    zipcode = models.IntegerField()
    phone = models.CharField(max_length=16)

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
    amount = models.IntegerField()
    valid_from = models.DateField()
    valid_until = models.DateField()

    def __str__(self):
        insured_names = [f"{insured.first_name} {insured.last_name}" for insured in self.insurance.all()]
        insured_list = ", ".join(insured_names)
        return f"({self.id}) {insured_list}: {self.subject}"


class InsuranceEvent(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
    )
    insured = models.ForeignKey(Insured, on_delete=models.CASCADE, null=True)
    description = models.TextField()
    date = models.DateField()
    status = models.CharField(max_length=32, choices=STATUS_CHOICES)
    note = models.TextField(blank=True, null=True)

    def __str__(self):
        return f'{self.insured.first_name} {self.insured.last_name} - {self.description}'