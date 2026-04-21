@echo off
chcp 949 >nul
setlocal enabledelayedexpansion

:: ============================================================
:: 바이브코딩 환경 키트 -- DEV-KIT.bat v1.0
:: AI 바이브코딩 입문자를 위한 원클릭 개발 환경 세팅 도구
:: ============================================================

:: 날짜 변수 (PowerShell로 로케일 독립적 처리)
for /f %%d in ('powershell -NoProfile -Command "Get-Date -Format yyyyMMdd" 2^>nul') do set REPORT_DATE=%%d
if not defined REPORT_DATE set REPORT_DATE=%DATE:~0,4%%DATE:~5,2%%DATE:~8,2%

set REPORT_FILE=%~dp0install-report-%REPORT_DATE%.txt
set LOG_FILE=%~dp0install-log-%REPORT_DATE%.txt
set START_TIME=%TIME%
set UPGRADE_MODE=skip

:: 로그 파일 초기화
> "%LOG_FILE%" echo === 바이브코딩 환경 키트 설치 상세 로그 ===
>> "%LOG_FILE%" echo 시작: %DATE% %TIME%
>> "%LOG_FILE%" echo.

:MAIN_MENU
cls
echo.
echo  ===========================================================
echo    바이브코딩 환경 키트 ^| AI 개발 환경 원클릭 세팅
echo  ===========================================================
echo.
echo    [1] 왕초보 설치    처음 시작하는 분  (5개,  ~7분)
echo    [2] 중급 설치      어느 정도 써본 분 (11개, ~15분)
echo    [3] 고급 설치      앱/서버 개발하는 분(16개, ~35분)
echo    [4] 올인원 설치    모든 도구 설치    (18개, ~45분)
echo    ---------------------------------------------------
echo    [5] 선택 설치      원하는 것만 골라서
echo    [6] 업데이트       설치된 도구 전체 최신으로
echo    [7] 제거           도구 삭제 (개별/전체)
echo    [8] 직접 다운로드  공식 사이트 URL 목록 (winget 불가 시)
echo    [9] 설치 확인      O/X + 버전 상태 표시
echo    [0] 종료
echo.
echo  ===========================================================
set /p MENU_CHOICE="  번호를 입력하세요: "

if "!MENU_CHOICE!"=="1" goto DO_LEVEL_1
if "!MENU_CHOICE!"=="2" goto DO_LEVEL_2
if "!MENU_CHOICE!"=="3" goto DO_LEVEL_3
if "!MENU_CHOICE!"=="4" goto DO_LEVEL_4
if "!MENU_CHOICE!"=="5" goto DO_SELECT
if "!MENU_CHOICE!"=="6" goto DO_UPDATE
if "!MENU_CHOICE!"=="7" goto DO_REMOVE
if "!MENU_CHOICE!"=="8" goto DO_MANUAL
if "!MENU_CHOICE!"=="9" goto DO_CHECK
if "!MENU_CHOICE!"=="0" goto DO_EXIT
goto MAIN_MENU

:: ============================================================
:: 사전 체크 (공통)
:: 호출 전 PRE_CHECK_RETURN 변수에 복귀 레이블 설정
:: ============================================================
:PRE_CHECK
echo.
echo  [사전 체크] 설치 환경을 확인합니다...
echo.
>> "%LOG_FILE%" echo.
>> "%LOG_FILE%" echo === 사전 체크: %TIME% ===

:: 1. Windows 버전 확인 (빌드 19044 = Win10 21H2)
:: delims=. 으로 "10.0.22631.xxx" 의 세 번째 토큰(빌드번호)만 추출
for /f "tokens=3 delims=." %%a in ('ver') do set WIN_BUILD=%%a
if defined WIN_BUILD (
    if !WIN_BUILD! LSS 19044 (
        echo  [주의] Windows 10 오래된 버전 감지 (빌드: !WIN_BUILD!)
        echo         winget 수동 설치: https://aka.ms/getwinget
        echo.
        >> "%LOG_FILE%" echo 주의: Windows 빌드 !WIN_BUILD! - winget 불안정 가능
        set /p CONT_WIN="  계속 진행하시겠습니까? (Y/N): "
        if /i "!CONT_WIN!" NEQ "y" goto MAIN_MENU
    ) else (
        echo  [OK] Windows 빌드 !WIN_BUILD!
        >> "%LOG_FILE%" echo OK: Windows 빌드 !WIN_BUILD!
    )
)

:: 2. winget 확인
winget --version >nul 2>&1
if errorlevel 1 (
    echo.
    echo  [오류] winget을 찾을 수 없습니다.
    echo         Microsoft Store 검색: "앱 설치 관리자"
    echo         또는: https://aka.ms/getwinget
    echo.
    >> "%LOG_FILE%" echo 오류: winget 없음
    pause
    goto MAIN_MENU
)
for /f %%v in ('winget --version') do set WINGET_VER=%%v
echo  [OK] winget !WINGET_VER!
>> "%LOG_FILE%" echo OK: winget !WINGET_VER!

:: 3. winget source update (실패해도 강제 종료 금지)
echo  [..] 패키지 목록 업데이트 중... (처음 실행 시 1~2분, 이후 빠름)
winget source update >nul 2>&1
if errorlevel 1 (
    echo  [주의] 패키지 목록 업데이트 실패 - 계속 진행합니다
    >> "%LOG_FILE%" echo 주의: winget source update 실패
) else (
    echo  [OK] 패키지 목록 업데이트 완료
    >> "%LOG_FILE%" echo OK: winget source update 성공
)

:: 4. 인터넷 연결 확인
ping -n 1 -w 3000 8.8.8.8 >nul 2>&1
if errorlevel 1 (
    echo  [주의] 인터넷 연결을 확인하세요.
    echo.
    >> "%LOG_FILE%" echo 주의: 인터넷 연결 불안정
    set /p CONT_NET="  계속 진행하시겠습니까? (Y/N): "
    if /i "!CONT_NET!" NEQ "y" goto MAIN_MENU
) else (
    echo  [OK] 인터넷 연결 확인
    >> "%LOG_FILE%" echo OK: 인터넷 연결
)

:: 5. 기존 Node.js 감지 (충돌 안내)
where node >nul 2>&1
if not errorlevel 1 (
    for /f %%v in ('node --version 2^>nul') do (
        echo  [안내] 기존 Node.js %%v 감지 - 건너뜀 처리됩니다
        >> "%LOG_FILE%" echo 안내: 기존 Node.js %%v 감지
    )
)

