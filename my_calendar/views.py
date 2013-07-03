from django.template.response import TemplateResponse
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
#from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.views.generic.edit import FormView
from django.conf import settings
from django.utils.timezone import utc
from datetime import datetime, timedelta, date
# from pytz import timezone
# import pytz


from my_calendar.models import Event, Comment
from my_calendar.forms import LoginForm, SignupForm, CreateEventForm



def earlier_date(date1, date2):
    if date1 < date2:
        return date1
    else:
        return date2


def homepage(request): 
    if request.user.is_authenticated():
        now = datetime.utcnow().replace(tzinfo=utc)
        upcoming_events = [event for event in request.user.events.all() if event.start_time - now < timedelta(days=7)]
    # form = NewHaikuForm(request.POST or None)
    # if request.user.is_authenticated():
    #     form.user = request.user
    #     if form.is_valid():
    #         form.save()
        news = [comment for event in request.user.events.all() for comment in event.comments.all()
                if comment.created > earlier_date((now - timedelta(days=30)), request.user.last_login)]
    else:
        upcoming_events = []
        news = []
    return TemplateResponse(request, 'homepage.html', locals())


def event(request):
    return TemplateResponse(request, 'event.html', locals())


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
        user = User.objects.create_user(username=username,
                                         password=password,
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


class CreateEventView(FormView):
    form_class = CreateEventForm
    template_name = 'create_event.html'

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        if form.is_valid():
            return self.valid_form(form, request)
        else:
            return self.invalid_form() 

    def invalid_form(self):
        return HttpResponseRedirect('/error_event/')

    def valid_form(self, form, request):
        # start_time = form.cleaned_data['start_time']
        # title = form.cleaned_data['title']
        event = Event.objects.create(creator=request.user, 
                                     start_time=form.cleaned_data['start_time'],
                                     end_time=form.cleaned_data['end_time'])
        event.people.add(request.user)
        for attribute in form.cleaned_data:
            if attribute not in ['group', 'start_time', 'end_time']:
                setattr(event, attribute, form.cleaned_data[attribute])
        # if 'description' in form.cleaned_data:
        #     event.description = form.cleaned_data['description']
        # if 'group' in form.cleaned_data:
        #     event.groups.add(form.cleaned_data['group'])
        # if 'end_time' in form.cleaned_data:
        #     event.end_time = form.cleaned_data['end_time']
        # if 'location' in form.cleaned_data:
        #     event.location = form.cleaned_data['location']
        event.save()
        comment = Comment.objects.create(text='I created this event.',
                                      creator=request.user,
                                      event=event)
        #event.comment_set.add(comment)
        return HttpResponseRedirect('/event' + str(event.id) + '/')


