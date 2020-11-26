from django import forms
from django.contrib import messages
from django.contrib.auth import get_user_model, authenticate, login

User = get_user_model()


class UserLoginForm(forms.Form):
    email = forms.EmailField(max_length=32)
    password = forms.CharField(widget=forms.PasswordInput)

    def __init__(self, request, *args, **kwargs):
        self.request = request
        super(UserLoginForm, self).__init__(*args, **kwargs)

    def clean(self):
        data = self.cleaned_data
        email = data.get('email')
        password = data.get('password')
        qs = User.objects.filter(email=email)
        if qs.exists():
            # user email is registered, check email is active or email activation
            not_active = qs.filter(is_active=False)
            if not_active.exists():
                msg = messages.error(self.request,"User is Inactive")

        user = authenticate(self.request, email=email, password=password)
        if user is None:
            msg = messages.error(self.request, "Invalid credentials.")
            raise forms.ValidationError(msg)
        login(self.request, user)
        return data


class UserRegistrationForm(forms.ModelForm):
    email = forms.EmailField(label='Email Address')
    phone = forms.CharField(max_length=14, min_length=11, label='Phone Number')
    password1 = forms.CharField(max_length=32, label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(max_length=32, label='Password Confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
            'email',
            'phone'
        )

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Password Don't match!")
        return password2

    def save(self, commit=True):
        user = super(UserRegistrationForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        user.is_active = True
        user.save()
        return user
