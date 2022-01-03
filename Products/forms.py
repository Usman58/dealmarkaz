from django import forms
from django.contrib.auth.forms import UserCreationForm,UsernameField,AuthenticationForm,SetPasswordForm,PasswordChangeForm,PasswordResetForm,UserChangeForm
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import password_validation
from .models import *
class UserForm(UserCreationForm):
    password1 = forms.CharField(label='Password',widget=forms.PasswordInput(attrs={'class':'form-control'}))
    password2 = forms.CharField(label='Confirm Password',widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    email=forms.CharField(required=True,widget=forms.EmailInput(attrs={'class':'form-control'}))
    class Meta:
        model=User
        fields=['username','email','password1','password2']
        labels={'email':"Email"}
        widgets={'username':forms.TextInput(attrs={'class':'form-control'})}
class LoginForm(AuthenticationForm):
    username = UsernameField(widget=forms.TextInput(attrs={'autofocus':True,'class':'form-control'}))
    password= forms.CharField(label=_('Password'),strip=False,widget=forms.PasswordInput(attrs={'autocomplete':'current-password','class':'form-control'}))

class MyPasswordChangeForm(PasswordChangeForm):
    old_password =forms.CharField(label=_('Old Password'),strip=False,widget=forms.PasswordInput(attrs={'autocomplete':'current-password','autofocus':True,'class':'form-control'}))
    new_password1 =forms.CharField(label=_('Newe Password'),strip=False,widget=forms.PasswordInput(attrs={'autocomplete':'new-password','class':'form-control'}),help_text=password_validation.password_validators_help_text_html())
    new_password2 =forms.CharField(label=_('Confirm New Password'),strip=False,widget=forms.PasswordInput(attrs={'autocomplete':'new-password','class':'form-control'}))
class MyPasswordResetForm(PasswordResetForm):
    email = forms.CharField(label=_("Email"),max_length=254,widget=forms.EmailInput(attrs={'autocomplete':'email','class': 'form-control'}))
class MySetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(label=_('Newe Password'), strip=False, widget=forms.PasswordInput(attrs={'autocomplete': 'new-password', 'class': 'form-control'}),help_text=password_validation.password_validators_help_text_html())
    new_password2 = forms.CharField(label=_('Confirm New Password'), strip=False, widget=forms.PasswordInput(attrs={'autocomplete': 'new-password', 'class': 'form-control'}))

class ProductForm(forms.ModelForm):
  class Meta:
    model = Product
    fields = ['name','description','image','price','condition','category','brand']
    labels = {'condition':'Condition'}
    widgets = {
        'name': forms.TextInput(attrs={'class': 'form-control'}),
        'description': forms.Textarea(attrs={'class': 'form-control'}),
        'condition':forms.Select(attrs={'class': 'form-control'}),
        'brand': forms.Select(attrs={'class': 'form-control'}),
        'price': forms.NumberInput(attrs={'class': 'form-control'}),
        'category': forms.Select(attrs={'class': 'form-control'}),
        }
class UpdateProductForm(forms.ModelForm):
  class Meta:
    model = Product
    fields = ['name', 'description', 'brand','price','condition']
    labels = {'name':'Name', 'desciption':'Description','brand_name:':'Brand','price':'Price','condition':'Condition'}
    widgets = {'name':forms.TextInput(attrs={'class':'form-control'}),
    'description':forms.Textarea(attrs={'class':'form-control'}),
    'brand':forms.Select(attrs={'class':'form-control'}),
    'price': forms.NumberInput(attrs={'class': 'form-control'}),
    'condition':forms.Select(attrs={'class': 'form-control'})
    }

class BrandForm(forms.ModelForm):
    class Meta:
        model=Brand
        fields='__all__'
class EditUserProfileForm(UserChangeForm):
 password = None
 email = forms.CharField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
 username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
 first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
 last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
 class Meta:
  model = User
  fields = ['username','first_name','last_name','email']

class ProfileUpdateForm(forms.ModelForm):
    phone_number = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    city = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    bio= forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control'}))
    image = forms.ImageField(label=_('Change Profile Image'), required=False, error_messages={'invalid': _("Image files only")}, widget=forms.FileInput)
    class Meta:
        model = Profile
        fields = ['image','phone_number','city','bio']

