from django import forms

CONSULTATION_CHOICES = [
    ("입시수강상담", "입시수강상담"),
    ("입시컨설팅", "입시컨설팅"),
]

PRACTICE_TIME_CHOICES = [
    ("30분 이하", "30분 이하"),
    ("1시간 내외", "1시간 내외"),
    ("2시간 내외", "2시간 내외"),
    ("3시간 이상", "3시간 이상"),
]

SCHOOL_GRADE_CHOICES = [
    ("상", "상"),
    ("중", "중"),
    ("하", "하"),
]


class EnrollApplicationForm(forms.Form):
    name = forms.CharField(
        max_length=50,
        label="이름",
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "예: 홍길동"}
        ),
    )
    phone = forms.CharField(
        max_length=30,
        label="연락처",
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "예: 010-1234-5678"}
        ),
    )
    birth_date = forms.DateField(
        label="생년월일",
        widget=forms.DateInput(
            attrs={"type": "date", "class": "form-control", "placeholder": "YYYY-MM-DD"}
        ),
    )
    residence = forms.CharField(
        max_length=100,
        label="거주지",
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "예: 광주광역시 북구"}
        ),
    )
    consultation_types = forms.ChoiceField(
        choices=CONSULTATION_CHOICES,
        widget=forms.RadioSelect(attrs={"class": "form-check-input"}),
        label="상담 유형",
    )
    level_test_piece = forms.CharField(
        max_length=200,
        required=False,
        label="레벨테스트 연주곡",
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "예: 베토벤 비창 1악장",
            }
        ),
    )
    career_school = forms.CharField(
        max_length=200,
        required=False,
        label="희망 학교",
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "예: OO예술중, OO예술고, OO대학/대학원",
            }
        ),
    )
    awards_history = forms.CharField(
        label="수상내역",
        required=False,
        widget=forms.Textarea(
            attrs={
                "rows": 3,
                "class": "form-control",
                "placeholder": "예: 2024 OO콩쿠르 금상",
            }
        ),
    )
    practice_time = forms.ChoiceField(
        choices=PRACTICE_TIME_CHOICES,
        widget=forms.RadioSelect(attrs={"class": "form-check-input"}),
        label="피아노 연습량",
        required=False,
    )
    school_grade = forms.ChoiceField(
        choices=SCHOOL_GRADE_CHOICES,
        widget=forms.RadioSelect(attrs={"class": "form-check-input"}),
        label="학교 성적",
        required=False,
    )
    transcript_available = forms.BooleanField(
        label="성적표 지참 가능 여부",
        required=False,
        widget=forms.CheckboxInput(attrs={"class": "form-check-input"}),
    )
    preferred_date = forms.DateField(
        label="희망 상담/수업 시작일",
        widget=forms.DateInput(
            attrs={"type": "date", "class": "form-control", "placeholder": "YYYY-MM-DD"}
        ),
    )
    message = forms.CharField(
        label="문의 내용",
        required=False,
        widget=forms.Textarea(
            attrs={
                "rows": 4,
                "class": "form-control",
            }
        ),
    )

    def clean(self):
        cleaned = super().clean()
        consultation_type = (cleaned.get("consultation_types") or "").strip()
        level_test_piece = cleaned.get("level_test_piece", "").strip()
        career_school = cleaned.get("career_school", "").strip()
        awards_history = cleaned.get("awards_history", "").strip()
        practice_time = cleaned.get("practice_time", "").strip()
        school_grade = cleaned.get("school_grade", "").strip()

        if consultation_type == "입시수강상담":
            if not level_test_piece:
                self.add_error("level_test_piece", "레벨테스트 연주곡을 입력해 주세요.")
            if not career_school:
                self.add_error("career_school", "희망 학교를 입력해 주세요.")
            if not awards_history:
                self.add_error("awards_history", "수상내역을 입력해 주세요.")
            if not practice_time:
                self.add_error("practice_time", "피아노 연습량을 선택해 주세요.")
            if not school_grade:
                self.add_error("school_grade", "학교 성적을 선택해 주세요.")

        if consultation_type == "입시컨설팅":
            if not level_test_piece:
                self.add_error("level_test_piece", "레벨테스트 연주곡을 입력해 주세요.")
            if not career_school:
                self.add_error("career_school", "희망 학교를 입력해 주세요.")

        cleaned["consultation_types"] = [consultation_type] if consultation_type else []
        cleaned["level_test_piece"] = level_test_piece
        cleaned["career_school"] = career_school
        cleaned["awards_history"] = awards_history
        cleaned["practice_time"] = practice_time
        cleaned["school_grade"] = school_grade
        return cleaned
