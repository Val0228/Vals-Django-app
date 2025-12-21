from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from users.models import Profile

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(label='Email address', help_text='You SHU email address.')
    first_name = forms.CharField(max_length=30, required=True, label='First Name')
    last_name = forms.CharField(max_length=30, required=True, label='Last Name')
    
    # Student profile fields
    date_of_birth = forms.DateField(
        required=True,
        label='Date of Birth',
        help_text='Format: YYYY-MM-DD',
        widget=forms.DateInput(attrs={'type': 'date'})
    )
    address = forms.CharField(max_length=255, required=True, label='Address')
    city = forms.CharField(max_length=100, required=True, label='City/Town')
    country = forms.CharField(max_length=100, required=True, label='Country')
    image = forms.ImageField(required=False, label='Profile Photo')

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            # Create or update profile with student information
            profile, created = Profile.objects.get_or_create(user=user)
            profile.date_of_birth = self.cleaned_data.get('date_of_birth')
            profile.address = self.cleaned_data.get('address')
            profile.city = self.cleaned_data.get('city')
            profile.country = self.cleaned_data.get('country')
            if self.cleaned_data.get('image'):
                profile.image = self.cleaned_data.get('image')
            profile.save()
        return user

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

class ProfileUpdateForm(forms.ModelForm):
    date_of_birth = forms.DateField(
        required=False,
        label='Date of Birth',
        widget=forms.DateInput(attrs={'type': 'date'})
    )
    
    class Meta:
        model = Profile
        fields = ['date_of_birth', 'address', 'city', 'country', 'image']
