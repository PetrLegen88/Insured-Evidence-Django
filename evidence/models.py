from django.db import models


class Insured(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    street = models.CharField(max_length=100)
    city = models.CharField(max_length=64)
    zipcode = models.IntegerField()
    phone = models.CharField(max_length=16)

    def __str__(self):
        return self.first_name + " " + self.last_name


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
        return f'{self.insurance} : {self.subject}'


class InsuranceEvent(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
    )
    insured = models.ForeignKey(Insured, on_delete=models.CASCADE, null=True)
    insurance = models.ForeignKey(Insurance, on_delete=models.CASCADE)
    description = models.TextField()
    date = models.DateField()
    status = models.CharField(max_length=32, choices=STATUS_CHOICES)
    note = models.TextField(blank=True, null=True)

    def __str__(self):
        return f'{self.insured.first_name} {self.insured.last_name} - {self.description}'
