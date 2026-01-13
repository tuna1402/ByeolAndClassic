from django import forms

PURPOSE_CHOICES = [
    ("예술중", "예술중"),
    ("예술고", "예술고"),
    ("음대입시", "음대입시"),
    ("일반대학원실기", "일반대학원실기"),
    ("반주과입시", "반주과입시"),
    ("교수학실기", "교수학실기"),
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
