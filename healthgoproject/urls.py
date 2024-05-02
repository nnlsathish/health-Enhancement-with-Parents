"""
URL configuration for healthgoproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from operator import index
from django.contrib import admin
from django.urls import path
from healthgoapp.views import *

urlpatterns = [
    path("admin/", admin.site.urls),
    path('',index,name='index'),
    path("signup/",signup,name='signup'),
    path("login/",loginaction,name='login'),
    path('psignup/',psignup,name='psignup'),
    path('plogin/',plogin,name='plogin'),
    path('diet/',diet,name='diet'),
    path('vacction/',vacction,name='vacction'),
    path('appointment/',appointment,name='appointment'),
    path('appoint/',vappoint,name='appoint'),
    path('vaccine/',vaccine,name='vaccine'),
    path("view_doctor/", view_Doctor, name='view_doctor'),
    path("view_doctorQ/", view_DoctorQ, name='view_doctorQ'),
    path("delete_doctor(?P<int:pid>)", Delete_Doctor, name='delete_doctor'),
    path("view_patient/", view_Patient, name='view_patient'),
    path("delete_patient(?P<int:pid>)", Delete_Patient, name='delete_patient'),
    path('child/',child,name='child'),
    path('feedback/',feedback,name='feedback'),
    path("view_appointment/", view_appoint, name='view_appointment'),
    path("delete_appointment(?P<int:pid>)", Delete_appoint, name='delete_appointment'),
    path("view_appointmentQ/", view_appointmentQ, name='view_appointmentQ'),
    path("view_child/", view_child, name='view_child'),
    path("delete_child(?P<int:pid>)", Delete_child, name='delete_child'),
    path("view_vaccine/", view_vaccine, name='view_vaccine'),
    path("delete_vaccine(?P<int:pid>)", Delete_vaccine, name='delete_vaccine'),
    path('appointment_list', appointment_list, name='appointment_list'),
    path('mark(?p<int:appointment_id>)', mark_appointment, name='mark_appointment'),
    path('child/<int:child_id>/',edit_child, name='edit_child'),

    
]
