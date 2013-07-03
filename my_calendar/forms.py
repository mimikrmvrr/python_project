from django import forms
from django.contrib.auth.models import User
from django.forms.extras.widgets import SelectDateWidget
from django.forms.widgets import SplitDateTimeWidget
from django.contrib.admin import widgets
from datetime import datetime, date

#from my_calendar.widgets import JqSplitDateTimeWidget, JqSplitDateTimeField

class LoginForm(forms.Form):
    username = forms.CharField(label='username')
    password = forms.CharField(widget=forms.PasswordInput, label='password')


class SignupForm(forms.Form):
    username = forms.CharField(label='Username:')
    first_name = forms.CharField(label='First name:')
    last_name = forms.CharField(label='Last name:')
    email = forms.EmailField(label='E-mail:')
    password = forms.CharField(widget=forms.PasswordInput, label='Password:')
    password_check = forms.CharField(widget=forms.PasswordInput, label='Confirm password:')

    def clean_username(self):
        try:
            user = User.objects.get(username=self.cleaned_data['username'])
        except User.DoesNotExist:
            return self.cleaned_data['username']
        raise forms.ValidationError("This username is already taken. Please choose another.")

    def clean(self):
        if 'password' in self.cleaned_data and 'password_check' in self.cleaned_data:
            if self.cleaned_data['password_check'] != self.cleaned_data['password']:
                raise forms.ValidationError("The passwords are different.")
        return self.cleaned_data


class CreateEventForm(forms.Form):
    title = forms.CharField(label="Name:")
    start_time = forms.DateTimeField(label='When?', widget=SelectDateWidget)
    end_time = forms.DateTimeField(label="End:", widget=SelectDateWidget)  
    location = forms.CharField(label="Where?")  
    description = forms.CharField(label="Add more info", widget=forms.Textarea)
    group = forms.CharField(label='Group:')
    
    def clean(self):
        # if self.cleaned_data['end_time'] and self.cleaned_data['start_time']:
        #     if self.cleaned_data['end_time'] < self.cleaned_data['start_time']:
        #         raise forms.ValidationError("The end must be after the begining.")
        return self.cleaned_data

    # def clean_start_time(self):
    #     if not self.cleaned_data['start_time']:
    #         raise forms.ValidationError("Please add when the start time of the event.")

    # def clean_title(self):
    #     if not self.cleaned_data['title']:
    #         raise forms.ValidationError("Please add the name of the event.")


# class MyTimeForm(forms.ModelForm):
#     class Meta:
#         model = MyTime

#     def __init__(self, *args, **kwargs):
#         super(MyTime, self).__init__(*args, **kwargs)
#         self.fields['date'].widget = widgets.AdminDateWidget()
#         self.fields['time'].widget = widgets.AdminTimeWidget()
#         self.fields['datetime'].widget = widgets.AdminSplitDateWidget()


# class SplitSelectDateTimeWidget(MultiWidget):
#     """
#     MultiWidget = A widget that is composed of multiple widgets.

#     This class combines SelectTimeWidget and SelectDateWidget so we have something 
#     like SpliteDateTimeWidget (in django.forms.widgets), but with Select elements.
#     """
#     def __init__(self, attrs=None, hour_step=None, minute_step=None, second_step=None, twelve_hr=None, years=None):
#         widgets = (SelectDateWidget(attrs=attrs, years=years), SelectTimeWidget(attrs=attrs, hour_step=hour_step, minute_step=minute_step, second_step=second_step, twelve_hr=twelve_hr))
#         super(SplitSelectDateTimeWidget, self).__init__(widgets, attrs)

#     def decompress(self, value):
#         if value:
#             return [value.date(), value.time().replace(microsecond=0)]
#         return [None, None]

#     def format_output(self, rendered_widgets):
#         """
#         Given a list of rendered widgets (as strings), it inserts an HTML
#         linebreak between them.
        
#         Returns a Unicode string representing the HTML for the whole lot.
#         """
#         rendered_widgets.insert(-1, '<br/>')
#         return u''.join(rendered_widgets)



