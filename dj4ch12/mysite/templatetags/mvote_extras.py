from django import template
from mysite import models

register = template.Library()

@register.filter(name='show_items')
def show_items(value):
    try:
        poll = models.Poll.objects.get(id=int(value))
        items = models.PollItem.objects.filter(poll=poll).count()
    except:
        items = 0
    return items

@register.filter(name='show_votes')
def show_votes(value):
    try:
        poll = models.Poll.objects.get(id=int(value))
        votes = 0
        pollitems = models.PollItem.objects.filter(poll=poll)
        for pollitem in pollitems:
            votes = votes + pollitem.vote
    except:
        votes = 0
    return votes