:: 6. 기존 Python 감지 (충돌 안내)
where python >nul 2>&1
if not errorlevel 1 (
    for /f %%v in ('python --version 2^>nul') do (
        echo  [안내] 기존 Python %%v 감지 - 건너뜀 처리됩니다
        >> "%LOG_FILE%" echo 안내: 기존 Python %%v 감지
    )
)

echo.
echo  [완료] 사전 체크 완료. 설치를 시작합니다.
>> "%LOG_FILE%" echo 사전 체크 완료
timeout /t 2 >nul
goto %PRE_CHECK_RETURN%

:: ============================================================
:: 레벨별 설치 진입점
:: ============================================================
:DO_LEVEL_1
set LEVEL_NAME=왕초보
set TOTAL=5
set CURRENT=0
set INSTALL_COUNT=0
set SKIP_COUNT=0
set FAIL_COUNT=0
del "%REPORT_FILE%.tmp" >nul 2>&1
echo.
echo  --------------------------------------------------
echo  [왕초보 설치 목록] 5개 도구 (약 7분 / 디스크 ~1GB)
echo    Git, Python 3, Node.js LTS, VS Code, Windows Terminal
echo  --------------------------------------------------
echo.
set /p CONFIRM_INST="  Y=설치 시작 / N=메인 메뉴로: "
if /i "!CONFIRM_INST!" NEQ "y" goto MAIN_MENU
echo.
echo  이미 설치된 도구 처리 방법:
echo    [1] 건너뜀    (현재 버전 유지)
echo    [2] 업그레이드 (최신 버전으로)
echo    [3] 제거       (삭제만)
set /p UPGRADE_CHOICE="  선택 (기본값=1): "
if "!UPGRADE_CHOICE!"=="" set UPGRADE_CHOICE=1
if "!UPGRADE_CHOICE!"=="2" (set UPGRADE_MODE=upgrade) else (
if "!UPGRADE_CHOICE!"=="3" (set UPGRADE_MODE=remove)  else (
set UPGRADE_MODE=skip))
set PRE_CHECK_RETURN=INSTALL_LEVEL_1
goto PRE_CHECK

:DO_LEVEL_2
set LEVEL_NAME=중급
set TOTAL=11
set CURRENT=0
set INSTALL_COUNT=0
set SKIP_COUNT=0
set FAIL_COUNT=0
del "%REPORT_FILE%.tmp" >nul 2>&1
echo.
echo  --------------------------------------------------
echo  [중급 설치 목록] 11개 도구 (약 15분 / 디스크 ~2GB)
echo    Git, Python, Node.js, GitHub CLI, PS7, pnpm, Bun, Ollama, VSCode, WinTerminal
echo  --------------------------------------------------
echo.
set /p CONFIRM_INST="  Y=설치 시작 / N=메인 메뉴로: "
if /i "!CONFIRM_INST!" NEQ "y" goto MAIN_MENU
echo.
echo  이미 설치된 도구 처리 방법:
echo    [1] 건너뜀    (현재 버전 유지)
echo    [2] 업그레이드 (최신 버전으로)
echo    [3] 제거       (삭제만)
set /p UPGRADE_CHOICE="  선택 (기본값=1): "
if "!UPGRADE_CHOICE!"=="" set UPGRADE_CHOICE=1
if "!UPGRADE_CHOICE!"=="2" (set UPGRADE_MODE=upgrade) else (
if "!UPGRADE_CHOICE!"=="3" (set UPGRADE_MODE=remove)  else (
set UPGRADE_MODE=skip))
set PRE_CHECK_RETURN=INSTALL_LEVEL_2
goto PRE_CHECK

:DO_LEVEL_3
set LEVEL_NAME=고급
set TOTAL=16
set CURRENT=0
set INSTALL_COUNT=0
set SKIP_COUNT=0
set FAIL_COUNT=0
del "%REPORT_FILE%.tmp" >nul 2>&1
echo.
echo  --------------------------------------------------
echo  [고급 설치 목록] 16개 도구 (약 35분 / 디스크 ~6GB)
echo    중급 포함 + Java 21 LTS, Flutter+Dart, Go, Rust
echo  --------------------------------------------------
echo.
set /p CONFIRM_INST="  Y=설치 시작 / N=메인 메뉴로: "
if /i "!CONFIRM_INST!" NEQ "y" goto MAIN_MENU
echo.
echo  이미 설치된 도구 처리 방법:
echo    [1] 건너뜀    (현재 버전 유지)
echo    [2] 업그레이드 (최신 버전으로)
echo    [3] 제거       (삭제만)
set /p UPGRADE_CHOICE="  선택 (기본값=1): "
if "!UPGRADE_CHOICE!"=="" set UPGRADE_CHOICE=1
if "!UPGRADE_CHOICE!"=="2" (set UPGRADE_MODE=upgrade) else (
if "!UPGRADE_CHOICE!"=="3" (set UPGRADE_MODE=remove)  else (
set UPGRADE_MODE=skip))
set PRE_CHECK_RETURN=INSTALL_LEVEL_3
goto PRE_CHECK

:DO_LEVEL_4
set LEVEL_NAME=올인원
set TOTAL=18
set CURRENT=0
set INSTALL_COUNT=0
set SKIP_COUNT=0
set FAIL_COUNT=0
del "%REPORT_FILE%.tmp" >nul 2>&1
echo.
echo  --------------------------------------------------
echo  [올인원 설치 목록] 18개 도구 (약 45분 / 디스크 ~7GB)
echo    고급 포함 + Ruby, PHP
echo  --------------------------------------------------
echo.
set /p CONFIRM_INST="  Y=설치 시작 / N=메인 메뉴로: "
if /i "!CONFIRM_INST!" NEQ "y" goto MAIN_MENU
echo.
echo  이미 설치된 도구 처리 방법:
echo    [1] 건너뜀    (현재 버전 유지)
echo    [2] 업그레이드 (최신 버전으로)
echo    [3] 제거       (삭제만)
set /p UPGRADE_CHOICE="  선택 (기본값=1): "
if "!UPGRADE_CHOICE!"=="" set UPGRADE_CHOICE=1
if "!UPGRADE_CHOICE!"=="2" (set UPGRADE_MODE=upgrade) else (
if "!UPGRADE_CHOICE!"=="3" (set UPGRADE_MODE=remove)  else (
set UPGRADE_MODE=skip))
set PRE_CHECK_RETURN=INSTALL_LEVEL_4
goto PRE_CHECK

