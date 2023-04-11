from django.shortcuts import HttpResponse,render

# Create your views here.
def index(request):
    # return HttpResponse("<h1>Hello Wolrd!<h1>")
    hobby = ["singing", "game"]
    food = ["Kimchi Pancake", "giblets"]

    return render(request, 'week5_day2.html', {"my_hobby" : hobby, "my_food" : food })
