from django import forms
from spms.models import login
from spms.models import Category
from spms.models import Vehicle

class LoginForm(forms.Form):
    username=forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class':'form-control',
                'placeholder':'Username'
            }
        )
    )
    mobile_number=forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class':'form-control',
                'placeholder':'Mobile Number'
            }
        )
    )
    password=forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class':'form-control',
                'placeholder':'Password'
            }
        )
    )

class ChangePasswordForm(forms.Form):
    
    current_password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Current Password'
            }
        )
    )
    new_password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'New Password'
            }
        )
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Re-enter Password'
            }
        )
    )

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = [
            'parking_area_number',
            'vehicle_type',
            'vehicle_limit',
            'parking_charge'
            ]

        widgets = {

            'parking_area_number': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Parking Area Number'
                }
            ),

            'vehicle_type': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Vehicle Type'
                }
            ),

            'vehicle_limit': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Vehicle Limit'
                }
            ),

            'parking_charge': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Parking Charge'
                }
            ),

        }


class VehicleForm(forms.ModelForm):

    class Meta:

        model = Vehicle

        fields = [
            'vehicle_number',
            'vehicle_type',
            'area_number',
            'parking_charge'
        ]

        widgets = {

            'vehicle_number': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Vehicle Number'
                }
            ),

            'vehicle_type': forms.Select(
                attrs={
                    'class': 'form-select'
                }
            ),

            'area_number': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Area Number'
                }
            ),

            'parking_charge': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Parking Charge'
                }
            ),

        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['vehicle_type'].queryset = \
            Category.objects.filter(status=True)