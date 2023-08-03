from django.contrib import admin
from .models import Insured, Insurance, InsuranceEvent, Report

admin.site.register(Insured)
admin.site.register(Insurance)
admin.site.register(InsuranceEvent)
admin.site.register(Report)