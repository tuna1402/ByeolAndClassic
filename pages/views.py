from django.shortcuts import render


def home(request):
    return render(request, "pages/home.html")


def greeting(request):
    return render(request, "pages/greeting.html")


def profile(request):
    return render(request, "pages/profile.html")


def awards(request):
    return render(request, "pages/awards.html")


def curriculum(request):
    return render(request, "pages/curriculum.html")


def accompanist(request):
    return render(request, "pages/accompanist.html")


def soloist(request):
    return render(request, "pages/soloist.html")


def masterclass(request):
    return render(request, "pages/masterclass.html")
