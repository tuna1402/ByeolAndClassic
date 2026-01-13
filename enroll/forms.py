from django import forms

PURPOSE_CHOICES = [
    ("hobby", "취미/여가"),
    ("exam", "입시/콩쿨"),
    ("major", "전공/전문 과정"),
    ("other", "기타"),
]


class EnrollApplicationForm(forms.Form):
    name = forms.CharField(max_length=50, label="이름")
    phone = forms.CharField(max_length=30, label="연락처")
    birth_date = forms.DateField(
        label="생년월일",
        widget=forms.DateInput(attrs={"type": "date"}),
    )
    residence = forms.CharField(max_length=100, label="거주지")
    purposes = forms.MultipleChoiceField(
        choices=PURPOSE_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        label="수강 목적",
    )
    preferred_date = forms.DateField(
        label="희망 상담/수업 시작일",
        widget=forms.DateInput(attrs={"type": "date"}),
    )
    message = forms.CharField(
        label="문의 내용",
        required=False,
        widget=forms.Textarea(attrs={"rows": 4}),
    )
