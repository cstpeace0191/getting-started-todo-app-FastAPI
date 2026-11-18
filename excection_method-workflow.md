'

## 사전 준비 ;
1. 다운로드 ; `git clone https://github.com/cstpeace0191/getting-started-todo-app-fastapi-origin.git`
2. In Git Bash, `mv getting-started-todo-app-fastapi-origin getting-started-todo-app-fastapi`
3. `cd getting-started-todo-app-fastapi`

## 로컬 실행과 테스트 — 실제 출력
``` Git Bash
cd backend
uv venv 
source .venv/bin/activate     
# Windows PowerShell: .venv\Scripts\activate.ps1
uv init
uv pip install -r requirements.txt
SQLITE_DB_LOCATION=/tmp/todo-test.db pytest -q
```

