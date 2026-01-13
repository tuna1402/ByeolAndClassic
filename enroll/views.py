from django.shortcuts import render

from enroll.forms import EnrollApplicationForm
from enroll.models import EnrollApplication
from enroll.services import send_admin_notification


def form(request):
    success = False
    if request.method == "POST":
        form = EnrollApplicationForm(request.POST)
        if form.is_valid():
            cleaned = form.cleaned_data
            application = EnrollApplication.objects.create(
                name=cleaned["name"],
                phone=cleaned["phone"],
                birth_date=cleaned["birth_date"],
                residence=cleaned["residence"],
                purposes=cleaned["purposes"],
                preferred_date=cleaned["preferred_date"],
                message=cleaned["message"],
            )
            send_admin_notification(
                {
                    "name": application.name,
                    "phone": application.phone,
                    "birth_date": application.birth_date,
                    "residence": application.residence,
                    "purposes": application.purposes,
                    "preferred_date": application.preferred_date,
                    "message": application.message or "-",
                }
            )
            success = True
            form = EnrollApplicationForm()
    else:
        form = EnrollApplicationForm()

    return render(
        request,
        "enroll/form.html",
        {
            "form": form,
            "success": success,
        },
    )
