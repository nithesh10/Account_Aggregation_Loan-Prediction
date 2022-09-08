from django.contrib import admin
from .models import Profile
from .models import Data
# Register your models here.
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user','phone_number','email_verified','uuid']
class DataAdmin(admin.ModelAdmin):
    list_display = ('client_name', 'gender', 'mstatus',  'dependance',  'education', 'self_employed', 'appIncome', 'co_appIncome', 'loan_amount', 'loan_amount_term', 'credit_history', 'property_area')

admin.site.register(Data, DataAdmin)