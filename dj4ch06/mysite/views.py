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
