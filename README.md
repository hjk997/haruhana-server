# 하루하나(Haruhana)

이 프로젝트는 **습관 달성표(스탬프)** 를 기록하고 관리하는 웹 애플리케이션입니다.  

향후 PWA로 배포하여 AWS 상에서 서비스할 계획입니다.

---

## 📌 프로젝트 개요
- 사용자는 **달성표(스탬프)** 를 생성하고, 매일 달성 여부와 메모를 기록할 수 있습니다.
- 스탬프 목록은 **스탬프 뷰** 와 **리스트 뷰** 두 가지 형태로 제공합니다.
- 로그인/회원가입 및 인증은 **JWT 기반**으로 처리합니다.
- 사용자는 목표 달성을 위한 스탬프를 만들 수 있습니다. 스탬프 이미지는 직접 등록할 수도 있습니다.
- 스탬프 이미지는 **S3를 연동**하여, 사용자가 자유롭게 업로드할 수 있습니다. 
- 매일 목표를 달성하고 스탬프를 채웁니다. 일별로 간단한 메모도 추가할 수 있습니다. 
- 초기 배포는 **AWS (EC2, RDS, S3, Route53 등)** 을 활용할 예정입니다.

---

## 🛠️ 기술 스택

### Frontend

[자세히 보기](https://github.com/hjk997/haruhana-client)

### Backend
- FastAPI (Python)
- SQLAlchemy / SQLModel (ORM)
- PostgreSQL (AWS RDS)
- JWT 인증 (OAuth2PasswordBearer 기반)
- MongoDB Atlas

### DevOps & Infra
- Docker / Docker Compose
- AWS EC2, RDS, S3, Route53
- GitHub Actions (CI/CD 예정)

---

## 📂 프로젝트 구조 (Backend)

```
haruhana-server/
├── core/ # 앱 설정 및 미들웨어
├── crud/ # DB CRUD 로직
├── db/ # DB 설정, 세션 관리 
├── models/ # SQLAlchemy / SQLModel 모델
├── router/ # API 라우터
├── schemas/ # Pydantic/SQLModel 스키마
├── utils/ # 공통 유틸리티 파일 
└── .env # 환경설정파일 
```

---

## 🚀 실행 방법 (개발 환경)

### Backend
```bash
# WSL / Ubuntu 환경에서 실행
docker-compose up -d  # PostgreSQL 실행

# 라이브러리 설치 
pip install -r requirements.txt
```

