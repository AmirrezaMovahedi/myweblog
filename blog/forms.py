from django import forms
from django.utils import timezone

from .models import Comment, User, Post, Account


class TicketForm(forms.Form):
    SUBJECT_CHOICES = (
        ('پیشنهاد', 'پیشنهاد'),
        ('انتقاد', 'انتقاد'),
        ('گزارش', 'گزارش')
    )
    message = forms.CharField(widget=forms.Textarea())
    name = forms.CharField(max_length=50, required=True)
    phone = forms.CharField(max_length=11, required=True)
    email = forms.EmailField()
    subject = forms.ChoiceField(choices=SUBJECT_CHOICES, required=True)

    def clean_phone(self):
        phone = self.cleaned_data['phone']
        if phone:
            if not phone.isnumeric():
                raise forms.ValidationError('شماره درست وارد نشده است ')
            else:
                return phone


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['name', 'message']

    def clean_name(self):
        name = self.cleaned_data['name']
        if name:
            if name.isnumeric():
                raise forms.ValidationError('نام درست وارد نشده است ')
            else:
                return name




class SearchFrom(forms.Form):
    query = forms.CharField()


class CreatePost(forms.ModelForm):
    image = forms.ImageField()

    class Meta:
        model = Post
        fields = ['title', 'description', 'category', 'reading_time']


# class User_Login(forms.Form):
#     username = forms.CharField(max_length=250, required=True)
#     password = forms.CharField(max_length=250, required=True, widget=forms.PasswordInput)


class UserRegister(forms.ModelForm):
    password = forms.CharField(max_length=20, widget=forms.PasswordInput)
    password2 = forms.CharField(max_length=20, widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'email']

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('The password does not match')
        else:
            return cd['password2']


class AccountForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ['photo', 'bio', 'birthday']


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