:: ============================================================
:: 왕초보 설치 (5개) - 의존성 순서 준수
:: ============================================================
:INSTALL_LEVEL_1
cls
echo.
echo  [왕초보 설치] 5개 도구를 설치합니다.
echo.
>> "%LOG_FILE%" echo === 왕초보 설치 시작: %TIME% ===

:: 의존성 1순위: Git
call :INSTALL "Git" "Git.Git"
:: 의존성 2순위: Python + Node.js
call :INSTALL "Python 3" "Python.Python.3"
call :INSTALL "Node.js LTS" "OpenJS.NodeJS.LTS"
:: 순위무관
call :INSTALL "VS Code" "Microsoft.VisualStudioCode"
call :INSTALL "Windows Terminal" "Microsoft.WindowsTerminal"

call :POST_BEGINNER
call :MAKE_REPORTS
call :PATH_CHECK
call :DONE_MSG
goto MAIN_MENU

:: ============================================================
:: 중급 설치 (왕초보 포함 10개)
:: ============================================================
:INSTALL_LEVEL_2
cls
echo.
echo  [중급 설치] 11개 도구를 설치합니다.
echo.
>> "%LOG_FILE%" echo === 중급 설치 시작: %TIME% ===

call :INSTALL "Git" "Git.Git"
call :INSTALL "Git LFS" "GitHub.GitLFS"
call :INSTALL "Python 3" "Python.Python.3"
call :INSTALL "Node.js LTS" "OpenJS.NodeJS.LTS"
call :INSTALL "GitHub CLI" "GitHub.cli"
call :INSTALL "PowerShell 7" "Microsoft.PowerShell"
:: 의존성 3순위: Node.js 이후 필수
call :INSTALL "pnpm" "pnpm.pnpm"
call :INSTALL "Bun" "Oven-sh.Bun"
call :INSTALL "Ollama" "Ollama.Ollama"
call :INSTALL "VS Code" "Microsoft.VisualStudioCode"
call :INSTALL "Windows Terminal" "Microsoft.WindowsTerminal"

call :POST_BEGINNER
call :POST_INTERMEDIATE
call :MAKE_REPORTS
call :PATH_CHECK
call :DONE_MSG
goto MAIN_MENU

:: ============================================================
:: 고급 설치 (중급 포함 14개)
:: ============================================================
:INSTALL_LEVEL_3
cls
echo.
echo  [고급 설치] 15개 도구를 설치합니다.
echo.
>> "%LOG_FILE%" echo === 고급 설치 시작: %TIME% ===

call :INSTALL "Git" "Git.Git"
call :INSTALL "Git LFS" "GitHub.GitLFS"
call :INSTALL "Python 3" "Python.Python.3"
call :INSTALL "Node.js LTS" "OpenJS.NodeJS.LTS"
call :INSTALL "GitHub CLI" "GitHub.cli"
call :INSTALL "PowerShell 7" "Microsoft.PowerShell"
call :INSTALL "pnpm" "pnpm.pnpm"
call :INSTALL "Bun" "Oven-sh.Bun"
call :INSTALL "Ollama" "Ollama.Ollama"
call :INSTALL "VS Code" "Microsoft.VisualStudioCode"
call :INSTALL "Windows Terminal" "Microsoft.WindowsTerminal"
:: 의존성 4순위: Java
call :INSTALL "Java 21 LTS" "EclipseAdoptium.Temurin.21.JDK"
call :INSTALL "Go" "GoLang.Go"
call :INSTALL "Rust" "Rustlang.Rustup"
:: 의존성 5순위: Java 이후 필수
call :INSTALL "Flutter+Dart" "Google.FlutterSDK"
call :INSTALL "Stripe CLI" "Stripe.StripeCLI"

call :POST_BEGINNER
call :POST_INTERMEDIATE
call :POST_ADVANCED
call :MAKE_REPORTS
call :PATH_CHECK
call :DONE_MSG
goto MAIN_MENU

:: ============================================================
:: 올인원 설치 (고급 포함 16개)
:: ============================================================
:INSTALL_LEVEL_4
cls
echo.
echo  [올인원 설치] 17개 도구를 설치합니다.
echo.
>> "%LOG_FILE%" echo === 올인원 설치 시작: %TIME% ===

call :INSTALL "Git" "Git.Git"
call :INSTALL "Git LFS" "GitHub.GitLFS"
call :INSTALL "Python 3" "Python.Python.3"
call :INSTALL "Node.js LTS" "OpenJS.NodeJS.LTS"
call :INSTALL "GitHub CLI" "GitHub.cli"
call :INSTALL "PowerShell 7" "Microsoft.PowerShell"
call :INSTALL "pnpm" "pnpm.pnpm"
call :INSTALL "Bun" "Oven-sh.Bun"
call :INSTALL "Ollama" "Ollama.Ollama"
call :INSTALL "VS Code" "Microsoft.VisualStudioCode"
call :INSTALL "Windows Terminal" "Microsoft.WindowsTerminal"
call :INSTALL "Java 21 LTS" "EclipseAdoptium.Temurin.21.JDK"
call :INSTALL "Go" "GoLang.Go"
call :INSTALL "Rust" "Rustlang.Rustup"
call :INSTALL "Flutter+Dart" "Google.FlutterSDK"
call :INSTALL "Stripe CLI" "Stripe.StripeCLI"
call :INSTALL "Ruby" "RubyInstallerTeam.RubyWithDevKit.3.3"
call :INSTALL "PHP" "PHP.PHP"

call :POST_BEGINNER
call :POST_INTERMEDIATE
call :POST_ADVANCED
call :MAKE_REPORTS
call :PATH_CHECK
call :DONE_MSG
goto MAIN_MENU

:: ============================================================
:: 도구 설치 서브루틴
:: %~1 = 도구 이름(한글), %~2 = winget ID
:: ============================================================
:: ============================================================
:: npm 전역 설치 서브루틴
:: %~1 = 도구 이름(한글), %~2 = npm 패키지명
:: ============================================================
:NPM_INSTALL
echo  [npm] %~1 설치 중...
>> "%LOG_FILE%" echo [npm] %~2 시작: %TIME%

