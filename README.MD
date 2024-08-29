# Django 와 Svelte 로 만든 게시판

---
### docker 실행방법
- docker-compose.yaml 파일이 있는 곳에서 docker compose up 으로 실행

---
### 구글 OAuth 실행
- 구글 OAuth 2.0 기능이 정상 작동 하려면 구글 api 가 필요
- https://console.cloud.google.com/welcome/new 
- 사용자 인증 정보로 - 클라이언트 ID 와 클라이언트 보안 비밀번호 생성
- django 관리자에서 주소 설정후 클라이언트 ID 와 클라이언트 보안 비밀번호 입력 
- 정상적으로 구글 OAuth 작동 
- 클라이언트 ID와 보안 비밀번호가 공개되면 안됨
- git에는 클라이언트 ID와 보안 비밀번호 정보 제외 - 구글 OAuth2.0 제외된 상태
