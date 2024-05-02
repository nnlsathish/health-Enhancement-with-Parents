from django.contrib import admin

from healthgoapp.models import Doctor, Patient, Appointment,review,Child
admin.site.register(Doctor)
admin.site.register(Patient)
admin.site.register(Appointment)
admin.site.register(Child)
admin.site.register(review)


# Register your models here.
