from django.shortcuts import render
from datetime import datetime

def index(request, tvno = 0):
    tv_list = [{'name':'中天', 'tvcode':'_QbRXRnHMVY'},
        {'name':'華視', 'tvcode':'wM0g8EoUZ_E'},
        {'name':'民視', 'tvcode':'ylYJSBUgaMA'},
        {'name':'中視', 'tvcode':'TCnaIE_SAtM'},]
    now = datetime.now()
    hour = now.timetuple().tm_hour
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

def carlist(request, maker=0):
    car_maker = ['SAAB', 'Ford', 'Honda', 'Mazda', 'Nissan','Toyota' ]
    car_list = [ [],
            ['Fiesta', 'Focus', 'Modeo', 'EcoSport', 'Kuga', 'Mustang'],
            ['Fit', 'Odyssey', 'CR-V', 'City', 'NSX'],
            ['Mazda3', 'Mazda5', 'Mazda6', 'CX-3', 'CX-5', 'MX-5'],
            ['Tida', 'March', 'Livina', 'Sentra', 'Teana', 'X-Trail', 'Juke', 'Murano'],
            ['Camry','Altis','Yaris','86','Prius','Vios', 'RAV4', 'Wish']
              ]
    maker = maker
    maker_name =  car_maker[maker]
    cars = car_list[maker]
    return render(request, 'carlist.html', locals())
    
def carprice(request, maker=0):
    car_maker = ['Ford', 'Honda', 'Mazda']
    car_list = [[   {'model':'Fiesta', 'price': 203500}, 
                    {'model':'Focus','price': 605000}, 
                    {'model':'Mustang','price': 900000}],
                [   {'model':'Fit', 'price': 450000}, 
                    {'model':'City', 'price': 150000}, 
                    {'model':'NSX', 'price':1200000}],
                [   {'model':'Mazda3', 'price': 329999}, 
                    {'model':'Mazda5', 'price': 603000},
                    {'model':'Mazda6', 'price':850000}],
              ]
    maker = maker
    maker_name =  car_maker[maker]
    cars = car_list[maker]
    return render(request, 'carprice.html', locals())

