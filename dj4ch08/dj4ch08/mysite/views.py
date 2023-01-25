from django.shortcuts import render, redirect
from mysite import models, forms
from django.core.mail import EmailMessage
import json, urllib
from django.conf import settings
import pymongo

def index(request):
    posts = models.Post.objects.filter(enabled=True).order_by('-pub_time')[:30]
    moods = models.Mood.objects.all()
    try:
        user_id = request.GET['user_id']
        user_pass = request.GET['user_pass']
        user_post = request.GET['user_post']
        user_mood = request.GET['mood']
    except:
        user_id = None
        message = '如要張貼訊息，則每一個欄位都要填...'

    if user_id != None:
        mood = models.Mood.objects.get(status=user_mood)
        post = models.Post(mood=mood, nickname=user_id, del_pass=user_pass, message=user_post)
        post.save()
        message='成功儲存！請記得你的編輯密碼[{}]!，訊息需經審查後才會顯示。'.format(user_pass)
    return render(request, 'index.html', locals())

def delpost(request, pid=None, del_pass=None):
    if del_pass and pid:
        try:
            post = models.Post.objects.get(id=pid)
            if post.del_pass == del_pass:
                post.delete()
        except:
            pass
    return redirect('/')

def listing(request):
    posts = models.Post.objects.filter(enabled=True).order_by('-pub_time')[:150]
    moods = models.Mood.objects.all()
    return render(request, 'listing.html', locals())

def posting(request):
    moods = models.Mood.objects.all()
    message = '如要張貼訊息，則每一個欄位都要填...'
    if request.method=='POST':
        user_id = request.POST.get('user_id')
        user_pass = request.POST.get('user_pass')
        user_post = request.POST.get('user_post')
        user_mood = request.POST.get('mood')
        if user_id != None:
            mood = models.Mood.objects.get(status=user_mood)
            post = models.Post(mood=mood, nickname=user_id, del_pass=user_pass, message=user_post)
            post.save()
            return redirect("/list/")
    return render(request, "posting.html", locals())

def contact(request):
    if request.method == 'POST':
        form = forms.ContactForm(request.POST)
        if form.is_valid():
            message = "感謝您的來信，我們會儘速處理您的寶貴意見。"
            user_name = form.cleaned_data['user_name']
            user_city = form.cleaned_data['user_city']
            user_school = form.cleaned_data['user_school']
            user_email  = form.cleaned_data['user_email']
            user_message = form.cleaned_data['user_message']

            mail_body = u'''
網友姓名：{}
居住城市：{}
是否在學：{}
電子郵件：{}
反應意見：如下
{}'''.format(user_name, user_city, user_school, user_email, user_message)

            email = EmailMessage(   '來自【不吐不快】網站的網友意見', 
                                    mail_body, 
                                    user_email,
                                    ['skynet.tw@gmail.com'])
            email.send()
        else:
            message = "請檢查您輸入的資訊是否正確！"
    else:
        form = forms.ContactForm()
    return render(request, 'contact.html', locals())

def post2db(request):
    if request.method == 'POST':
        post_form = forms.PostForm(request.POST)
        if post_form.is_valid():
            recaptcha_response = request.POST.get('g-recaptcha-response')
            url = 'https://www.google.com/recaptcha/api/siteverify'
            values = {
                'secret': settings.GOOGLE_RECAPTCHA_SECRET_KEY,
                'response': recaptcha_response
            }
            data = urllib.parse.urlencode(values).encode()
            req =  urllib.request.Request(url, data=data)
            response = urllib.request.urlopen(req)
            result = json.loads(response.read().decode())
            if result['success']:
                post_form.save()
                return redirect('/list/')
    else:
        post_form = forms.PostForm()
        message = '如要張貼訊息，則每一個欄位都要填...'          
    return render(request, 'post2db.html', locals())

def bmi(request):
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    collections = client["ch08mdb"]["bodyinfo"]
    if request.method=="POST":
        name = request.POST.get("name").strip()
        height = request.POST.get("height").strip()
        weight = request.POST.get("weight").strip()
        collections.insert_one({
            "name": name,
            "height": height,
            "weight": weight
        })
        return redirect("/bmi/")
    else:
        records = collections.find()
        data = list()
        for rec in records:
            t = dict()
            t['name'] = rec['name']
            t['height'] = rec['height']
            t['weight'] = rec['weight']
            t['bmi'] = round(float(t['weight'])/(int(t['height'])/100)**2, 2)
            data.append(t)

    return render(request, "bmi.html", locals())