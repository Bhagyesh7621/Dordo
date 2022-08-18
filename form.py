from django.contrib.auth.forms import (UserCreationForm,AuthenticationForm,PasswordChangeForm,UserChangeForm,PasswordResetForm,SetPasswordForm)
from django.contrib.auth.models import User
from django import forms

from med.models import CustomeraddressModel


class SignupForm(UserCreationForm):
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}))
    class Meta:
        model = User
        fields = ['username','email','password1','password2']

        widgets = {
            'username':forms.TextInput(attrs={'class':'form-control'}),
            # 'first_name':forms.TextInput(attrs={'class':'form-control'}),
            # 'last_name':forms.TextInput(attrs={'class':'form-control'}),
            'email':forms.EmailInput(attrs={'class':'form-control'}),
        }



    def clean_email(self):
        email = self.cleaned_data['email']
        if email == '':
            raise forms.ValidationError('This field is required.')
        else:
            return email


#user signin
class SigninForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}))

    class Meta:
        model = User
        fields = ['username','password']



# User Change Password with Old Password
class PassChangeForm(PasswordChangeForm):
    old_password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Enter Your Old Password'}))
    new_password1 =forms.CharField(label='New Password',widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Enter New Password'}))
    new_password2 =forms.CharField(label='Confirm New Password',widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Enter Re-New Password'}))



#user resetpassword
# Password Reset TextBox With Registred E-Mail
class PassResetForm(PasswordResetForm):
    email = forms.CharField(widget=forms.EmailInput(attrs={'class':'form-control','placeholder':'Enter Your Registered E-Mail'}))
    
# New Password Set Registred E-Mail Link
class SetNewPassForm(SetPasswordForm):
    new_password1 = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'Enter New Password'}))
    new_password2 = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'Confirm New Password'}))
# Profile




class UserProfileChangeForm(UserChangeForm):
    password = None

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', ]
        widgets = {
        
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Username'}),

            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter First Name'}),

            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Last Name'}),

            'email': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter E-Mail'}),


        }


# Customer Address CRUD
class CustomeraddressForm(forms.ModelForm):
    class Meta:
        model = CustomeraddressModel
        fields = ['fname', 'lname', 'email', 'mobile', 'counrty',
                  'state', 'city', 'pincode', 'add1', 'add2', ]
        widgets = {

            # 'user':forms.Select(attrs={'class':'form-control','placeholder':'Enter Username'}),

            'fname': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter First Name'}),

            'lname': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Last Name'}),

            'email': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter E-Mail'}),

            'mobile': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter mobile no'}),

            'counrty': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter country'}),

            'state': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter state'}),

            'city': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter city'}),

            'pincode': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter pincode'}),

            'add1': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter address'}),

            'add2': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter address'}),
        }