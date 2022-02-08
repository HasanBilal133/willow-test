from django.contrib.auth import get_user_model
from rest_framework import serializers, response
from .models import Doctor, Address, Specialities, Booking, Slot

MyUser = get_user_model()


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = '__all__' 


class SpecialitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Specialities
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = ('first_name', 'last_name',)


class AccountSerializer(serializers.ModelSerializer):
    address = AddressSerializer()
    specialities = SpecialitySerializer(many=True)
    user = UserSerializer(read_only=True)
    class Meta:
        model = Doctor
        fields = '__all__' 

    #customize the update method because it isn't able to update nested serializers
    def update(self, instance, validated_data):
        if 'address' in validated_data:
            nested_serializer = self.fields['address']
            nested_instance = instance.address
            nested_data = validated_data.pop('address')
            nested_serializer.update(nested_instance, nested_data)
        
        if 'specialities' in validated_data:
            nested_serializer = self.fields['specialities']
            nested_instance = instance.specialities
            nested_data = validated_data.pop('specialities')
        
        return super().update(instance, validated_data)


class BookingsSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = Booking 
        fields = '__all__'


class SlotSerializer(serializers.ModelSerializer):
    class Meta:
        model = Slot
        exclude = ('doctor',)


class RegisterSerializer(serializers.Serializer):
    email = serializers.EmailField()
    phone_number = serializers.CharField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    password1 = serializers.CharField()
    password2 = serializers.CharField()
    consultation_type = serializers.ChoiceField(choices=['Clinical', 'Online'])
    consultation_price = serializers.IntegerField()
    specialities = serializers.ListField()
    insurance_company = serializers.CharField()
    insurance_number = serializers.CharField()
    image = serializers.ImageField(allow_null=True)

    #customize the creat method because it is nested serializers 
    def create(self, validated_data):
        data = validated_data
        email = data.get('email')
        phone_number = data.get('phone_number')
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        password1 = data.get('password1')
        password2 = data.get('password2')
        consultation_type = data.get('consultation_type')
        consultation_price = data.get('consultation_price')
        specialities = data.get('specialities')
        insurance_company = data.get('insurance_company')
        insurance_number = data.get('insurance_number')
        image = data.get('image')

        if password1 != password2:
            raise serializers.ValidationError("Password must match")
            return data
        else:
            user = MyUser.objects.create_user(first_name, last_name, email, phone_number, password=password1)
            user.save()
            doctor = Doctor.objects.create(user=user, consultation_type=consultation_type, consultation_price=consultation_price, insurance_company=insurance_company, insurance_number=insurance_number, image=image)
            doctor.save()
            for speciality in specialities:
                speciality_object= Specialities.objects.create(specialitie=speciality)
                speciality_object.save()
                doctor.specialities.add(speciality_object)
            return data