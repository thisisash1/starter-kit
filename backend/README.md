# FastAPI 백엔드 스타터킷

초심자를 위한 Python FastAPI 백엔드 API 스타터 프로젝트입니다.

## 주요 기능

- ✅ 레이어드 아키텍처 (Controller → Service → Repository)
- ✅ 사용자 관리 CRUD API
- ✅ 페이지네이션 및 검색 기능
- ✅ 자동 API 문서화 (Swagger/ReDoc)
- ✅ 데이터베이스 마이그레이션 (Alembic)
- ✅ 환경 변수 관리
- ✅ 표준화된 에러 핸들링

## 기술 스택

- **언어**: Python 3.12+
- **프레임워크**: FastAPI 0.115+
- **데이터베이스**: MySQL 8.0+ (또는 호환 가능한 DB)
- **ORM**: SQLAlchemy 2.0+ (Async)
- **마이그레이션**: Alembic
- **검증**: Pydantic 2.0+

## 프로젝트 구조

```
backend/
├── app/
│   ├── core/                  # 핵심 유틸리티
│   │   ├── exceptions.py      # 커스텀 예외
│   │   ├── responses.py       # 표준 응답 포맷
│   │   └── pagination.py      # 페이지네이션
│   ├── models/                # SQLAlchemy ORM 모델
│   │   ├── base.py            # Base 모델
│   │   └── user.py            # User 모델
│   ├── schemas/               # Pydantic DTO
│   │   ├── base.py
│   │   └── user.py
│   ├── repositories/          # Repository 레이어
│   │   ├── base.py            # 제너릭 CRUD
│   │   └── user.py            # User Repository
│   ├── services/              # Service 레이어
│   │   └── user.py            # User Service
│   ├── api/                   # Controller 레이어
│   │   ├── router.py
│   │   └── v1/
│   │       └── users.py       # User 엔드포인트
│   ├── config.py              # 환경 변수 설정
│   ├── database.py            # DB 연결 설정
│   ├── dependencies.py        # 의존성
│   └── main.py                # FastAPI 앱 진입점
├── alembic/                   # 데이터베이스 마이그레이션
│   └── versions/
│       └── 001_create_users_table.py
├── requirements.txt           # 의존성
├── .env.example               # 환경 변수 예시
├── .env                       # 환경 변수 (git에서 제외)
├── alembic.ini                # Alembic 설정
└── README.md                  # 이 파일
```

## 시작하기

### 1단계: Python 가상환경 생성

```bash
python3 -m venv venv

# macOS/Linux:
source venv/bin/activate

# Windows:
venv\Scripts\activate
```

### 2단계: 의존성 설치

```bash
pip install -r requirements.txt
```

### 3단계: 환경 변수 설정

`.env.example` 파일을 `.env`로 복사하고 데이터베이스 정보를 입력합니다:

```bash
cp .env.example .env
```

`.env` 파일 수정:

```bash
APP_NAME=FastAPI Starter
DEBUG=True

DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=your_password
DB_NAME=fastapi_starter
```

### 4단계: MySQL 데이터베이스 생성

```sql
CREATE DATABASE fastapi_starter CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### 5단계: 데이터베이스 마이그레이션

```bash
alembic upgrade head
```

### 6단계: 개발 서버 실행

```bash
# 방법 1: Uvicorn 직접 실행
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# 방법 2: Python 스크립트 실행
python -m app.main
```

### 7단계: API 문서 확인

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
- 헬스 체크: http://localhost:8000/health

## API 엔드포인트

### 사용자 관리

| 메서드 | 경로 | 설명 |
|--------|------|------|
| POST | `/api/v1/users` | 사용자 생성 |
| GET | `/api/v1/users` | 사용자 목록 조회 (페이지네이션, 검색) |
| GET | `/api/v1/users/{id}` | 사용자 상세 조회 |
| PUT | `/api/v1/users/{id}` | 사용자 정보 수정 |
| DELETE | `/api/v1/users/{id}` | 사용자 삭제 |

### 쿼리 파라미터

**GET /api/v1/users**

- `page` (int): 페이지 번호 (기본값: 1)
- `page_size` (int): 페이지 크기 (기본값: 10, 최대: 100)
- `search` (str): 검색어 (이름 또는 이메일)

### 요청 예제

**사용자 생성**

```bash
curl -X POST "http://localhost:8000/api/v1/users" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "홍길동",
    "email": "hong@example.com",
    "age": 30
  }'
