#  * This file is part of recharge-me project.
#  * (c) Ochui Princewill Patrick <ochui.princewill@gmail.com>
#  * For the full copyright and license information, please view the "LICENSE.md"
#  * file that was distributed with this source code.

from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from allauth.account.forms import SignupForm, LoginForm, ResetPasswordForm, AddEmailForm
from phonenumber_field.formfields import PhoneNumberField
from phonenumber_field.widgets import PhoneNumberInternationalFallbackWidget
from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    """
    CustomUserCreationForm will be used from django admin site
    and is only available to staff users during user creation
    """

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = UserCreationForm.Meta.fields


class CustomUserChangeForm(UserChangeForm):
    """
    CustomUserChangeForm will be used from django admin site
    and is only available to staff users during user update
    """
    class Meta:
        model = CustomUser
        fields = UserChangeForm.Meta.fields


class CustomSignupForm(SignupForm):

    phone_number = PhoneNumberField()

    def __init__(self, *args, **kwargs):
        super(CustomSignupForm, self).__init__(*args, **kwargs)
        self.fields['email'].widget = forms.EmailInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'E-mail address',
                'autofocus': 'autofocus'
            }
        )

        self.fields['phone_number'].widget = PhoneNumberInternationalFallbackWidget(
            attrs={
                'class': 'form-control',
                'placeholder': '080xxxxxxxx'
            }
        )

        self.fields['password1'].widget = forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Password'
            }
        )

        self.fields['password2'].widget = forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Password (again)'
            }
        )


    def save(self, request):
        """
        Adds extra field data to the user instance
        returns User object.
        """
        user = super(CustomSignupForm, self).save(request)
        user.phone_number = self.cleaned_data['phone_number']
        user.save()
        return user


class CustomLoginForm(LoginForm):

    def __init__(self, *args, **kwargs):
        super(CustomLoginForm, self).__init__(*args, **kwargs)
        self.fields['login'].widget = forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Username or e-mail',
                'autofocus': 'autofocus'
            }
        )

        self.fields['password'].widget = forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Password',
            }
        )

        self.fields['remember'].widget = forms.CheckboxInput(
            attrs={
                'class': 'chk-remember'
            }
        )


class CustomResetPasswordForm(ResetPasswordForm):

    def __init__(self, *args, **kwargs):
        super(CustomResetPasswordForm, self).__init__(*args, **kwargs)
        self.fields['email'].widget = forms.EmailInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'E-mail address'
            }
        )

class EditProfileForm(forms.ModelForm):

    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'phone_number',
                    'date_of_birth', )
        widgets = {
            'first_name': forms.TextInput(
                attrs={
                    'class': 'form-control',
                }
            ),
            'last_name': forms.TextInput(
                attrs={
                    'class': 'form-control',
                }
            ),
            'phone_number': forms.TextInput(
                attrs={
                    'class': 'form-control'
                }
            ),
            'date_of_birth': forms.DateInput(
                attrs={
                    'class': 'form-control'
                }
            )
        }