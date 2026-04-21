# -*- coding: utf-8 -*-
"""
DEV-KIT v1.1.0 upgrade patch
모든 13개 수정사항을 단일 스크립트로 일괄 적용
BAT 파일: CP949 인코딩 (Edit 도구 직접 수정 불가 → Python 우회)
"""
import shutil
import os
import re

BAT_PATH = r"D:\AI_Dev_Work\2026y\26y_04m_22d_dev-one-click-setting-kit\dev-one-click-setting-kit.bat"
BASE     = r"D:\AI_Dev_Work\2026y\26y_04m_22d_dev-one-click-setting-kit"

# ── 백업 ──────────────────────────────────────────────────────
shutil.copy(BAT_PATH, BAT_PATH + '.bak')
print("[백업] OK:", BAT_PATH + '.bak')

with open(BAT_PATH, 'r', encoding='cp949') as f:
    content = f.read()

changes = []
warnings = []

def patch(name, old, new):
    global content
    if old in content:
        content = content.replace(old, new, 1)
        changes.append(name)
        print(f"  [OK] {name}")
        return True
    warnings.append(name)
    print(f"  [!!] WARNING: {name} - 패턴 미발견")
    return False

# ============================================================
# B1: findstr 오탐 수정 (778-785줄)
#   echo !SEL! | findstr /C:"8" 는 "18", "28" 도 매칭 → 오작동
#   for 이중 루프로 토큰 단위 정확 비교로 교체
# ============================================================
patch('B1: findstr 오탐 수정',
    'echo !SEL! | findstr /C:"8" >nul 2>&1\n'
    'if not errorlevel 1 set NEED_NODE=1\n'
    'echo !SEL! | findstr /C:"10" >nul 2>&1\n'
    'if not errorlevel 1 set NEED_NODE=1\n'
    'for %%x in (19 20 21 22 23 24 25 26) do (\n'
    '    echo !SEL! | findstr /C:"%%x" >nul 2>&1\n'
    '    if not errorlevel 1 set NEED_NODE=1\n'
    ')',
    'for %%n in (8 10 19 20 21 22 23 24 25 26) do (\n'
    '    for %%s in (!SEL!) do if "%%s"=="%%n" set NEED_NODE=1\n'
    ')'
)

# ============================================================
# B2: 디스크 여유 공간 체크 삽입 (124줄 이후)
#   인터넷 체크 블록 종료 직후, Node.js 버전 체크 전에 삽입
#   PowerShell로 C드라이브 여유 공간 조회, 3GB 미만 경고
# ============================================================
patch('B2: 디스크 공간 체크 삽입',
    '    >> "%LOG_FILE%" echo OK: 인터넷 연결\n'
    ')\n'
    '\n'
    ':: 5.',
    '    >> "%LOG_FILE%" echo OK: 인터넷 연결\n'
    ')\n'
    '\n'
    ':: 디스크 여유 공간 체크 (3GB 미만 경고)\n'
    'powershell -nologo -command "if ((Get-PSDrive C).Free/1GB -lt 3) { exit 1 }" >nul 2>&1\n'
    'if errorlevel 1 (\n'
    '    echo  [경고] C드라이브 여유 공간 3GB 미만 - 설치 중 실패할 수 있습니다.\n'
    '    set /p CONT_DISK="  계속하시겠습니까? (y/n): "\n'
    '    if /i "!CONT_DISK!" NEQ "y" goto MAIN_MENU\n'
    ') else (\n'
    '    echo  [OK] 디스크 여유 공간 확인\n'
    ')\n'
    '\n'
    ':: 5.'
)

# ============================================================
# B3: timeout /nobreak 추가 (495줄, :INSTALL 서브루틴)
#   /nobreak 없으면 Ctrl+C 로 대기 스킵 → 재시도 무력화
# ============================================================
patch('B3: timeout /nobreak 추가',
    'timeout /t 5 >nul\n'
    '\n'
    'winget install --id %~2 --source winget --accept-source-agreements --accept-package-agreements --silent >nul 2>&1\n'
    'set RETRY_ERR=!errorlevel!',
    'timeout /t 5 /nobreak >nul\n'
    '\n'
    'winget install --id %~2 --source winget --accept-source-agreements --accept-package-agreements --silent >nul 2>&1\n'
    'set RETRY_ERR=!errorlevel!'
)

