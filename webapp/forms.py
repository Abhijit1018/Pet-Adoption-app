from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordResetForm, SetPasswordForm
from django.contrib.auth.models import User
from .models import Pet, UserProfile, AdminProfile, PetRegistrationRequest
from django.core.exceptions import ValidationError

class PasswordVisibilityMixin:
    """Mixin to add password visibility toggle to forms"""
    def add_password_toggle(self, field_name):
        if field_name in self.fields:
            self.fields[field_name].widget.attrs.update({
                'class': 'form-control password-field',
                'data-toggle': 'password'
            })

class RegisterForm(UserCreationForm, PasswordVisibilityMixin):
    email = forms.EmailField(required=True)
    age = forms.IntegerField(required=True, min_value=13, max_value=120, 
                           help_text="Must be at least 13 years old")
    phone_number = forms.CharField(max_length=15, required=True, 
                                 help_text="Include country code if international")
    gender = forms.ChoiceField(choices=UserProfile.GENDER_CHOICES, required=True)
    location = forms.CharField(max_length=100, required=True,
                             help_text="City, State/Province, Country")

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add password visibility toggle
        self.add_password_toggle('password1')
        self.add_password_toggle('password2')
        
        # Update widget attributes
        self.fields['password1'].widget.attrs.update({
            'class': 'form-control password-field',
            'placeholder': 'Enter password'
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'form-control password-field',
            'placeholder': 'Confirm password'
        })
    
    def save(self, commit=True):
        user = super().save(commit=commit)
        if commit:
            UserProfile.objects.create(
                user=user,
                age=self.cleaned_data['age'],
                phone_number=self.cleaned_data['phone_number'],
                gender=self.cleaned_data['gender'],
                location=self.cleaned_data['location']
            )
        return user

class AdminRegistrationForm(UserCreationForm, PasswordVisibilityMixin):
    email = forms.EmailField(required=True)
    admin_code = forms.CharField(max_length=50, required=True, 
                               help_text="Special admin registration code")
    
    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add password visibility toggle
        self.add_password_toggle('password1')
        self.add_password_toggle('password2')
        
        # Update widget attributes
        self.fields['password1'].widget.attrs.update({
            'class': 'form-control password-field',
            'placeholder': 'Enter password'
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'form-control password-field',
            'placeholder': 'Confirm password'
        })
    
    def clean_admin_code(self):
        admin_code = self.cleaned_data.get('admin_code')
        # You can change this secret code
        if admin_code != "PET_ADMIN_2025":
            raise ValidationError("Invalid admin registration code.")
        return admin_code
    
    def clean(self):
        cleaned_data = super().clean()
        if not AdminProfile.can_create_admin():
            raise ValidationError("Maximum number of admin accounts (3) already created.")
        return cleaned_data
    
    def save(self, commit=True):
        user = super().save(commit=commit)
        if commit:
            user.is_staff = True
            user.is_superuser = True
            user.save()
            AdminProfile.objects.create(user=user)
        return user

class PetForm(forms.ModelForm):
    class Meta:
        model = Pet
        fields = ['name', 'species', 'breed', 'color', 'age', 'gender', 'status', 
                 'location', 'description', 'contact_email', 'contact_phone', 'image']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'age': forms.TextInput(attrs={'placeholder': 'e.g., 2 years, 6 months, Puppy'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make contact info required for certain statuses
        if self.instance and self.instance.status in ['lost', 'found']:
            self.fields['contact_email'].required = True
            self.fields['contact_phone'].required = True

class CustomPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(
        max_length=254,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your email address',
            'autocomplete': 'email'
        })
    )

class CustomSetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(
        label="New password",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter new password',
            'autocomplete': 'new-password'
        }),
        strip=False,
    )
    new_password2 = forms.CharField(
        label="Confirm new password",
        strip=False,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirm new password',
            'autocomplete': 'new-password'
        }),
    )

class PetRegistrationRequestForm(forms.ModelForm):
    class Meta:
        model = PetRegistrationRequest
        fields = [
            'name', 'species', 'breed', 'color', 'age', 'gender', 
            'pet_status', 'location', 'description', 'contact_email', 
            'contact_phone', 'image'
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Pet name'}),
            'species': forms.Select(attrs={'class': 'form-control'}),
            'breed': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Breed (optional)'}),
            'color': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Color (optional)'}),
            'age': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., 2 years, 6 months, Puppy'}),
            'gender': forms.Select(attrs={'class': 'form-control'}),
            'pet_status': forms.Select(attrs={'class': 'form-control'}),
            'location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'City, State/Province'}),
            'description': forms.Textarea(attrs={
                'class': 'form-control', 
                'rows': 4, 
                'placeholder': 'Describe the pet, any special needs, behavior, etc.'
            }),
            'contact_email': forms.EmailInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Contact email (optional - will use your account email if blank)'
            }),
            'contact_phone': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Contact phone (optional)'
            }),
            'image': forms.FileInput(attrs={'class': 'form-control-file'})
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make contact_email show user's email as placeholder if available
        if hasattr(self, 'instance') and hasattr(self.instance, 'user') and self.instance.user:
            self.fields['contact_email'].widget.attrs['placeholder'] = f'Leave blank to use: {self.instance.user.email}'
