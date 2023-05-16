from django.shortcuts import render
from django.http import HttpResponse

def homepage(request):
    return render(request, "index.html")

def about(request, author_no=0):
    html = "<h2>Here is Author:{}'s about page!</h2><hr>".format(author_no)
    return HttpResponse(html)

def listing(request, yr, mon, day):
    html = "<h2>List Date is {}/{}/{}</h2><hr>".format(yr, mon, day)
    return HttpResponse(html)


def post(request, yr, mon, day, post_num):
    html = "<h2>{}/{}/{}:Post Number:{}</h2><hr>".format(yr, mon, day, post_num)
    return HttpResponse(html)

def company(request):
    return HttpResponse("Company page!")

def sales(request):
    return HttpResponse("Sales page!")

def contact(request):
    return HttpResponse("Contact page!")
