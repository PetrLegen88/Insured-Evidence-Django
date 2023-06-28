"""
URL configuration for Evidence_pojistnych_udalosti project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from evidence import views
from django.conf import settings
from django.conf.urls.static import static
from accounts.views import sign_up, user_login, user_logout
from evidence.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.homepage, name='homepage'),
    path('insured/', views.insured, name='insured'),
    path('signup/', sign_up, name='sign_up'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('new_insured/', new_insured, name='new_insured'),
    path('insured/<int:insured_id>/', views.insured_detail, name='insured_detail'),
    path('add_insurance/<int:insured_id>/', views.add_insurance, name='add_insurance'),
    path('insurances/', views.insurances, name='insurances'),
    path('insurance/<int:insurance_id>/', views.insurance_detail, name='insurance_detail'),
    path('delete_insured/<int:insured_id>/', views.delete_insured, name='delete_insured'),
    path('insureds/edit/<int:insured_id>/', views.edit_insured, name='edit_insured'),
    path('delete_insurance/<int:insurance_id>/', views.delete_insurance, name='delete_insurance'),
    path('edit_insurance/<int:insurance_id>/', views.edit_insurance, name='edit_insurance'),

    path('insurance_events/', insurance_events, name='insurance_events'),
    path('insurance_event/<int:event_id>/', views.insurance_event_detail, name='insurance_event_detail'),
    path('event/delete/<int:event_id>/', views.delete_event, name='delete_event'),
    ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
