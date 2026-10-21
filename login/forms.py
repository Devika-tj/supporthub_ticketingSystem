from django import forms

from django.contrib.auth.forms import AuthenticationForm

from .models import User


class LoginForm(AuthenticationForm):

    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Enter your username',
                'autocomplete': 'username'
            }
        )
    )


    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Enter your password',
                'autocomplete': 'current-password'
            }
        )
    )


class CreateUserForm(forms.ModelForm):

    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control'
            }
        ),
        min_length=6
    )


    confirm_password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control'
            }
        ),
        label='Confirm Password'
    )


    class Meta:

        model = User

        fields = [
            'username',
            'password',
            'confirm_password',
            'full_name',
            'email',
            'phone',
            'role'
        ]


        widgets = {

            'username': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': '6 or 7 digit number'
                }
            ),

            'full_name': forms.TextInput(
                attrs={
                    'class': 'form-control'
                }
            ),

            'email': forms.EmailInput(
                attrs={
                    'class': 'form-control'
                }
            ),

            'phone': forms.TextInput(
                attrs={
                    'class': 'form-control'
                }
            ),

            'role': forms.Select(
                attrs={
                    'class': 'form-select'
                }
            ),
        }


    def clean(self):

        cleaned = super().clean()


        if cleaned.get('password') != cleaned.get(
            'confirm_password'
        ):

            raise forms.ValidationError(
                'Passwords do not match.'
            )


        if cleaned.get('role') not in {
            'staff',
            'support'
        }:

            raise forms.ValidationError(
                'This screen can create Staff or Support Staff accounts only.'
            )


        return cleaned


    def save(self, commit=True):

        user = super().save(commit=False)


        user.set_password(
            self.cleaned_data['password']
        )


        user.email_verified = bool(
            user.email
        )


        if commit:

            user.save()


        return user