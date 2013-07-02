from django.template.response import TemplateResponse
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
#from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.views.generic.edit import FormView
from django.conf import settings

from datetime import datetime, timedelta, date


from my_calendar.models import Event, Comment
from my_calendar.forms import LoginForm, SignupForm



def earlier_date(date1, date2):
    if date1 < date2:
        return date1
    else:
        return date2

def homepage(request): 
    if request.user.is_authenticated():
        upcoming_events = [event for event in request.user.events.all() if event.start_time - datetime.now() < timedelta(days=7)]
    # form = NewHaikuForm(request.POST or None)
    # if request.user.is_authenticated():
    #     form.user = request.user
    #     if form.is_valid():
    #         form.save()
        news = [comment for event in request.user.events.all() for comment in event.comments
                if comment.created > earlier_date((datetime.now() - timedelta(days=30)), request.user.last_login)]
    else:
        upcoming_events = []
        news = []
    return TemplateResponse(request, 'homepage.html', locals())


class LoginView(FormView):
    form_class = LoginForm
    template_name = 'login.html'
    success_url = '/'

    def valid_form(self, form):
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(self.request, user)
                return HttpResponseRedirect('/')
        else:
            return self.invalid_form()

    def invalid_form(self):
        return HttpResponseRedirect('/error_login/')

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        if form.is_valid():
            return self.valid_form(form)
        else:
            return self.invalid_form()


class SignupView(FormView):
    form_class = SignupForm
    template_name = 'registration.html'

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        if form.is_valid():
            return self.save(form)
        else:
            return self.invalid_form()

    def save(self, form):
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = User.objects.create_user(username=form.cleaned_data['username'],
                                         password=form.cleaned_data['password'],
                                         email=form.cleaned_data['email'])
        if 'first_name' in form.cleaned_data:
            user.first_name = form.cleaned_data['first_name']
        if 'last_name' in form.cleaned_data:
            user.last_name = form.cleaned_data['last_name']
        user.save()
        #success_url = '/' + user.username + '/'
        return HttpResponseRedirect('/')

    def invalid_form(self):
        return HttpResponseRedirect('/error_registration/')
