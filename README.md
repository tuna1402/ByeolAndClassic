Django 기반 개인 홈페이지 프로젝트.

## Dev Environment
- Windows 11 + WSL2 (Ubuntu)
- Python 3.11 + venv
- DB: SQLite (start)
- Front: Bootstrap + Django Templates

## Quickstart (WSL)
```bash
cd ~/PianoAcademy
python3.11 -m venv .venv
source .venv/bin/activate
pip install -U pip
pip install -r requirements.txt
make migrate
make run
```

## Initial Data
- news 카테고리 초기 데이터는 마이그레이션에 포함되어 있습니다.
- `python manage.py migrate` 실행 시 공지/콩쿨/입시 카테고리가 자동 생성됩니다.
- 초기 데이터가 누락되면 동일 마이그레이션을 재실행하거나 삭제 후 다시 migrate 하세요.
