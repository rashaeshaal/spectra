
from django import forms
from .models import CustomUser, UserProfile



class UserForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ('email', 'name', 'mobile', 'otp')
        

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('profile_pic', 'address_line_1', 'address_line_2', 'postcode', 'area', 'state', 'country')
        
