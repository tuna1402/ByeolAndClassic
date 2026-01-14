from django.shortcuts import render

from .models import PageContent, PageKey


def home(request):
    return render(request, "pages/home.html")


def greeting(request):
    page = PageContent.objects.filter(key=PageKey.GREETING).first()
    return render(request, "pages/greeting.html", {"page": page})


def profile(request):
    page = PageContent.objects.filter(key=PageKey.PROFILE).first()
    return render(request, "pages/profile.html", {"page": page})


def awards(request):
    page = PageContent.objects.filter(key=PageKey.AWARDS).first()
    return render(request, "pages/awards.html", {"page": page})


def curriculum(request):
    page = PageContent.objects.filter(key=PageKey.CURRICULUM).first()
    return render(request, "pages/curriculum.html", {"page": page})


def accompanist(request):
    page = PageContent.objects.filter(key=PageKey.ACCOMPANIST).first()
    return render(request, "pages/accompanist.html", {"page": page})


def soloist(request):
    page = PageContent.objects.filter(key=PageKey.SOLOIST).first()
    return render(request, "pages/soloist.html", {"page": page})


def masterclass(request):
    page = PageContent.objects.filter(key=PageKey.MASTERCLASS).first()
    return render(request, "pages/masterclass.html", {"page": page})
