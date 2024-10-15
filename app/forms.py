from django import forms
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm,UsernameField,PasswordChangeForm,PasswordResetForm,SetPasswordForm
from django.contrib.auth.models import User
from django.utils.translation import gettext,gettext_lazy as _
from django.contrib.auth import password_validation

class CustomerRegistrationform(UserCreationForm):
    password1=forms.CharField(label='Password',widget=forms.PasswordInput(attrs={'class':'form-control'}))
    password2=forms.CharField(label='Confirm Password',widget=forms.PasswordInput(attrs={'class':'form-control'}))
    email=forms.EmailField(required=True,widget=forms.EmailInput(attrs={'class':'form-control'}))
    class Meta:
        model=User
        fields=['username','email','password1','password2']
        labels={'email':'Email'}
        widgets={'username':forms.TextInput(attrs={'class':'form-control'})}


class Loginform(AuthenticationForm):
    username=UsernameField(widget=forms.TextInput(attrs={'autofocus':True,'class':'form-control'}))
    password=forms.CharField(label=('Password'),strip=False,widget=forms.PasswordInput(attrs={'autocomplete':'current-password','class':'form-control'}))

from django import forms
from django.contrib.auth.forms import PasswordChangeForm
from django.utils.translation import gettext_lazy as _



class MyPasswordChangeForm(PasswordChangeForm):
    
    old_password = forms.CharField(
        label=_("Old Password"),
        strip=False,  
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your old password',
            'autocomplete': 'current-password',
            'required': 'true'
        })
    )

   
    new_password1 = forms.CharField(
        label=_("New Password"),
        strip=False, 
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your new password',
            'autocomplete': 'new-password',
            'required': 'true'
        })
    )

   
    new_password2 = forms.CharField(
        label=_("Confirm New Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirm your new password',
            'autocomplete': 'new-password',
            'required': 'true'
        })
    )


class MyPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(
        label=_("Email"),
        max_length=254,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',  # Bootstrap styling
            'placeholder': 'Enter your email',
            'required': 'required',  # Make the field required
        }),
        error_messages={
            'required': _("Please enter your email address."),
            'invalid': _("Please enter a valid email address."),
        }
    )

    def clean_email(self):
        email = self.cleaned_data.get('email')
        # You can add custom validation here if needed
        return email



# forms.py


# forms.py



class Mysetpasswordform(SetPasswordForm):
    username = forms.CharField(
        label=_("Username"),
        max_length=150,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your username'}),
    )
    
    new_password1 = forms.CharField(
        label=_("New password"),
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter new password'}),
        strip=False,
        help_text=password_validation.password_validators_help_text_html(),
    )

    new_password2 = forms.CharField(
        label=_("Confirm new password"),
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm new password'}),
        strip=False,
    )

    def clean_new_password2(self):
        password1 = self.cleaned_data.get("new_password1")
        password2 = self.cleaned_data.get("new_password2")
        
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(_("The two password fields didn’t match."))

        # Check if the new password meets the validation criteria
        password_validation.validate_password(password=password1, user=self.user)
        
        return password2