npm list -g %~2 >nul 2>&1
if not errorlevel 1 (
    if "!UPGRADE_MODE!"=="upgrade" (
        npm update -g %~2 >nul 2>&1
        echo         [업그레이드] %~1 (npm)
        >> "%LOG_FILE%" echo   결과: 업그레이드 (npm)
        >> "%REPORT_FILE%.tmp" echo   [업그레이드] %~1 (npm)
    ) else if "!UPGRADE_MODE!"=="remove" (
        npm uninstall -g %~2 >nul 2>&1
        echo         [제거] %~1 (npm)
        >> "%LOG_FILE%" echo   결과: 제거 (npm)
        >> "%REPORT_FILE%.tmp" echo   [제거] %~1 (npm)
    ) else (
        echo         [건너뜀] %~1 (이미 설치됨)
        >> "%LOG_FILE%" echo   결과: 건너뜀 (이미 설치됨)
        >> "%REPORT_FILE%.tmp" echo   [건너뜀] %~1 (npm)
    )
    goto :eof
)

npm install -g %~2 >nul 2>&1
if not errorlevel 1 (
    echo         [완료] %~1
    >> "%LOG_FILE%" echo   결과: 성공 (npm)
    >> "%REPORT_FILE%.tmp" echo   [설치] %~1 (npm)
    goto :eof
)

echo         [재시도] %~1...
timeout /t 5 /nobreak >nul
npm install -g %~2 >nul 2>&1
if not errorlevel 1 (
    echo         [완료] %~1 (재시도 성공)
    >> "%REPORT_FILE%.tmp" echo   [설치] %~1 (npm)
    goto :eof
)

echo         [건너뜀] %~1 (npm 설치 실패)
>> "%LOG_FILE%" echo   결과: 실패 (npm)
>> "%REPORT_FILE%.tmp" echo   [실패] %~1 (npm)
goto :eof

:INSTALL
set /a CURRENT+=1
echo  [!CURRENT!/!TOTAL!] %~1 설치 중...
>> "%LOG_FILE%" echo [!CURRENT!/!TOTAL!] %~2 시작: %TIME%

winget install --id %~2 --source winget --accept-source-agreements --accept-package-agreements --silent >nul 2>&1
set INST_ERR=!errorlevel!

if !INST_ERR! EQU 0 (
    echo         [완료] %~1
    >> "%LOG_FILE%" echo   결과: 성공 (errorlevel=0)
    set /a INSTALL_COUNT+=1
    >> "%REPORT_FILE%.tmp" echo   [성공] %~1
    goto :eof
)

:: errorlevel 0이 아닌 경우 ? winget list로 이미 설치됨 여부 확인
winget list --id %~2 --source winget >nul 2>&1
if not errorlevel 1 (
    if "!UPGRADE_MODE!"=="upgrade" (
        winget upgrade --id %~2 --source winget --accept-source-agreements --accept-package-agreements --silent >nul 2>&1
        echo         [업그레이드] %~1
        >> "%LOG_FILE%" echo   결과: 업그레이드 (errorlevel=!INST_ERR!)
        set /a INSTALL_COUNT+=1
        >> "%REPORT_FILE%.tmp" echo   [업그레이드] %~1
    ) else if "!UPGRADE_MODE!"=="remove" (
        winget uninstall --id %~2 --source winget --silent >nul 2>&1
        echo         [제거] %~1
        >> "%LOG_FILE%" echo   결과: 제거
        set /a SKIP_COUNT+=1
        >> "%REPORT_FILE%.tmp" echo   [제거] %~1
    ) else (
        echo         [건너뜀] %~1 (이미 설치됨)
        >> "%LOG_FILE%" echo   결과: 건너뜀 (이미 설치됨, errorlevel=!INST_ERR!)
        set /a SKIP_COUNT+=1
        >> "%REPORT_FILE%.tmp" echo   [건너뜀] %~1
    )
    goto :eof
)

:: 실제 실패 ? 5초 후 1회 자동 재시도
echo         [재시도] %~1 실패 ? 5초 후 재시도...
>> "%LOG_FILE%" echo   1차 실패 (errorlevel=!INST_ERR!), 재시도: %TIME%
timeout /t 5 >nul

winget install --id %~2 --source winget --accept-source-agreements --accept-package-agreements --silent >nul 2>&1
set RETRY_ERR=!errorlevel!

if !RETRY_ERR! EQU 0 (
    echo         [완료] %~1 (재시도 성공)
    >> "%LOG_FILE%" echo   재시도 성공 (errorlevel=0): %TIME%
    set /a INSTALL_COUNT+=1
    >> "%REPORT_FILE%.tmp" echo   [성공] %~1 (재시도)
    goto :eof
)

winget list --id %~2 --source winget >nul 2>&1
if not errorlevel 1 (
    if "!UPGRADE_MODE!"=="upgrade" (
        winget upgrade --id %~2 --source winget --accept-source-agreements --accept-package-agreements --silent >nul 2>&1
        echo         [업그레이드] %~1
        >> "%LOG_FILE%" echo   결과: 업그레이드
        set /a INSTALL_COUNT+=1
        >> "%REPORT_FILE%.tmp" echo   [업그레이드] %~1
    ) else if "!UPGRADE_MODE!"=="remove" (
        winget uninstall --id %~2 --source winget --silent >nul 2>&1
        echo         [제거] %~1
        >> "%LOG_FILE%" echo   결과: 제거
        set /a SKIP_COUNT+=1
        >> "%REPORT_FILE%.tmp" echo   [제거] %~1
    ) else (
        echo         [건너뜀] %~1 (이미 설치됨)
        >> "%LOG_FILE%" echo   결과: 건너뜀
        set /a SKIP_COUNT+=1
        >> "%REPORT_FILE%.tmp" echo   [건너뜀] %~1
    )
) else (
    echo         [건너뜀] %~1 설치 실패 → 나중에 수동 설치
    >> "%LOG_FILE%" echo   재시도 실패 (errorlevel=!RETRY_ERR!): %TIME%
    set /a FAIL_COUNT+=1
    >> "%REPORT_FILE%.tmp" echo   [실패] %~1
)
goto :eof

:: ============================================================
:: Post-install: 왕초보 (Git autocrlf, pip 업그레이드, npm fund)
:: ============================================================
:POST_BEGINNER
echo.
echo  ---------------------------------------------------
echo  [설치 후 자동 설정]
echo.

:: Git autocrlf 자동 설정 (Windows 줄바꿈 표준, 첫 커밋 오류 예방)
where git >nul 2>&1
if not errorlevel 1 (
    git config --global core.autocrlf true >nul 2>&1
    >> "%LOG_FILE%" echo POST: git config --global core.autocrlf true 완료
    echo  [자동] Git 줄바꿈 설정 완료 (autocrlf=true)
    echo.
    echo  ★ Git 사용자 정보는 직접 설정이 필요합니다:
    echo.
    echo      git config --global user.name  "홍길동"
    echo      git config --global user.email "your@email.com"
    echo.
)

