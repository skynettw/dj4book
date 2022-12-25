from django.shortcuts import render
from datetime import datetime

def index(request, tvno = 0):
    tv_list = [{'name':'中天', 'tvcode':'_QbRXRnHMVY'},
        {'name':'華視', 'tvcode':'wM0g8EoUZ_E'},
        {'name':'民視', 'tvcode':'ylYJSBUgaMA'},
        {'name':'中視', 'tvcode':'TCnaIE_SAtM'},]
    now = datetime.now()
    tv = tv_list[tvno]
    return render(request, 'index.html', locals())

def engtv(request, tvno='0'):
    tv_list = [{'name':'SkyNews', 'tvcode':'9Auq9mYxFEE'},
            {'name':'Euro News', 'tvcode':'pykpO5kQJ98'},
            {'name':'India News', 'tvcode':'Xmm3Kr5P1Uw'},
            {'name':'CNA News', 'tvcode':'XWq5kBlakcQ'},]

    now = datetime.now()
    tvno = tvno
    tv = tv_list[int(tvno)]
    return render(request, 'engtv.html', locals())

