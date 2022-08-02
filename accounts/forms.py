from django import  forms
from .models import User,Department, Profile


# Staff Registration form
class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Enter Password',
        'class': 'form-control',
    }))

    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Confirm Password'
    }))

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'phone_number', 'email', 'department','password']

    # adding classes and placeholder /
    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs['placeholder'] = 'Enter First Name'
        self.fields['last_name'].widget.attrs['placeholder'] = 'Enter last Name'
        self.fields['phone_number'].widget.attrs['placeholder'] = 'Enter Phone Number'
        self.fields['email'].widget.attrs['placeholder'] = 'Enter Email Address'
        self.fields['department'].widget.attrs['placeholder'] = 'Choose Department'
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'

    def clean(self):
        cleaned_data = super(RegistrationForm, self).clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:
            raise forms.ValidationError(
                "Password does not match!"
            )    

class UserProfileForm(forms.ModelForm):
    profile_picture = forms.ImageField(required=False, error_messages = {'Invalid':("Image files only")}, widget=forms.FileInput)
    class Meta:
        model = Profile
        fields = ( 'profile_pics',)

    # def __init__(self, *args, **kwargs):
    #     super(UserProfileForm, self).__init__(*args, **kwargs)
    #     for field in self.fields:
    #         self.fields[field].widget.attrs['class'] = 'form-control'            
            

# Login Form
class LoginForm(forms.Form):
    email = forms.EmailField(required=True,widget=forms.TextInput(attrs={'type':'email','class':'form-control','placeholder':'email'}))        
    password = forms.CharField(widget=forms.TextInput(attrs={'type':'password','class':'form-control','placeholder':'Password'})) 
    