:: pip 업그레이드 자동 실행 (pip 경고 제거)
where python >nul 2>&1
if not errorlevel 1 (
    python -m pip install --upgrade pip >nul 2>&1
    >> "%LOG_FILE%" echo POST: pip upgrade 완료
    echo  [자동] pip 업그레이드 완료
)

:: npm 광고 메시지 제거 (초보자 혼란 방지)
where npm >nul 2>&1
if not errorlevel 1 (
    npm config set fund false >nul 2>&1
    npm install -g @anthropic-ai/claude-code >nul 2>&1
    >> "%LOG_FILE%" echo POST: Claude Code CLI 설치 완료
    echo  [자동] Claude Code CLI 설치 완료 (새 터미널: claude --version)
    >> "%LOG_FILE%" echo POST: npm config set fund false 완료
    echo  [자동] npm 광고 메시지 제거 완료
)
echo.
goto :eof

:: ============================================================
:: Post-install: 중급 (Ollama 모델 안내 ? 자동 다운로드 금지)
:: ============================================================
:POST_INTERMEDIATE
where ollama >nul 2>&1
if not errorlevel 1 (
    echo  ★ Ollama 로컬 AI 모델 안내 (2GB 이상 ? 직접 실행):
    echo.
    echo      ollama pull llama3.2   (약 2GB)
    echo      ollama pull gemma3     (약 3GB)
    echo.
)

echo  [자동] 배포/DB CLI 도구 npm 설치 중...
call :NPM_INSTALL "Vercel CLI" "vercel"
call :NPM_INSTALL "Supabase CLI" "supabase"
call :NPM_INSTALL "Stripe SDK" "stripe"
call :NPM_INSTALL "Resend SDK" "resend"
goto :eof

:: ============================================================
:: Post-install: 고급 (Rust toolchain, VS Code 확장 URL 안내)
:: ============================================================
:POST_ADVANCED
where rustup >nul 2>&1
if not errorlevel 1 (
    rustup update stable >nul 2>&1
    >> "%LOG_FILE%" echo POST: rustup update stable 완료
    echo  [자동] Rust toolchain 업데이트 완료
    echo.
)

echo  ★ VS Code 확장 프로그램 (직접 설치):
echo.
echo      Python:   https://marketplace.visualstudio.com/items?itemName=ms-python.python
echo      Prettier: https://marketplace.visualstudio.com/items?itemName=esbenp.prettier-vscode
echo.

echo  [자동] 고급 배포 CLI 설치 중...
call :NPM_INSTALL "Railway CLI" "@railway/cli"
goto :eof

:: ============================================================
:: 리포트 생성 2종 (요약 + 상세)
:: ============================================================
:MAKE_REPORTS
set END_TIME=%TIME%

if not exist "%REPORT_FILE%.tmp" >> "%REPORT_FILE%.tmp" echo   (설치 항목 없음)

:: 강사용 요약 리포트
(
    echo ====================================================
    echo  바이브코딩 환경 키트 - 설치 리포트
    echo ====================================================
    echo  PC 이름:    %COMPUTERNAME%
    echo  설치 레벨:  %LEVEL_NAME%
    echo  설치 날짜:  %DATE%
    echo  시작 시각:  %START_TIME%
    echo  완료 시각:  %END_TIME%
    echo  성공: %INSTALL_COUNT%개  건너뜀: %SKIP_COUNT%개  실패: %FAIL_COUNT%개
    echo ====================================================
    type "%REPORT_FILE%.tmp"
    echo ====================================================
    echo  이 파일을 강사에게 전달하면 설치 상태를 파악할 수 있습니다.
    echo ====================================================
) > "%REPORT_FILE%"

del "%REPORT_FILE%.tmp" >nul 2>&1

>> "%LOG_FILE%" echo.
>> "%LOG_FILE%" echo === 설치 완료: %END_TIME% ===
>> "%LOG_FILE%" echo 성공: %INSTALL_COUNT% / 건너뜀: %SKIP_COUNT% / 실패: %FAIL_COUNT%

echo.
echo  [리포트 저장 완료] 아래 파일을 강사에게 전달해 주세요:
echo    %REPORT_FILE%  (강사용 요약)
echo    %LOG_FILE%     (디버깅용 상세)
goto :eof

:: ============================================================
:: PATH 검증 출력 (설치 완료 후 눈으로 확인)
:: ============================================================
:PATH_CHECK
echo.
echo  ---------------------------------------------------
echo  [PATH 검증] 현재 터미널에서 인식되는 도구
echo  ---------------------------------------------------
for %%c in (git python node npm pnpm bun go rustc rustup flutter dart java gh pwsh ruby php cursor) do (
    where %%c >nul 2>&1
    if not errorlevel 1 echo    [O] %%c
)
echo.
goto :eof

:: ============================================================
:: 설치 완료 메시지
:: ============================================================
:DONE_MSG
echo  ---------------------------------------------------
if !FAIL_COUNT! GTR 0 (
    echo  [주의] 일부 도구 설치 실패: !FAIL_COUNT!개
    echo         %LOG_FILE% 를 강사에게 전달하세요.
    echo.
)
echo  설치가 완료되었습니다!
echo.
echo  [다음 단계 가이드]
echo   1. 새 터미널 열기 (시작메뉴 -> Windows Terminal 또는 PowerShell)
echo   2. git --version / python --version / node --version 입력 확인
echo   3. git config --global user.name "홍길동" 형식으로 이름 설정
echo   4. git config --global user.email "my@email.com" 형식으로 이메일 설정
echo   5. 각 도구 설치 확인: [9] 설치 확인 메뉴 이용
echo.
echo  --- 주요 CLI 버전 확인 ---
echo   vercel --version
echo   supabase --version
echo   npx prisma --version
echo   claude --version
echo.
echo  새 터미널을 열어서 시작하세요.
echo  (현재 창은 PATH 변경 전 상태입니다)
echo.
pause
goto :eof

