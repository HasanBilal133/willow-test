from django import forms
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.db.models import Q

MyUser = get_user_model()


class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = MyUser
        fields = ('phone_number', 'email', "first_name", "last_name")

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = MyUser
        fields = ('phone_number', 'email', "first_name", "last_name", 'password', 'is_active', 'is_admin')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]


class UserLoginForm(forms.Form):
    phone_number = forms.CharField(label='phone_number')
    password = forms.CharField(label='password', widget=forms.PasswordInput)

    #check the username and password by overide the clean method
    def clean(self, *args, **kwargs):
        phone_number = self.cleaned_data.get('phone_number')
        password_field = self.cleaned_data.get('password')

        phone_number = MyUser.objects.filter(phone_number=phone_number) 
        user = (phone_number).distinct()
        if not user.exists() or user.count()!=1:
            raise forms.ValidationError('your phone_number or password wrong')
        user = user.first()
        if not user.check_password(password_field):
            raise forms.ValidationError('your phone_number or password wrong')

        return super(UserLoginForm, self).clean(*args, **kwargs)