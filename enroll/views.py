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
                consultation_types=cleaned["consultation_types"],
                level_test_piece=cleaned["level_test_piece"],
                career_school=cleaned["career_school"],
                awards_history=cleaned["awards_history"],
                practice_time=cleaned["practice_time"],
                school_grade=cleaned["school_grade"],
                transcript_available=cleaned["transcript_available"],
                preferred_date=cleaned["preferred_date"],
                message=cleaned["message"],
            )
            send_admin_notification(
                {
                    "name": application.name,
                    "phone": application.phone,
                    "birth_date": application.birth_date,
                    "residence": application.residence,
                    "consultation_types": application.consultation_types,
                    "level_test_piece": application.level_test_piece or "-",
                    "career_school": application.career_school or "-",
                    "awards_history": application.awards_history or "-",
                    "practice_time": application.practice_time or "-",
                    "school_grade": application.school_grade or "-",
                    "transcript_available": application.transcript_available,
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