# ============================================================
# B4a: 카운터 echo 수정 (330줄) — LEVEL_3: 15→16
#   Stripe CLI 포함 실제 설치 항목 수와 불일치
# ============================================================
patch('B4a: 카운터 15->16 (LEVEL_3)',
    'echo  [고급 설치] 15개 도구를 설치합니다.',
    'echo  [고급 설치] 16개 도구를 설치합니다.'
)

# ============================================================
# B4b: 카운터 echo 수정 (367줄) — LEVEL_4: 17→18
# ============================================================
patch('B4b: 카운터 17->18 (LEVEL_4)',
    'echo  [올인원 설치] 17개 도구를 설치합니다.',
    'echo  [올인원 설치] 18개 도구를 설치합니다.'
)

# ============================================================
# B5: PATH_CHECK에서 cursor 제거 (668줄)
#   cursor는 winget 설치 후 PATH에 자동 등록되지 않음 → 항상 [X] 오탐
# ============================================================
patch('B5: PATH_CHECK cursor 제거',
    'for %%c in (git python node npm pnpm bun go rustc rustup flutter dart java gh pwsh ruby php cursor) do (',
    'for %%c in (git python node npm pnpm bun go rustc rustup flutter dart java gh pwsh ruby php) do ('
)

# ============================================================
# S1: DO_UPDATE — winget upgrade --all → 18개 도구 개별 업그레이드
#   이유: --all 은 OS 컴포넌트 포함 전체 패키지 업그레이드 → 의도치 않은 시스템 변경
# ============================================================
patch('S1: DO_UPDATE 개별 업그레이드 교체',
    'winget upgrade --all --source winget --accept-source-agreements --accept-package-agreements',
    'for %%p in ('
    'Git.Git GitHub.GitLFS Python.Python.3 OpenJS.NodeJS.LTS GitHub.cli '
    'Microsoft.PowerShell pnpm.pnpm Oven-sh.Bun Ollama.Ollama '
    'Microsoft.VisualStudioCode Microsoft.WindowsTerminal '
    'EclipseAdoptium.Temurin.21.JDK GoLang.Go Rustlang.Rustup '
    'Google.FlutterSDK Stripe.StripeCLI '
    'RubyInstallerTeam.RubyWithDevKit.3.3 PHP.PHP'
    ') do (\n'
    '    winget upgrade --id %%p --source winget --accept-source-agreements --accept-package-agreements --silent >nul 2>&1\n'
    '    if not errorlevel 1 echo  [업그레이드] %%p\n'
    ')'
)

# ============================================================
# S2a: DO_MANUAL — Antigravity 메뉴 항목 제거 (963줄)
# ============================================================
patch('S2a: Antigravity 메뉴 항목 제거',
    'echo    [4] Antigravity      https://antigravity.google/download\n',
    ''
)

# ============================================================
# S2b: DO_MANUAL — Antigravity start 명령 제거 (975줄)
# ============================================================
patch('S2b: Antigravity start 명령 제거',
    'if "!MAN_CHOICE!"=="4" start "" "https://antigravity.google/download"\n',
    ''
)

# ============================================================
# S2c: DO_MANUAL — Antigravity echo/pause 제거 (980줄)
#   regex 사용: "4" 선택의 브라우저 안내 메시지 라인
# ============================================================
count = len(re.findall(r'if "!MAN_CHOICE!"=="4" echo\.', content))
if count == 1:
    content = re.sub(r'if "!MAN_CHOICE!"=="4" echo\..*\n', '', content)
    changes.append('S2c: Antigravity echo/pause 제거')
    print('  [OK] S2c: Antigravity echo/pause 제거')
