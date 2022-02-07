from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model

MyUser = get_user_model()

#choices
consultation_choices = [
    ("Clinical", "Clinical"),
    ("Online", "Online")
]

#validators 
def isDigitValidator(value):
    if not value.isdigit:
        raise ValidationError(f"Not Valid") 

#models
class Address(models.Model):
    country = models.CharField(max_length=120)
    city = models.CharField(max_length=120)
    street = models.CharField(max_length=120)
    zip_code = models.CharField(max_length=10, validators=[isDigitValidator])


class Specialities(models.Model):
    specialitie = models.CharField(max_length=120)

    def __str__(self):
        return self.specialitie
    


class Doctor(models.Model):
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    address = models.OneToOneField(Address, blank=True, null=True, on_delete=models.SET_NULL)
    consultation_type = models.CharField(max_length=10, choices=consultation_choices)
    consultation_price = models.IntegerField()
    specialities = models.ManyToManyField(Specialities)
    insurance_company = models.CharField(max_length=120)
    insurance_number = models.CharField(max_length=120, validators=[isDigitValidator])
    image = models.ImageField(upload_to='user_images', blank=True, null=True)

    def __str__(self):
        return self.user.first_name + ' ' + self.user.last_name
    

class Booking(models.Model):
    name = models.CharField(max_length=120)
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    appointment_at = models.DateTimeField()
    
    def __str__(self):
        return self.name
    

class Slot(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    available_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return str(self.available_at)
            