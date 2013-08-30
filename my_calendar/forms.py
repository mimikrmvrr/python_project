from django import forms
from django.contrib.auth.models import User
from django.forms.extras.widgets import SelectDateWidget
from django.forms.widgets import SplitDateTimeWidget
from django.contrib.admin import widgets
from datetime import datetime, date
from calendar import HTMLCalendar
from itertools import groupby

class LoginForm(forms.Form):
    username = forms.CharField(label='username')
    password = forms.CharField(widget=forms.PasswordInput, label='password')


class PostCommentForm(forms.Form):
    text = forms.CharField(widget=forms.Textarea, label='Comment')

    def clean(self):
        return self.cleaned_data


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
    location = forms.CharField(label="Where?", required=False)  
    description = forms.CharField(label="Add more info", widget=forms.Textarea, required=False)
    group = forms.CharField(label='Group:', required=False)
    
    def clean(self):
        return self.cleaned_data


class CreateGroupForm(forms.Form):
    name = forms.CharField(label="Name:")
    users = forms.CharField(label='Members:', required=False)
    
    def clean(self):
        return self.cleaned_data

    def clean_name(self):
        if not self.cleaned_data['name']:
            raise forms.ValidationError("Please add the name of the group.")


class CalendarForm(HTMLCalendar):

    def __init__(self, events):
        super(CalendarFrom, self).__init__()
        self.events = self.group_by_day(events)

    def formatday(self, day, weekday):
        if day != 0:
            cssclass = self.cssclass[weekday]
            if date.today() == date(self.year, self.month, day):
                cssclass += ' today'
            if day in self.events:
                cssclass += ' filled'
                body = ['<ul>']
                for event in self.events[day]:
                    body.append('<li>')
                    body.append('<a href="/events/%s/">' % event.id)
                    body.append('%s' % event.title)
                    body.append('</a></li>')
                body.append("</ul>")
                return self.day_cell(cssclass, '%d %s' % (day, ''.join(body)))
            return self.day_cell(cssclass, day)
        return self.day_cell('noday', '&nbsp;')

    def formatmonth(self, year, month):
        self.year, self.month = year, month
        return super(CalendarForm, self).formatmonth(year, month)

    def group_by_day(self, events):
        time = lambda event: event.start_time
        return dict([(day, list(events)) for day, events in groupby(event, time)])

    def day_cell(self, cssclass, body):
        return '<td class="%s">%s</td>' % (cssclass, body)