elif count == 0:
    warnings.append('S2c: Antigravity echo/pause 제거')
    print('  [!!] WARNING: S2c — 패턴 미발견')
else:
    warnings.append('S2c: Antigravity echo/pause 제거 (다중 매칭)')
    print(f'  [!!] WARNING: S2c — {count}개 매칭, 건너뜀')

# ============================================================
# U1: ANSI 색상 코드 초기화 삽입 (set UPGRADE_MODE=skip 직후)
#   Windows 10+ 가상 터미널 시퀀스 활성화 → 색상 echo 가능
# ============================================================
patch('U1: ANSI 초기화 삽입',
    'set START_TIME=%TIME%\n'
    'set UPGRADE_MODE=skip\n'
    '\n',
    'set START_TIME=%TIME%\n'
    'set UPGRADE_MODE=skip\n'
    '\n'
    ':: ANSI 색상 코드 활성화 (Windows 10+)\n'
    'reg add HKCU\\Console /v VirtualTerminalLevel /t REG_DWORD /d 1 /f >nul 2>&1\n'
    '\n'
)

# ============================================================
# U2: POST_INTERMEDIATE npm 4종 — 자동 설치 → Y/N 선택 설치
#   Vercel/Supabase/Stripe/Resend 필요 없는 사용자는 설치 건너뜀
# ============================================================
patch('U2: npm Y/N 확인 프롬프트 추가',
    'call :NPM_INSTALL "Vercel CLI" "vercel"\n'
    'call :NPM_INSTALL "Supabase CLI" "supabase"\n'
    'call :NPM_INSTALL "Stripe SDK" "stripe"\n'
    'call :NPM_INSTALL "Resend SDK" "resend"',
    'set /p INST_VERCEL="  Vercel CLI 설치할까요? (y/n): "\n'
    'if /i "!INST_VERCEL!"=="y" call :NPM_INSTALL "Vercel CLI" "vercel"\n'
    'set /p INST_SUPABASE="  Supabase CLI 설치할까요? (y/n): "\n'
    'if /i "!INST_SUPABASE!"=="y" call :NPM_INSTALL "Supabase CLI" "supabase"\n'
    'set /p INST_STRIPE="  Stripe SDK 설치할까요? (y/n): "\n'
    'if /i "!INST_STRIPE!"=="y" call :NPM_INSTALL "Stripe SDK" "stripe"\n'
    'set /p INST_RESEND="  Resend SDK 설치할까요? (y/n): "\n'
    'if /i "!INST_RESEND!"=="y" call :NPM_INSTALL "Resend SDK" "resend"'
)

# ============================================================
# U3: MAKE_REPORTS 소요시간 계산 표시 (626줄 이후)
#   START_TIME ~ END_TIME 차이를 분/초로 계산해 출력
# ============================================================
patch('U3: 소요시간 계산 삽입',
    ':MAKE_REPORTS\n'
    'set END_TIME=%TIME%\n'
    '\n',
    ':MAKE_REPORTS\n'
    'set END_TIME=%TIME%\n'
    '\n'
    ':: 소요 시간 계산\n'
    'for /f "tokens=1-3 delims=:." %%a in ("%START_TIME: =0%") do set /a _SS=%%a*3600+%%b*60+%%c\n'
    'for /f "tokens=1-3 delims=:." %%a in ("%END_TIME: =0%") do set /a _ES=%%a*3600+%%b*60+%%c\n'
    'set /a _EL=_ES-_SS\n'
    'if !_EL! LSS 0 set /a _EL+=86400\n'
    'set /a _EM=_EL/60\n'
    'set /a _EL_S=_EL %% 60\n'
    'echo  소요 시간: !_EM!분 !_EL_S!초\n'
    '>> "%LOG_FILE%" echo 소요 시간: !_EM!분 !_EL_S!초\n'
    '\n'
)

# ============================================================
# BAT 파일 저장
# ============================================================
with open(BAT_PATH, 'w', encoding='cp949') as f:
    f.write(content)
