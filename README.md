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