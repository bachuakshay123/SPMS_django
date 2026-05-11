from django import forms
from spms.models import login
class LoginForm(forms.ModelForm):
    username=forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class':'form-control',
                'placeholder':'Username'
            }
        )
    )
    password=forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class':'form-control',
                'placeholder':'Password'
            }
        )
    )
    class Meta:
        model=login
        fields="__all__"

# class changepasswordForm(forms.ModelForm):
#     current_password=forms.CharField(
#         widget=forms.PasswordInput(
#             attrs={
#                 'class':'form-control',
#                 'placeholder':'Current password'
#             }
#         )
#     )
#     new_password=forms.CharField(
#         widget=forms.PasswordInput(
#             attrs={
#                 'class':'form-control',
#                 'placeholder':'New Password'
#             }
#         )
#     )
#     confirm_password=forms.CharField(
#         widget=forms.PasswordInput(
#             attrs={
#                 'class':'form-control',
#                 'placeholder':'Re-enter Password'
#             }
#         )
#     )