print(f"\n[저장] BAT 파일 업데이트 완료")

# ============================================================
# R1: fix 스크립트 6개 삭제
# ============================================================
fix_files = ['fix6b.py', 'fix6c.py', 'fix7.py', 'fix8.py', 'fix9.py', 'upgrade6.py']
deleted = []
for fname in fix_files:
    fpath = os.path.join(BASE, fname)
    if os.path.exists(fpath):
        os.remove(fpath)
        deleted.append(fname)
if deleted:
    changes.append(f'R1: fix 스크립트 삭제 ({", ".join(deleted)})')
    print(f'  [OK] R1: 삭제 완료 - {", ".join(deleted)}')
else:
    print('  [!!] WARNING: R1 — 삭제할 파일 없음')

# ============================================================
# R2: CHANGELOG.md v1.1.0 섹션 추가
# ============================================================
CHANGELOG_PATH = os.path.join(BASE, 'CHANGELOG.md')
with open(CHANGELOG_PATH, 'r', encoding='utf-8') as f:
    cl = f.read()

if '[v1.1.0]' not in cl:
    v110 = (
        '\n'
        '## [v1.1.0] - 2026-04-22\n'
        '\n'
        '### Fixed\n'
        '\n'
        '- **B1** findstr 오탐 수정 — `findstr /C:"8"` 가 `18`·`28` 등에도 매칭되는 버그, for 이중 루프 정확 매칭으로 교체\n'
        '- **B2** 디스크 여유 공간 체크 추가 — C드라이브 3GB 미만 시 경고 및 중단 선택\n'
        '- **B3** `timeout /nobreak` 추가 — 재시도 대기 중 Ctrl+C 스킵 방지\n'
        '- **B4** 설치 카운터 수정 — LEVEL_3: 15→16개, LEVEL_4: 17→18개 (Stripe CLI 포함 누락)\n'
        '- **B5** PATH_CHECK `cursor` 제거 — winget PATH 미등록 항목 오탐 방지\n'
        '\n'
        '### Changed\n'
        '\n'
        '- **S1** 전체 업데이트 — `winget upgrade --all` → 키트 18개 도구 개별 업그레이드 (시스템 전체 변경 방지)\n'
        '- **S2** 수동 설치 메뉴 — Antigravity 항목 완전 제거 (메뉴·start·echo 포함)\n'
        '- **U1** ANSI 색상 코드 초기화 — Windows 10+ 가상 터미널 시퀀스 자동 활성화\n'
        '- **U2** npm 패키지 설치 방식 — 자동 일괄 설치 → Vercel/Supabase/Stripe/Resend 개별 Y/N 선택\n'
        '- **U3** 소요 시간 표시 — 완료 시 총 분/초 화면 출력 및 로그 기록\n'
        '\n'
        '### Removed\n'
        '\n'
        '- `fix6b.py` `fix6c.py` `fix7.py` `fix8.py` `fix9.py` `upgrade6.py` — 내부 패치 스크립트 삭제 (v1.1.0에 통합)\n'
        '\n'
    )
    insert_pos = cl.find('\n---\n') + 5
    cl = cl[:insert_pos] + v110 + cl[insert_pos:]
    with open(CHANGELOG_PATH, 'w', encoding='utf-8') as f:
        f.write(cl)
    changes.append('R2: CHANGELOG v1.1.0 추가')
    print('  [OK] R2: CHANGELOG v1.1.0 추가')
else:
    print('  [INFO] R2: CHANGELOG에 이미 v1.1.0 존재')

# ============================================================
# 결과 요약
# ============================================================
total = 13
print(f'\n{"=" * 52}')
print(f' DEV-KIT v1.1.0 패치 결과: {len(changes)}/{total} 적용')
print('=' * 52)
for i, c in enumerate(changes, 1):
    print(f'  {i:2d}. {c}')
if warnings:
    print(f'\n  경고 ({len(warnings)}개):')
    for w in warnings:
        print(f'    !! {w}')
print()
