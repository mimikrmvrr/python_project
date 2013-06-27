from django.template.response import TemplateResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from datetime import datetime, timedelta, date

from my_calendar.models import Event, Comment
#from haikus.forms import NewHaikuForm


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
        news = [comment for comment in event.comments for event in request.user.events.all() 
                if comment.created > earlier_date((datetime.now() - timedelta(days=30)), request.user.last_login)]
    else:
        upcoming_events = []
        news = []
    return TemplateResponse(request, 'homepage.html', locals())

