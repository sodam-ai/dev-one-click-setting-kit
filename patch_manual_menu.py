# -*- coding: utf-8 -*-
import shutil

BAT_PATH = r"D:\AI_Dev_Work\2026y\26y_04m_22d_dev-one-click-setting-kit\dev-one-click-setting-kit.bat"
shutil.copy(BAT_PATH, BAT_PATH + '.bak')

with open(BAT_PATH, 'r', encoding='cp949') as f:
    content = f.read()

changes = []

# ── 1. 메인 메뉴 [8] 레이블 업데이트
old_menu8 = 'echo    [8] 수동 설치      Cursor, Claude Desktop 등 다운로드'
new_menu8 = 'echo    [8] 직접 다운로드  공식 사이트 URL 목록 (winget 불가 시)'
if old_menu8 in content:
    content = content.replace(old_menu8, new_menu8, 1)
    changes.append('메인메뉴 [8] 레이블')
    print('  [OK] 메인메뉴 [8] 레이블 업데이트')
else:
    print('  [!!] 메인메뉴 [8] 레이블 미발견')

# ── 2. DO_MANUAL 섹션 전체 교체
s = content.find(':DO_MANUAL\n')
e = content.find('\n:: ============================================================', s + 1)

if s == -1 or e == -1:
    print('  [!!] DO_MANUAL 섹션 경계 미발견')
else:
    new_section = ''':DO_MANUAL
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
echo    [12] Flutter           https://flutter.dev/docs/get-started/install/windows/desktop
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
if "!MAN_CHOICE!"=="12" start "" "https://flutter.dev/docs/get-started/install/windows/desktop"   & set _OPENED=1
if "!MAN_CHOICE!"=="13" start "" "https://go.dev/dl/"                                             & set _OPENED=1
if "!MAN_CHOICE!"=="14" start "" "https://rustup.rs/"                                             & set _OPENED=1
if "!MAN_CHOICE!"=="15" start "" "https://rubyinstaller.org/downloads/"                           & set _OPENED=1
if "!MAN_CHOICE!"=="16" start "" "https://windows.php.net/download/"                              & set _OPENED=1
if "!MAN_CHOICE!"=="17" start "" "https://cursor.com/ko/download"                                 & set _OPENED=1
if "!MAN_CHOICE!"=="18" start "" "https://claude.com/ko-kr/download"                              & set _OPENED=1
if "!MAN_CHOICE!"=="19" start "" "https://desktop.github.com/download/"                           & set _OPENED=1

if "!_OPENED!"=="1" echo. & echo  브라우저가 열렸습니다. 다운로드 후 설치하세요. & echo. & pause
goto DO_MANUAL'''

    content = content[:s] + new_section + content[e:]
    changes.append('DO_MANUAL 섹션 전체 교체')
    print('  [OK] DO_MANUAL 섹션 교체 완료 (19개 URL)')

with open(BAT_PATH, 'w', encoding='cp949') as f:
    f.write(content)

print(f'\n완료: {len(changes)}개 변경 적용')
for c in changes:
    print(f'  - {c}')