:: ============================================================
:: 선택 설치
:: ============================================================
:: 선택 설치
:: ============================================================
:DO_SELECT
cls
echo.
echo  [선택 설치] 원하는 번호를 쉼표로 입력하세요  (예: 1,3,6)
echo  ---------------------------------------------------
echo.
echo  [ 기본 도구 ]
echo    [1]  Git           [2]  Python 3     [3]  Node.js LTS
echo    [4]  VS Code       [5]  WinTerminal   [6]  GitHub CLI
echo    [7]  PowerShell 7  [8]  pnpm          [9]  Ollama
echo    [10] Bun
echo.
echo  [ 언어 / 런타임 ]
echo    [11] Java 21 LTS   [12] Flutter       [13] Go
echo    [14] Rust
echo.
echo  [ 올인원 ]
echo    [15] Ruby          [16] PHP
echo.
echo  [ 추가 도구 (winget) ]
echo    [17] Git LFS       [18] Stripe CLI
echo.
echo  [ 배포 / DB CLI (npm) ]
echo    [19] Vercel CLI    [20] Supabase CLI  [21] Stripe SDK
echo    [22] Resend SDK    [23] Railway CLI
echo.
echo  [ 프로젝트별 선택 (npm) ]
echo    [24] Clerk         [25] Prisma        [26] Uploadthing
echo         * 24=Supabase Auth 사용시 불필요  25=DB ORM  26=파일업로드
echo.
echo  ---------------------------------------------------
echo    0 = 메인 메뉴로
echo.
set /p SEL="  번호 입력: "
if "!SEL!"=="0" goto MAIN_MENU
if "!SEL!"=="" goto DO_SELECT

echo.
echo  선택: !SEL!
set /p CONFIRM_SEL="  Y=설치 시작 / N=다시 선택: "
if /i "!CONFIRM_SEL!" NEQ "y" goto DO_SELECT
echo.
echo  이미 설치된 도구 처리 방법:
echo    [1] 건너뜀    (현재 버전 유지)
echo    [2] 업그레이드 (최신 버전으로)
echo    [3] 제거       (삭제만)
set /p UPGRADE_CHOICE="  선택 (기본값=1): "
if "!UPGRADE_CHOICE!"=="" set UPGRADE_CHOICE=1
if "!UPGRADE_CHOICE!"=="2" (set UPGRADE_MODE=upgrade) else (
if "!UPGRADE_CHOICE!"=="3" (set UPGRADE_MODE=remove)  else (
set UPGRADE_MODE=skip))

set LEVEL_NAME=선택설치
set TOTAL=0
set CURRENT=0
set INSTALL_COUNT=0
set SKIP_COUNT=0
set FAIL_COUNT=0
del "%REPORT_FILE%.tmp" >nul 2>&1

for %%n in (!SEL:,= !) do set /a TOTAL+=1

>> "%LOG_FILE%" echo.
>> "%LOG_FILE%" echo === 선택 설치 목록: !SEL! ===

:: pnpm(8), Bun(10), npm 도구(19-26) -> Node.js 선행 설치
set NEED_NODE=
echo !SEL! | findstr /C:"8" >nul 2>&1
if not errorlevel 1 set NEED_NODE=1
echo !SEL! | findstr /C:"10" >nul 2>&1
if not errorlevel 1 set NEED_NODE=1
for %%x in (19 20 21 22 23 24 25 26) do (
    echo !SEL! | findstr /C:"%%x" >nul 2>&1
    if not errorlevel 1 set NEED_NODE=1
)
if defined NEED_NODE (
    where node >nul 2>&1
    if errorlevel 1 (
        echo  [안내] Node.js가 필요합니다. 먼저 설치합니다.
        set /a TOTAL+=1
        call :INSTALL "Node.js LTS" "OpenJS.NodeJS.LTS"
    )
)
set NEED_NODE=

:: Flutter(12) -> Java 21 선행 설치
echo !SEL! | findstr /C:"12" >nul 2>&1
if not errorlevel 1 (
    where java >nul 2>&1
    if errorlevel 1 (
        echo  [안내] Flutter는 Java 21이 필요합니다. 먼저 설치합니다.
        set /a TOTAL+=1
        call :INSTALL "Java 21 LTS" "EclipseAdoptium.Temurin.21.JDK"
    )
)

for %%n in (!SEL:,= !) do (
    if "%%n"=="1"  call :INSTALL "Git" "Git.Git"
    if "%%n"=="2"  call :INSTALL "Python 3" "Python.Python.3"
    if "%%n"=="3"  call :INSTALL "Node.js LTS" "OpenJS.NodeJS.LTS"
    if "%%n"=="4"  call :INSTALL "VS Code" "Microsoft.VisualStudioCode"
    if "%%n"=="5"  call :INSTALL "Windows Terminal" "Microsoft.WindowsTerminal"
    if "%%n"=="6"  call :INSTALL "GitHub CLI" "GitHub.cli"
    if "%%n"=="7"  call :INSTALL "PowerShell 7" "Microsoft.PowerShell"
    if "%%n"=="8"  call :INSTALL "pnpm" "pnpm.pnpm"
    if "%%n"=="9"  call :INSTALL "Ollama" "Ollama.Ollama"
    if "%%n"=="10" call :INSTALL "Bun" "Oven-sh.Bun"
    if "%%n"=="11" call :INSTALL "Java 21 LTS" "EclipseAdoptium.Temurin.21.JDK"
    if "%%n"=="12" call :INSTALL "Flutter+Dart" "Google.FlutterSDK"
    if "%%n"=="13" call :INSTALL "Go" "GoLang.Go"
    if "%%n"=="14" call :INSTALL "Rust" "Rustlang.Rustup"
    if "%%n"=="15" call :INSTALL "Ruby" "RubyInstallerTeam.RubyWithDevKit.3.3"
    if "%%n"=="16" call :INSTALL "PHP" "PHP.PHP"
    if "%%n"=="17" call :INSTALL "Git LFS" "GitHub.GitLFS"
    if "%%n"=="18" call :INSTALL "Stripe CLI" "Stripe.StripeCLI"
    if "%%n"=="19" call :NPM_INSTALL "Vercel CLI" "vercel"
    if "%%n"=="20" call :NPM_INSTALL "Supabase CLI" "supabase"
    if "%%n"=="21" call :NPM_INSTALL "Stripe SDK" "stripe"
    if "%%n"=="22" call :NPM_INSTALL "Resend SDK" "resend"
    if "%%n"=="23" call :NPM_INSTALL "Railway CLI" "@railway/cli"
    if "%%n"=="24" call :NPM_INSTALL "Clerk" "@clerk/clerk-sdk-node"
    if "%%n"=="25" call :NPM_INSTALL "Prisma" "prisma"
    if "%%n"=="26" call :NPM_INSTALL "Uploadthing" "uploadthing"
)

