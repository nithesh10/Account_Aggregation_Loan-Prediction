from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
import uuid

from unicodedata import name
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from sklearn.tree import DecisionTreeClassifier
import joblib

# Create your models here.

phone_regex = RegexValidator(regex=r'^\+?1?\d{9,10}$', 
                                message = "Phone number must be entered in the format: '+999999999'. Up to 10 digits allowed.")

class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=17,validators=[phone_regex],unique=True)
    email_verified = models.BooleanField(default=False)
    uuid = models.UUIDField(default=uuid.uuid4,editable=False)

GENDER = (
		(0, 'Female'),
		(1, 'Male'),
	)
Mstatus = (
		(0, 'Single'),
		(1, 'Married'),
	)
Education = (
		(0, 'Graduated'),
		(1, 'Not Graduated'),
	)
Self_employed = (
		(0, 'No'),
		(1, 'Yes'),
	)
Credit_history = (
		(0, 'No'),
		(1, 'Yes'),
	)
Property_area = (
		(0, 'Rural'),
		(1, 'Semi-urban'),
        (2, 'Urban'),
	)

class Data(models.Model):
    client_name = models.CharField(max_length=100, null=True)
    gender = models.PositiveBigIntegerField(choices=GENDER, null=True)
    mstatus = models.PositiveBigIntegerField(choices=Mstatus, null=True)
    dependance = models.PositiveBigIntegerField(validators=[MinValueValidator(0), MaxValueValidator(10)], null=True)
    education = models.PositiveBigIntegerField(choices=Education, null=True)
    self_employed = models.PositiveBigIntegerField(choices=Self_employed, null=True)
    appIncome = models.PositiveBigIntegerField(validators=[MinValueValidator(100), MaxValueValidator(10000000)], null=True)
    co_appIncome = models.PositiveBigIntegerField(validators=[MinValueValidator(100), MaxValueValidator(10000000)], null=True)
    loan_amount = models.PositiveBigIntegerField(validators=[MinValueValidator(100), MaxValueValidator(100000)], null=True)
    loan_amount_term = models.PositiveBigIntegerField(validators=[MinValueValidator(90), MaxValueValidator(360)], null=True)
    credit_history = models.PositiveBigIntegerField(choices=Credit_history, null=True)
    property_area = models.PositiveBigIntegerField(choices=Property_area, null=True)
    loan_status = models.CharField(max_length=300, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    
    
    def save(self, *args, **kwargs):
        ml_model = joblib.load('ml_model/ml_loan_prediction.joblib')
        self.loan_status = ml_model.predict([[self.gender, self.mstatus, self.dependance,  self.education,  self.self_employed, self.appIncome, self.co_appIncome, self.loan_amount, self.loan_amount_term, self.credit_history, self.property_area ]])
        print("saved")
        return super().save(*args, **kwargs)
    
    class Meta:
        ordering = ['-date']
    
    def __str__(self):
        return self.name