```

**사용자 목록 조회 (페이지네이션)**

```bash
curl "http://localhost:8000/api/v1/users?page=1&page_size=10"
```

**사용자 검색**

```bash
curl "http://localhost:8000/api/v1/users?search=홍길동"
```

**사용자 상세 조회**

```bash
curl "http://localhost:8000/api/v1/users/1"
```

**사용자 정보 수정**

```bash
curl -X PUT "http://localhost:8000/api/v1/users/1" \
  -H "Content-Type: application/json" \
  -d '{
    "age": 31
  }'
```

**사용자 삭제**

```bash
curl -X DELETE "http://localhost:8000/api/v1/users/1"
```

## 아키텍처 설명

### 레이어드 아키텍처

```
┌─────────────────────────────────────────┐
│   API Layer (Controller)                │
│   - HTTP 요청/응답 처리                 │
│   - 입력 검증 (Pydantic)                │
└────────────┬────────────────────────────┘
             │
┌────────────┴────────────────────────────┐
│   Service Layer                          │
│   - 비즈니스 로직                       │
│   - 데이터 변환 (Model ↔ DTO)          │
│   - 에러 처리                           │
└────────────┬────────────────────────────┘
             │
┌────────────┴────────────────────────────┐
│   Repository Layer                       │
│   - 데이터베이스 CRUD 작업              │
│   - 쿼리 실행                           │
│   - ORM 모델 처리                       │
└────────────┬────────────────────────────┘
             │
┌────────────┴────────────────────────────┐
│   Database Layer (MySQL)                 │
└──────────────────────────────────────────┘
```

### 데이터 흐름

1. **요청**: 클라이언트가 API 엔드포인트에 요청
2. **검증**: Pydantic이 입력 데이터 자동 검증
3. **서비스**: Service 레이어에서 비즈니스 로직 실행
4. **데이터 액세스**: Repository를 통해 데이터베이스 쿼리
5. **응답**: DTO로 변환된 응답 반환

## 코딩 컨벤션

- **언어**: 한국어 주석 (비즈니스 로직만)
- **네이밍**: snake_case
- **들여쓰기**: 2칸
- **타입 힌팅**: 모든 함수에 필수

## 에러 처리

### 표준 응답 포맷

**성공 응답**

```json
{
  "success": true,
  "data": { ... },
  "message": null
}
```

**에러 응답**

```json
{
  "success": false,
  "error": "에러 메시지",
  "detail": "상세 정보 (디버그 모드에서만)"
}
```

### 에러 코드

| 상태 코드 | 설명 |
|-----------|------|
| 400 | Bad Request (기본 에러) |
| 404 | Not Found (리소스 없음) |
| 409 | Conflict (중복 데이터) |
| 422 | Unprocessable Entity (입력값 검증 실패) |
| 500 | Internal Server Error |

## 데이터베이스 마이그레이션

### 마이그레이션 생성

```bash
alembic revision --autogenerate -m "설명"
```

### 마이그레이션 적용

```bash
alembic upgrade head
```

### 마이그레이션 이전 버전으로 되돌리기

```bash
alembic downgrade -1
```

### 마이그레이션 이력 확인

```bash
alembic current
alembic history
```

## 트러블슈팅

### 데이터베이스 연결 실패

**문제**: `pymysql.Error` 또는 `aiomysql` 연결 오류

**해결**:
1. MySQL 서버가 실행 중인지 확인
2. `.env` 파일의 DB 정보 확인
3. 데이터베이스가 존재하는지 확인

### 마이그레이션 실패

**문제**: Alembic 명령어 실패

**해결**:
1. `.env` 파일이 올바르게 설정되었는지 확인
2. MySQL 서버가 실행 중인지 확인
3. `alembic current`로 현재 마이그레이션 상태 확인

### 포트 이미 사용 중

**문제**: `Address already in use` 오류

**해결**:
```bash
# 다른 포트 사용
uvicorn app.main:app --reload --port 8001
```

## 다음 단계

### 기능 추가

1. **인증/인가**: JWT 토큰 기반 인증 시스템
2. **파일 업로드**: 이미지/파일 업로드 기능
3. **캐싱**: Redis 통합
4. **백그라운드 작업**: Celery 통합
5. **로깅**: 구조화된 로깅 시스템

### 배포

1. **Docker**: 컨테이너화
2. **프로덕션 서버**: Gunicorn + Nginx
3. **HTTPS**: SSL 인증서
4. **모니터링**: APM 도구 (Sentry 등)

## 라이선스

MIT License

## 기여

버그 리포트 및 기능 제안은 GitHub Issues에서 받습니다.
