# django 와 svelte 로 만든 게시판 docker 와 docker compose 기능을 사용


---
### docker 실행방법 - 우분투 환경 기준
- compose.yaml 파일이 있는 곳에서 터미널 실행후 docker compose up 또는 docker compose up --build 로 실행


---
#### 구글 OAuth 실행
- 구글 OAuth 2.0 기능이 정상 작동 하려면 구글 api 가 필요
- https://console.cloud.google.com/welcome/new 
- 사용자 인증 정보로 - 클라이언트 ID 와 클라이언트 보안 비밀번호 생성
- django 관리자 에서 주소 설정후 클라이언트 ID 와 클라이언트 보안 비밀번호 입력 
- 정상적으로 구글 OAuth 작동 - git에는 구글 api 서비스 정보 제외
