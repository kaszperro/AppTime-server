from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth import get_user_model

User = get_user_model()


class RegisterForm(forms.ModelForm):
    password1 = forms.CharField(label='Hasło', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Powtórz hasło', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = (
            'email',
            'name',
            'surname',
            'phone_number',
        )

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.error_messages['required'] = 'Pole jest wymagane'

    def clean_email(self):
        email = self.cleaned_data.get('email')
        qs = User.objects.filter(email=email)
        if qs.exists():
            raise forms.ValidationError("Email jest zajęty")
        return email

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Hasła się nie zgadzają")
        return password2

    def save(self, commit=True):
        # user = super().save(commit=False)
        user = User.objects.create_user(
            self.cleaned_data["email"],
            self.cleaned_data["name"],
            self.cleaned_data["surname"],
            self.cleaned_data["phone_number"],
            self.cleaned_data["password1"]
        )
        # user.set_password(self.cleaned_data["password1"])
        # if commit:
        #    user.save()
        return user