call :MAKE_REPORTS
call :PATH_CHECK
call :DONE_MSG
goto MAIN_MENU

:DO_UPDATE
cls
echo.
echo  [업데이트] 설치된 모든 도구를 최신 버전으로 업데이트합니다.
echo.
>> "%LOG_FILE%" echo === 전체 업데이트 시작: %TIME% ===

winget upgrade --all --source winget --accept-source-agreements --accept-package-agreements

>> "%LOG_FILE%" echo 전체 업데이트 완료: %TIME%
echo.
echo  [완료] 업데이트 완료.
pause
goto MAIN_MENU

:: ============================================================
:: 제거
:: ============================================================
:DO_REMOVE
cls
echo.
echo  [제거 메뉴]
echo    [1] 개별 도구 제거
echo    [2] 전체 제거
echo    [0] 메인 메뉴
echo.
echo  * 0 = 메인 메뉴로 돌아가기
set /p REM_CHOICE="  번호: "
if "!REM_CHOICE!"=="0" goto MAIN_MENU
if "!REM_CHOICE!"=="1" goto REMOVE_ONE
if "!REM_CHOICE!"=="2" goto REMOVE_ALL
goto DO_REMOVE

:REMOVE_ONE
cls
echo.
echo  [개별 제거] 제거할 도구 번호를 입력하세요
echo.
echo  [1]Git  [2]Python  [3]Node.js  [4]VSCode  [5]WinTerminal
echo  [6]GitHub CLI  [7]PS7  [8]pnpm  [9]Ollama  [10]Bun
echo  [11]Java21  [12]Flutter  [13]Go  [14]Rust  [15]Ruby  [16]PHP
echo  [0] 뒤로
echo.
set /p REM_SEL="  번호: "
if "!REM_SEL!"=="0"  goto DO_REMOVE

if "!REM_SEL!"=="1"  winget uninstall --id Git.Git --source winget --silent
if "!REM_SEL!"=="2"  winget uninstall --id Python.Python.3 --source winget --silent
if "!REM_SEL!"=="3"  winget uninstall --id OpenJS.NodeJS.LTS --source winget --silent
if "!REM_SEL!"=="4"  winget uninstall --id Microsoft.VisualStudioCode --source winget --silent
if "!REM_SEL!"=="5"  winget uninstall --id Microsoft.WindowsTerminal --source winget --silent
if "!REM_SEL!"=="6"  winget uninstall --id GitHub.cli --source winget --silent
if "!REM_SEL!"=="7"  winget uninstall --id Microsoft.PowerShell --source winget --silent
if "!REM_SEL!"=="8"  winget uninstall --id pnpm.pnpm --source winget --silent
if "!REM_SEL!"=="9"  winget uninstall --id Ollama.Ollama --source winget --silent
if "!REM_SEL!"=="10" winget uninstall --id Oven-sh.Bun --source winget --silent
if "!REM_SEL!"=="11" winget uninstall --id EclipseAdoptium.Temurin.21.JDK --source winget --silent
if "!REM_SEL!"=="12" winget uninstall --id Google.FlutterSDK --source winget --silent
if "!REM_SEL!"=="13" winget uninstall --id GoLang.Go --source winget --silent
if "!REM_SEL!"=="14" winget uninstall --id Rustlang.Rustup --source winget --silent
if "!REM_SEL!"=="15" winget uninstall --id RubyInstallerTeam.RubyWithDevKit.3.3 --source winget --silent
if "!REM_SEL!"=="16" winget uninstall --id PHP.PHP --source winget --silent

echo.
echo  [완료] 제거 완료.
pause
goto MAIN_MENU

:REMOVE_ALL
echo.
echo  [경고] 이 키트로 설치한 모든 도구를 제거합니다.
set /p REM_ALL_CONFIRM="  Y를 입력하면 진행합니다: "
if /i "!REM_ALL_CONFIRM!" NEQ "y" goto DO_REMOVE

echo  제거 중... (시간이 걸릴 수 있습니다)
for %%i in (
    PHP.PHP
    RubyInstallerTeam.RubyWithDevKit.3.3
    Google.FlutterSDK
    Rustlang.Rustup
    GoLang.Go
    EclipseAdoptium.Temurin.21.JDK
    Oven-sh.Bun
    pnpm.pnpm
    Ollama.Ollama
    Microsoft.PowerShell
    GitHub.cli
    Microsoft.WindowsTerminal
    Microsoft.VisualStudioCode
    OpenJS.NodeJS.LTS
    Python.Python.3
    Git.Git
) do (
    winget uninstall --id %%i --source winget --silent >nul 2>&1
    echo    제거: %%i
)
echo.
echo  [npm] npm 패키지 제거 중...
for %%p in (vercel supabase stripe resend @railway/cli @clerk/clerk-sdk-node prisma uploadthing) do (
    npm uninstall -g %%p >nul 2>&1
    echo    [npm] 제거: %%p
)
echo.
echo  [완료] 전체 제거 완료.
pause
goto MAIN_MENU

:: ============================================================
:: 수동 설치 안내 (Cursor 최우선)
:: ============================================================
:DO_MANUAL
cls
echo.
echo  [직접 다운로드 링크]
echo  winget 설치가 안 될 때 공식 사이트에서 직접 받으세요.
echo  ---------------------------------------------------
echo.
echo   --- 초보자 도구 ---
echo    [1]  Git               https://git-scm.com/download/win
echo    [2]  Python 3          https://www.python.org/downloads/
echo    [3]  Node.js LTS       https://nodejs.org/en/download
echo    [4]  VS Code           https://code.visualstudio.com/download
echo    [5]  Windows Terminal  https://aka.ms/terminal
echo.
echo   --- 중급 도구 ---
echo    [6]  GitHub CLI        https://cli.github.com/
echo    [7]  PowerShell 7      https://github.com/PowerShell/PowerShell/releases/latest
echo    [8]  pnpm              https://pnpm.io/installation
echo    [9]  Ollama            https://ollama.com/download/windows
echo    [10] Bun               https://bun.sh/
echo.
echo   --- 고급 도구 ---
echo    [11] Java 21 LTS       https://adoptium.net/
echo    [12] Flutter           https://docs.flutter.dev/get-started/install/windows
echo    [13] Go                https://go.dev/dl/
echo    [14] Rust              https://rustup.rs/
echo.
echo   --- 새로운 도구 ---
echo    [15] Ruby              https://rubyinstaller.org/downloads/
echo    [16] PHP               https://windows.php.net/download/
echo.
echo   --- AI 도구 (별도 설치 필요) ---
echo    [17] Cursor            https://cursor.com/ko/download
echo    [18] Claude Desktop    https://claude.com/ko-kr/download
echo    [19] GitHub Desktop    https://desktop.github.com/download/
echo.
echo   --- 개발 확장 CLI ---
echo    [20] GitHub LFS        https://git-lfs.com/
echo    [21] Stripe CLI        https://docs.stripe.com/stripe-cli
echo.
echo  ---------------------------------------------------
echo    [0] 메인 메뉴로
echo.
set /p MAN_CHOICE="  번호 입력: "
if "!MAN_CHOICE!"=="0" goto MAIN_MENU

