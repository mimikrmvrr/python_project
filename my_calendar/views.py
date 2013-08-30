from django.template.response import TemplateResponse
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User, Group
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.views.generic.edit import FormView
from django.conf import settings
from django.utils.timezone import utc
from datetime import datetime, timedelta, date
from django.views.decorators.http import require_http_methods
from itertools import groupby
from my_calendar.models import Event, Comment
from my_calendar.forms import LoginForm, SignupForm, CreateEventForm, CreateGroupForm, PostCommentForm


def earlier_date(date1, date2):
    if date1 < date2:
        return date1
    else:
        return date2


def homepage(request): 
    if request.user.is_authenticated():
        now = datetime.utcnow().replace(tzinfo=utc)
        upcoming_events = [event for event in request.user.events.all() if event.start_time - now < timedelta(days=7)]
        news = [comment for event in request.user.events.all() for comment in event.comments.all()
                if comment.created > earlier_date((now - timedelta(days=30)), request.user.last_login)]
    else:
        upcoming_events = []
        news = []
    news.reverse()
    return TemplateResponse(request, 'homepage.html', locals())


def eventpage(request, id):
    events = Event.objects.filter(id=id)
    event = events[0]
    comments = event.comments.all()
    return TemplateResponse(request, 'event.html', locals())


def eventslist(request):
        if request.user.is_authenticated():
            now = datetime.utcnow().replace(tzinfo=utc)
            events = [event for event in request.user.events.all() if event.start_time - now < timedelta(days=30)]
        else:
            events = []
        time_function = lambda event: event.start_time
        events_by_date = dict((day, list(events)) for day, events in groupby(events, time_function))
        dates = events_by_date.keys()
        events_lists_by_dates = [events_by_date[date] for date in dates]
        return TemplateResponse(request, 'eventslist.html', locals())


def groups(request):
    groupslist = request.user.groups.all()
    return TemplateResponse(request, 'groupslist.html', locals())


def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/')


class PostCommentView(FormView):
    form_class = PostCommentForm
    template_name = 'event.html'

    @require_http_methods("GET")
    def get(self, request, id):
        return eventpage(request, id)

    def valid_form(self, form, request):
        now = datetime.utcnow().replace(tzinfo=utc)
        event = request.user.events.filter(id=id)[0]
        comment = Comment.objects.create(text=form.cleaned_data['text'],
                                         creator=request.user,
                                         created=now)
        comment.event.add(event)
        comment.save()
        return HttpResponseRedirect(request.path)

    @require_http_methods("POSТ")
    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        if form.is_valid():
            return self.valid_form(form, request)
        else:
            return self.invalid_form(request)

    def invalid_form(self, request):
        return HttpResponseRedirect(request.path)


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
            return self.save(form, request)
        else:
            return self.invalid_form()

    def save(self, form, request):
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
        user = authenticate(username=request.POST['username'],
                            password=request.POST['password'])
        login(request, user)
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
        event = Event.objects.create(creator=request.user, 
                                     start_time=form.cleaned_data['start_time'],
                                     end_time=form.cleaned_data['end_time'])
        event.people.add(request.user)
        for attribute in form.cleaned_data:
            if attribute not in ['group', 'start_time', 'end_time']:
                setattr(event, attribute, form.cleaned_data[attribute])
        if 'group' in form.cleaned_data:
            for group in request.user.groups.filter(name=form.cleaned_data['group']):
                event.groups.add(group)
                for user in group.user_set.all():
                    event.people.add(user)
        event.save()
        comment = Comment.objects.create(text='I created this event.',
                                      creator=request.user,
                                      event=event)
        event.comment_set.add(comment)
        event.save()
        return HttpResponseRedirect('/events/' + str(event.id) + '/')


class CreateGroupView(FormView):
    form_class = CreateGroupForm
    template_name = 'create_group.html'

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        if form.is_valid():
            return self.valid_form(form, request)
        else:
            return self.invalid_form() 

    def invalid_form(self):
        return HttpResponseRedirect('/error_group/')

    def valid_form(self, form, request):
        group = Group.objects.create(name=form.cleaned_data['name'])
        group.user_set.add(request.user)
        group.save()
        return HttpResponseRedirect('/groups/' + str(group.id) + '/')

