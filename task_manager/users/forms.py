# users/forms.py
from django import forms
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.forms import UserCreationForm

class BaseUserForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name in ['first_name', 'last_name', 'username']:
            self.fields[field_name].required = True
            self.fields[field_name].widget.attrs['required'] = 'required'

        for field_name, field in self.fields.items():
            css_class = field.widget.attrs.get('class', 'form-control')
            if self.is_bound:
                if self.errors.get(field_name):
                    css_class += ' is-invalid'
                else:
                    css_class += ' is-valid'
            field.widget.attrs['class'] = css_class

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username')

        labels = {
            'first_name': _('First Name'),
            'last_name': _('Last Name'),
            'username': _('Username'),
        }

        help_texts = {
            'username': _(
                '''Required field. No more than 150 characters. Only letters, numbers and symbols @/./+/-/_.'''
            ),
        }

        widgets = {
            'username': forms.TextInput(attrs={'placeholder': _('Username')}),
            'first_name': forms.TextInput(attrs={'placeholder': _('First name')}),
            'last_name': forms.TextInput(attrs={'placeholder': _('Last name')}),
        }

class CustomUserCreateForm(UserCreationForm, BaseUserForm):
    password1 = forms.CharField(
        label=_("Password"),
        widget=forms.PasswordInput(attrs={'placeholder': _('Password'), 'class': 'form-control'}),
        help_text=_("Your password must contain at least 3 characters."),
    )

    password2 = forms.CharField(
        label=_("Password confirmation"),
        widget=forms.PasswordInput(attrs={
            'label': _('Confirm Password'),
            'placeholder': _('Confirm password'),
            'class': 'form-control'
        }),
        help_text=_("Please enter the password again to confirm."),
    )

    class Meta(BaseUserForm.Meta):
        model = User
        fields = BaseUserForm.Meta.fields + ('password1', 'password2',)

class CustomUserUpdateForm(BaseUserForm):
    password1 = forms.CharField(
        label=_("New password"),
        widget=forms.PasswordInput(attrs={'placeholder': _('New password'), 'class': 'form-control'}),
        required=False
    )
    password2 = forms.CharField(
        label=_("Confirm password"),
        widget=forms.PasswordInput(attrs={'placeholder': _('Confirm password'), 'class': 'form-control'}),
        required=False
    )

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 or password2:
            if password1 != password2:
                self.add_error('password2', _("Passwords do not match"))
            elif len(password1) < 3:
                self.add_error('password1', _("Password must be at least 3 characters"))
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        password = self.cleaned_data.get('password1')
        if password:
            user.password = make_password(password)
        if commit:
            user.save()
        return user

    def clean_username(self):
        username = self.cleaned_data['username']
        qs = User.objects.filter(username=username).exclude(pk=self.instance.pk)
        if qs.exists():
            raise forms.ValidationError(_("A user with that username already exists."))
        return username