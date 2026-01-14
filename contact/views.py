import logging

from django.contrib import messages
from django.shortcuts import redirect, render

from contact.forms import ContactForm
from core.services.email import send_contact_email

logger = logging.getLogger(__name__)


def form(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            message = form.save()
            try:
                send_contact_email(
                    {
                        "name": message.name,
                        "phone": message.phone,
                        "email": message.email,
                        "message": message.message,
                    }
                )
                logger.info("Contact email sent for message_id=%s", message.id)
            except Exception:
                logger.exception("Contact email failed for message_id=%s", message.id)
            messages.success(
                request,
                "문의가 접수되었습니다. 담당자가 확인 후 연락드리겠습니다.",
            )
            return redirect("contact_done")
    else:
        form = ContactForm()

    return render(request, "contact/form.html", {"form": form})


def done(request):
    return render(request, "contact/done.html")
