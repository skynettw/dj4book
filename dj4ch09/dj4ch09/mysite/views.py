from django.shortcuts import render, redirect
from django.contrib.sessions.models import Session
from mysite import models, forms
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib import auth
from django.contrib.auth.decorators import login_required

# for 9.2
# def index(request):
#     if 'username' in request.session and request.session['username'] != None:
#         username = request.session['username']
#         useremail = request.session['useremail']
#     return render(request, 'index.html', locals())

# for 9.2
# def login(request):
#     if request.method == 'POST':
#         login_form = forms.LoginForm(request.POST)
#         if login_form.is_valid():
#             login_name=request.POST['username'].strip()
#             login_password=request.POST['password']
#             try:
#                 user = models.User.objects.get(name=login_name)
#                 if user.password == login_password:
#                     request.session['username'] = user.name
#                     request.session['useremail'] = user.email
#                     messages.add_message(request, messages.SUCCESS, '成功登入了')
#                     return redirect('/')
#                 else:
#                     messages.add_message(request, messages.WARNING, '密碼錯誤，請再檢查一次')
#             except:
#                 messages.add_message(request, messages.WARNING, '找不到使用者')
#         else:
#             messages.add_message(request, messages.INFO,'請檢查輸入的欄位內容')
#     else:
#         login_form = forms.LoginForm()

#     return render(request, 'login.html', locals())

# for 9.3
# def index(request):
#     if request.user.is_authenticated:
#         username = request.user.username
#     messages.get_messages(request)
#     return render(request, 'index.html', locals())

# for 9.3.3
def index(request):
    if request.user.is_authenticated:
        username = request.user.username
        useremail = request.user.email
        try:
            user = User.objects.get(username=username)
            diaries = models.Diary.objects.filter(user=user).order_by('-ddate')
        except Exception as e:
            print(e)
            pass
    messages.get_messages(request)
    return render(request, 'index.html', locals())

# for 9.3
def login(request):
    if request.method == 'POST':
        login_form = forms.LoginForm(request.POST)
        if login_form.is_valid():
            login_name=request.POST['username'].strip()
            login_password=request.POST['password']
            user = authenticate(username=login_name, password=login_password)
            if user is not None:
                if user.is_active:
                    auth.login(request, user)
                    messages.add_message(request, messages.SUCCESS, '成功登入了')
                    return redirect('/')
                else:
                    messages.add_message(request, messages.WARNING, '帳號尚未啟用')
            else:
                messages.add_message(request, messages.WARNING, '登入失敗')
        else:
            messages.add_message(request, messages.INFO,'請檢查輸入的欄位內容')
    else:
        login_form = forms.LoginForm()
    return render(request, 'login.html', locals())


# for 9.2
# def logout(request):
#     if 'username' in request.session:
#         Session.objects.all().delete()
#         return redirect('/login/')
#     return redirect("/")

# for 9.2
# def userinfo(request):
#     if 'username' in request.session:
#         username = request.session['username']
#     else:
#         return redirect('/login/')
#     try:
#         userinfo = models.User.objects.get(name=username)
#     except:
#         pass
#     return render(request, 'userinfo.html', locals())

# for 9.3
def logout(request):
    auth.logout(request)
    messages.add_message(request, messages.INFO, "成功登出了")
    return redirect('/')

#for 9.3
# @login_required(login_url='/login/')
# def userinfo(request):
#     if request.user.is_authenticated:
#         username = request.user.username
#         try:
#             userinfo = User.objects.get(username=username)
#         except:
#             pass
#     return render(request, 'userinfo.html', locals())

# for 9.3.2

@login_required(login_url='/login/')
def userinfo(request):
    if request.user.is_authenticated:
        username = request.user.username
        try:
            user = User.objects.get(username=username)
            userinfo = models.Profile.objects.get(user=user)
        except:
            pass
    return render(request, "userinfo.html", locals())

@login_required(login_url='/login/')
def posting(request):
    if request.user.is_authenticated:
        username = request.user.username
        useremail = request.user.email
    messages.get_messages(request)
        
    if request.method == 'POST':
        user = User.objects.get(username=username)
        diary = models.Diary(user=user)
        post_form = forms.DiaryForm(request.POST, instance=diary)
        if post_form.is_valid():
            messages.add_message(request, messages.INFO, "日記已儲存")
            post_form.save()  
            return redirect('/')
        else:
            messages.add_message(request, messages.INFO, '要張貼日記，每一個欄位都要填...')
    else:
        post_form = forms.DiaryForm()
        messages.add_message(request, messages.INFO, '要張貼日記，每一個欄位都要填...')
    return render(request, "posting.html", locals())

def votes(request):
    data = models.Vote.objects.all()
    return render(request, "votes.html", locals())