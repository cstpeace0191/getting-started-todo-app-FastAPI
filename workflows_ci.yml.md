# CI 워크플로 설명 (.github/workflows/ci.yml)

파일: [.github/workflows/ci.yml](.github/workflows/ci.yml)

이 워크플로는 GitHub Actions에서 코드 변경마다 백엔드, 클라이언트, Docker 이미지를 자동으로 검사합니다. 검사에 하나라도 실패하면 PR 체크가 실패로 표시됩니다.

## 실행 시점

- `main` 브랜치를 대상으로 하는 Pull Request가 열리거나 갱신될 때 (`pull_request`)
- `main` 브랜치에 push될 때 (`push`)
- Actions 탭에서 수동으로 실행할 때 (`workflow_dispatch`)

같은 브랜치에서 새 실행이 시작되면 이전 실행은 취소됩니다 (`concurrency`).

## 권한

`permissions: contents: read`로 저장소 내용 읽기 권한만 부여합니다.

## 작업(job) 구성

### 1. backend (ruff + pytest)

`backend/` 폴더에서 실행되며 최대 10분입니다.

1. 저장소를 체크아웃하고 Python 3.12를 설치합니다 (pip 캐시 사용).
2. `pip install -r requirements-dev.txt`로 개발 의존성을 설치합니다.
3. `ruff check .`로 린트를 검사합니다. 결과는 GitHub 주석 형식으로 표시됩니다.
4. `pytest`를 실행하며 `src/` 폴더의 커버리지를 측정합니다. 커버리지가 80% 미만이면 실패합니다. 결과는 `junit.xml`, `coverage.xml`로 저장됩니다.
5. 커버리지 요약을 실행 결과 화면(`GITHUB_STEP_SUMMARY`)에 표시합니다. 이 단계는 앞 단계가 실패해도 실행됩니다 (`if: always()`).
6. `backend-test-report` 아티팩트로 `coverage.xml`과 `junit.xml`을 업로드합니다. 이 단계도 항상 실행됩니다.

환경 변수 `SQLITE_DB_LOCATION=/tmp/todo-test.db`는 러너에서 쓰기가 불가능한 기본 경로 `/etc/todos`를 피하기 위한 설정입니다.

### 2. client (eslint + build)

`client/` 폴더에서 실행되며 최대 10분입니다.

1. Node.js 22를 설치합니다 (npm 캐시 사용).
2. `npm ci --ignore-scripts`로 의존성을 설치합니다. 설치 스크립트는 실행하지 않습니다.
3. `npm run lint`로 ESLint를 실행합니다.
4. `npm run build`로 프로덕션 빌드를 확인합니다.

### 3. docker (multi-stage build)

`backend`와 `client` 작업이 모두 성공해야 실행됩니다 (`needs`). 최대 20분입니다.

1. Buildx를 설정합니다.
2. 저장소 루트의 Dockerfile에서 `final` 타깃을 빌드합니다. push는 하지 않고 로컬 이미지 `todo-app:ci`로만 로드합니다. 빌드 캐시는 GitHub Actions 캐시를 사용합니다.
3. 스모크 테스트: 컨테이너를 3000번 포트로 실행한 뒤, 최대 20초 동안 `http://localhost:3000/api/greeting`에 응답하는지 확인합니다. 응답이 없으면 컨테이너 로그를 출력하고 실패합니다.

## 요약

| 작업 | 검사 내용 | 선행 조건 |
|---|---|---|
| backend | ruff 린트, pytest, 커버리지 80% 이상 | 없음 |
| client | ESLint, 빌드 | 없음 |
| docker | Docker 이미지 빌드, `/api/greeting` 응답 확인 | backend, client 성공 |
