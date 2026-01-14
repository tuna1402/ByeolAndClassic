# Deployment (WSL2 + Cloudflare Tunnel)

## 0원 운영 아키텍처

Cloudflare Tunnel → Caddy (:8080) → Gunicorn (:8000)

- Cloudflare Tunnel이 외부 트래픽을 받고, 로컬 Caddy로 전달합니다.
- Caddy는 정적/미디어 파일을 서빙하고, 나머지는 Gunicorn으로 프록시합니다.

## 최초 1회 설정

1) `.env` 준비
   - `deploy/env.prod.example -> .env` 로 복사 후 값 채우기
   - **`.env`는 커밋 금지**
2) 의존성 설치

```bash
pip install -r requirements.txt
```

3) 마이그레이션/정적 수집

```bash
python manage.py migrate
python manage.py collectstatic --noinput
```

## 수동 실행 순서 (테스트/검증용)

```bash
set -a
source .env
set +a

./deploy/run_gunicorn.sh
```

```bash
caddy run --config ./deploy/Caddyfile
```

```bash
cloudflared tunnel --config ./deploy/cloudflared-config.yml run
```

## systemd로 상시 구동 (WSL systemd=true 가정)

```bash
sudo cp deploy/systemd/*.service deploy/systemd/*.timer /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable --now byeolandclassic-gunicorn.service
sudo systemctl enable --now byeolandclassic-caddy.service
sudo systemctl enable --now byeolandclassic-cloudflared.service
sudo systemctl enable --now byeolandclassic-backup.timer
```

> **주의**: `/home/<user>/PianoAcademy` 경로, `.env` 위치, 터널 UUID는 반드시 수정해야 합니다.

## Cloudflare Tunnel 설정 요약

1) tunnel 생성
2) 도메인 매핑 후 `deploy/cloudflared-config.yml` 작성
3) `cloudflared-config.example.yml` 참고

**ingress에 catch-all (`http_status:404`) 항목이 반드시 필요**합니다.

## 백업

### 수동 백업

```bash
./deploy/backup/backup.sh
```

- 기본 경로: `~/backups/byeolandclassic`
- `BACKUP_DIR=/path/to/backup` 환경변수로 경로 변경 가능

### systemd timer (매일 03:00)

```bash
sudo systemctl enable --now byeolandclassic-backup.timer
```

### cron 대안

```bash
0 3 * * * /home/<user>/PianoAcademy/deploy/backup/backup.sh
```

## 복원 방법

- `db.sqlite3` 복원: 백업 디렉터리의 `db.sqlite3`를 프로젝트 루트로 복사
- `media` 복원: 백업 디렉터리의 `media/`를 프로젝트 `media/`로 복사

## 흔한 문제

- **포트 충돌**: 8000/8080 사용 중인지 확인
- **staticfiles 비어 있음**: `python manage.py collectstatic --noinput` 실행
- **403 CSRF**: `.env`의 `CSRF_TRUSTED_ORIGINS` 확인
- **cloudflared 404**: ingress catch-all 설정 확인
