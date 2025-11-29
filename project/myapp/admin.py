from django.contrib import admin
from .models import Student, FeeStructure, Payment, Owing

admin.site.register(Student)
admin.site.register(FeeStructure)
admin.site.register(Payment)
admin.site.register(Owing)
