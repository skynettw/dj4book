#-*- coding: utf-8 -*-
from datetime import datetime
from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from allauth.account.decorators import verified_email_required
from mysite import models

# Create your views here.

def index(request):
    all_polls = models.Poll.objects.all().order_by('-created_at')
    paginator = Paginator(all_polls, 5)
    p = request.GET.get('p')

    try:
        polls = paginator.page(p)
    except PageNotAnInteger:
        polls = paginator.page(1)
    except EmptyPage:
        polls = paginator.page(paginator.num_pages)

    return render(request, 'index.html', locals())


@login_required
# @verified_email_required
def poll(request, pollid):
    try:
        poll = models.Poll.objects.get(id = pollid)
    except:
        poll = None
    if poll is not None:
        pollitems = models.PollItem.objects.filter(poll=poll).order_by('-vote')
    return render(request, 'poll.html', locals())

# @login_required
# def vote(request, pollid, pollitemid):
#     try:
#         pollitem = models.PollItem.objects.get(id = pollitemid)
#     except:
#         pollitem = None
#     if pollitem is not None:
#         pollitem.vote = pollitem.vote + 1
#         pollitem.save()
#     target_url = '/poll/{}'.format( pollid)
#     return redirect(target_url)

@login_required
def vote(request, pollid, pollitemid):
    target_url = '/poll/{}'.format( pollid)

    try:
        if models.VoteCheck.objects.filter(userid=request.user.id, pollid=pollid, vote_date = datetime.date.today()):
            return redirect(target_url)

        vote_rec = models.VoteCheck(userid=request.user.id, pollid=pollid, vote_date = datetime.date.today())
        vote_rec.save()

        pollitem = models.PollItem.objects.get(id = pollitemid)

        if pollitem is not None:
            pollitem.vote = pollitem.vote + 1
            pollitem.save()
    except:
        pollitem = None

    return redirect(target_url)

@login_required
def govote(request):
    try:
        is_ajax = request.headers.get('x-requested-with') == 'XMLHttpRequest'

        votes = 0

        if (request.method != "GET") or (not is_ajax):
            return HttpResponse(votes)

        pollid = request.GET.get('pollid')
        is_voted = models.VoteCheck.objects.filter(userid=request.user.id, pollid=pollid, vote_date = datetime.date.today())

        if (not is_voted):
            pollitemid = request.GET.get('pollitemid')
            pollitem = models.PollItem.objects.get(id=pollitemid)
            pollitem.vote = pollitem.vote + 1
            pollitem.save()
            votes = pollitem.vote

            vote_rec = models.VoteCheck(userid=request.user.id, pollid=pollid, vote_date = datetime.date.today())
            vote_rec.save()

        return HttpResponse(votes)
    except:
        votes = 0
        return HttpResponse(votes)