set _OPENED=0
if "!MAN_CHOICE!"=="1"  start "" "https://git-scm.com/download/win"                              & set _OPENED=1
if "!MAN_CHOICE!"=="2"  start "" "https://www.python.org/downloads/"                              & set _OPENED=1
if "!MAN_CHOICE!"=="3"  start "" "https://nodejs.org/en/download"                                 & set _OPENED=1
if "!MAN_CHOICE!"=="4"  start "" "https://code.visualstudio.com/download"                         & set _OPENED=1
if "!MAN_CHOICE!"=="5"  start "" "https://aka.ms/terminal"                                        & set _OPENED=1
if "!MAN_CHOICE!"=="6"  start "" "https://cli.github.com/"                                        & set _OPENED=1
if "!MAN_CHOICE!"=="7"  start "" "https://github.com/PowerShell/PowerShell/releases/latest"       & set _OPENED=1
if "!MAN_CHOICE!"=="8"  start "" "https://pnpm.io/installation"                                   & set _OPENED=1
if "!MAN_CHOICE!"=="9"  start "" "https://ollama.com/download/windows"                            & set _OPENED=1
if "!MAN_CHOICE!"=="10" start "" "https://bun.sh/"                                                & set _OPENED=1
if "!MAN_CHOICE!"=="11" start "" "https://adoptium.net/"                                          & set _OPENED=1
if "!MAN_CHOICE!"=="12" start "" "https://docs.flutter.dev/get-started/install/windows"   & set _OPENED=1
if "!MAN_CHOICE!"=="13" start "" "https://go.dev/dl/"                                             & set _OPENED=1
if "!MAN_CHOICE!"=="14" start "" "https://rustup.rs/"                                             & set _OPENED=1
if "!MAN_CHOICE!"=="15" start "" "https://rubyinstaller.org/downloads/"                           & set _OPENED=1
if "!MAN_CHOICE!"=="16" start "" "https://windows.php.net/download/"                              & set _OPENED=1
if "!MAN_CHOICE!"=="17" start "" "https://cursor.com/ko/download"                                 & set _OPENED=1
if "!MAN_CHOICE!"=="18" start "" "https://claude.com/ko-kr/download"                              & set _OPENED=1
if "!MAN_CHOICE!"=="19" start "" "https://desktop.github.com/download/"                           & set _OPENED=1

if "!MAN_CHOICE!"=="20" start "" "https://git-lfs.com/"                                          & set _OPENED=1
if "!MAN_CHOICE!"=="21" start "" "https://docs.stripe.com/stripe-cli"                            & set _OPENED=1

if "!_OPENED!"=="1" echo. & echo  브라우저가 열렸습니다. 다운로드 후 설치하세요. & echo. & pause
goto DO_MANUAL
:: ============================================================
:: 설치 상태 확인 (O/X)
:: ============================================================
:DO_CHECK
cls
echo.
echo  [설치 상태 확인]
echo  ---------------------------------------------------
echo.

echo  [ 기본 개발 도구 ]
call :CHECK_ONE "Git" git
call :CHECK_ONE "Git LFS" git-lfs
call :CHECK_ONE "Python 3" python
call :CHECK_ONE "Node.js" node
call :CHECK_ONE "npm" npm
call :CHECK_ONE "VS Code" code
call :CHECK_ONE "Windows Terminal" wt
call :CHECK_ONE "GitHub CLI" gh
call :CHECK_ONE "PowerShell 7" pwsh
call :CHECK_ONE "pnpm" pnpm
call :CHECK_ONE "Ollama" ollama
call :CHECK_ONE "Bun" bun
echo.
echo  [ 언어 / 런타임 ]
call :CHECK_ONE "Java" java
where flutter >nul 2>&1
if errorlevel 1 (
    echo    [X] Flutter
) else (
    set _FV=
    for /f "tokens=2" %%v in ('flutter --version 2^>nul ^| findstr /B "Flutter"') do if not defined _FV set _FV=%%v
    if defined _FV (echo    [O] Flutter  !_FV!) else echo    [O] Flutter
)
call :CHECK_ONE "Dart" dart
call :CHECK_ONE "Go" go
call :CHECK_ONE "Rust" rustc
call :CHECK_ONE "Cargo" cargo
call :CHECK_ONE "Ruby" ruby
call :CHECK_ONE "PHP" php
echo.
echo  [ 배포 / DB CLI ]
call :CHECK_ONE "Stripe CLI" stripe
call :CHECK_ONE "Vercel CLI" vercel
call :CHECK_ONE "Supabase CLI" supabase
call :CHECK_ONE "Railway CLI" railway
call :CHECK_ONE "Prisma" prisma
echo.
echo  [ AI 에디터 ]
call :CHECK_ONE "Cursor" cursor
call :CHECK_ONE "Claude Code CLI" claude

echo.
echo  ---------------------------------------------------
echo  새 터미널에서 확인 시 더 정확한 결과가 나옵니다.
pause
goto MAIN_MENU

:: %~1 = 표시 이름, %~2 = 실행파일명
:CHECK_ONE
where %~2 >nul 2>&1
if errorlevel 1 (
    echo    [X] %~1
    goto :eof
)
set CHK_VER=
for /f "tokens=*" %%v in ('%~2 --version 2^>nul') do if not defined CHK_VER set CHK_VER=%%v
if defined CHK_VER (
    echo    [O] %~1  !CHK_VER!
) else (
    echo    [O] %~1
)
goto :eof

:: ============================================================
:: 종료
:: ============================================================
:DO_EXIT
echo.
echo  바이브코딩 환경 키트를 종료합니다.
echo  좋은 바이브코딩 되세요!
echo.
pause
exit /b 0
