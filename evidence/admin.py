from django.contrib import admin
from .models import Insured, Insurance , InsuranceEvent

admin.site.register(Insured)
admin.site.register(Insurance)
admin.site.register(InsuranceEvent)


