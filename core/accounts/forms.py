from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError
from accounts.models import Users

# Form creation configuration and rewrite base aof django auth form


class UserCreationForm(forms.ModelForm):
    """
    Form for user creation
    with parent database model Users
    """

    password1 = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(
        label="Password confirmation", widget=forms.PasswordInput
    )

    class Meta:
        model = Users
        fields = ("email", "password1", "password2")

    def clean_password2(self):
        # Check that the two passwords are equal
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("The two password fields didn't match.")
        return password2

    def save(self, commit=True):
        # Save definition for database
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    disabled password hash display field.
    """

    password = ReadOnlyPasswordHashField()

    class Meta:
        model = Users
        fields = (
            "email",
            "password",
            "is_staff",
            "is_active",
            "is_superuser",
        )
