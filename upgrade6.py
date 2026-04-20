# -*- coding: utf-8 -*-
# upgrade6.py - P1+P2 통합 반영
# 변경 5종:
#   1. DO_UPDATE: npm update -g 추가
#   2. PATH_CHECK: vercel/supabase/stripe/railway/prisma/claude/antigravity 추가
#   3. REMOVE_ONE: [17]GitLFS [18]StripeCLI + [19]-[26] npm uninstall 추가
#   4. REMOVE_ALL: Stripe.StripeCLI + GitHub.GitLFS + npm uninstall 추가
#   5. DONE_MSG: 치트시트 추가 + "Cursor 미설치 시 [8]" 문구 중립화
import sys

bat = r"D:\AI_Dev_Work\2026y\26y_04m_22d_One-click setting-file\DEV-KIT.bat"

with open(bat, 'rb') as f:
    raw = f.read()

content = raw.decode('cp949')
orig = content

def sub(old, new, label):
    global content
    if old not in content:
        print(f"[FAIL] {label}: 패턴 미발견")
        print(f"  찾는값: {repr(old[:120])}")
        sys.exit(1)
    content = content.replace(old, new, 1)
    print(f"[OK] {label}")

def sub_in(section, old, new, label):
    global content
    idx = content.find(section)
    if idx == -1:
        print(f"[FAIL] {label}: 섹션 미발견 '{section}'")
        sys.exit(1)
    tail = content[idx:]
    if old not in tail:
        print(f"[FAIL] {label}: 섹션 내 패턴 미발견")
        print(f"  찾는값: {repr(old[:120])}")
        sys.exit(1)
    content = content[:idx] + tail.replace(old, new, 1)
    print(f"[OK] {label}")

# ============================================================
# 1. DO_UPDATE: npm update -g 추가
# ============================================================
sub(
    'winget upgrade --all --source winget --accept-source-agreements --accept-package-agreements\r\n'
    '\r\n'
    '>> "%LOG_FILE%" echo',

    'winget upgrade --all --source winget --accept-source-agreements --accept-package-agreements\r\n'
    '\r\n'
    'echo.\r\n'
    'echo  [npm] npm \xc0\xfc\xc7\xb8 \xc6\xd0\xc5\xb0\xc1\xf6 \xbe\xf7\xb5\xa5\xc0\xcc\xc6\xae \xc1\xa4...\r\n'
    'npm update -g >nul 2>&1\r\n'
    'echo  [npm] \xbe\xf7\xb5\xa5\xc0\xcc\xc6\xae \xc644\xb8\xa3\xb7\xc1.\r\n'
    '\r\n'
    '>> "%LOG_FILE%" echo',

    'DO_UPDATE: npm update -g 추가'
)

# ============================================================
# 2. PATH_CHECK: for 루프 확장
# ============================================================
sub(
    'for %%c in (git python node npm pnpm bun go rustc rustup flutter dart java gh pwsh ruby php cursor) do (',

    'for %%c in (git python node npm pnpm bun go rustc rustup flutter dart java gh pwsh ruby php cursor vercel supabase stripe railway prisma claude antigravity) do (',

    'PATH_CHECK: CLI 7종 추가'
)

# ============================================================
# 3. REMOVE_ONE: [17]-[26] 추가
# ============================================================
sub(
    'if "!REM_SEL!"=="16" winget uninstall --id PHP.PHP --source winget --silent\r\n'
    '\r\n'
    'echo.',

    'if "!REM_SEL!"=="16" winget uninstall --id PHP.PHP --source winget --silent\r\n'
    'if "!REM_SEL!"=="17" winget uninstall --id GitHub.GitLFS --source winget --silent\r\n'
    'if "!REM_SEL!"=="18" winget uninstall --id Stripe.StripeCLI --source winget --silent\r\n'
    'if "!REM_SEL!"=="19" npm uninstall -g vercel >nul 2>&1\r\n'
    'if "!REM_SEL!"=="20" npm uninstall -g supabase >nul 2>&1\r\n'
    'if "!REM_SEL!"=="21" npm uninstall -g stripe >nul 2>&1\r\n'
    'if "!REM_SEL!"=="22" npm uninstall -g resend >nul 2>&1\r\n'
    'if "!REM_SEL!"=="23" npm uninstall -g @railway/cli >nul 2>&1\r\n'
    'if "!REM_SEL!"=="24" npm uninstall -g @clerk/clerk-sdk-node >nul 2>&1\r\n'
    'if "!REM_SEL!"=="25" npm uninstall -g prisma >nul 2>&1\r\n'
    'if "!REM_SEL!"=="26" npm uninstall -g uploadthing >nul 2>&1\r\n'
    '\r\n'
    'echo.',

    'REMOVE_ONE: [17]-[26] 추가'
)

# REMOVE_ONE 메뉴 echo 업데이트
sub(
    'echo  [1]Git  [2]Python  [3]Node.js  [4]VSCode  [5]WinTerminal\r\n'
    'echo  [6]GitHub CLI  [7]PS7  [8]pnpm  [9]Ollama  [10]Bun\r\n'
    'echo  [11]Java21  [12]Flutter  [13]Go  [14]Rust  [15]Ruby  [16]PHP\r\n'
    'echo  [0]',

    'echo  [1]Git    [2]Python   [3]Node.js  [4]VSCode     [5]WinTerminal\r\n'
    'echo  [6]GitHub CLI  [7]PS7  [8]pnpm  [9]Ollama  [10]Bun\r\n'
    'echo  [11]Java21  [12]Flutter  [13]Go  [14]Rust  [15]Ruby  [16]PHP\r\n'
    'echo  [17]GitLFS  [18]StripeCLI\r\n'
    'echo  [19]Vercel  [20]Supabase  [21]Stripe  [22]Resend  [23]Railway\r\n'
    'echo  [24]Clerk   [25]Prisma    [26]Uploadthing\r\n'
    'echo  [0]',

    'REMOVE_ONE: 메뉴 echo 업데이트'
)

# ============================================================
# 4. REMOVE_ALL: Stripe.StripeCLI + GitHub.GitLFS + npm uninstall 추가
# ============================================================
sub(
    '    PHP.PHP\r\n'
    '    RubyInstallerTeam.RubyWithDevKit.3.3\r\n'
    '    Google.FlutterSDK\r\n'
    '    Rustlang.Rustup\r\n'
    '    GoLang.Go\r\n'
    '    EclipseAdoptium.Temurin.21.JDK\r\n'
    '    Oven-sh.Bun\r\n'
    '    pnpm.pnpm\r\n'
    '    Ollama.Ollama\r\n'
    '    Microsoft.PowerShell\r\n'
    '    GitHub.cli\r\n'
    '    Microsoft.WindowsTerminal\r\n'
    '    Microsoft.VisualStudioCode\r\n'
    '    OpenJS.NodeJS.LTS\r\n'
    '    Python.Python.3\r\n'
    '    Git.Git\r\n'
    ') do (\r\n'
    '    winget uninstall --id %%i --source winget --silent >nul 2>&1\r\n'
    '    echo',

    '    Stripe.StripeCLI\r\n'
    '    GitHub.GitLFS\r\n'
    '    PHP.PHP\r\n'
    '    RubyInstallerTeam.RubyWithDevKit.3.3\r\n'
    '    Google.FlutterSDK\r\n'
    '    Rustlang.Rustup\r\n'
    '    GoLang.Go\r\n'
    '    EclipseAdoptium.Temurin.21.JDK\r\n'
    '    Oven-sh.Bun\r\n'
    '    pnpm.pnpm\r\n'
    '    Ollama.Ollama\r\n'
    '    Microsoft.PowerShell\r\n'
    '    GitHub.cli\r\n'
    '    Microsoft.WindowsTerminal\r\n'
    '    Microsoft.VisualStudioCode\r\n'
    '    OpenJS.NodeJS.LTS\r\n'
    '    Python.Python.3\r\n'
    '    Git.Git\r\n'
    ') do (\r\n'
    '    winget uninstall --id %%i --source winget --silent >nul 2>&1\r\n'
    '    echo',

    'REMOVE_ALL: Stripe.StripeCLI + GitHub.GitLFS 추가'
)

# REMOVE_ALL: npm uninstall 블록 추가
sub(
    '    winget uninstall --id %%i --source winget --silent >nul 2>&1\r\n'
    '    echo    \xc0\xa7\xc1\xa6: %%i\r\n'
    ')\r\n'
    'echo.\r\n'
    'echo  [\xc0\xcf\xb7\xae] \xc0\xfc\xc3\xbc \xc1\xa6\xb0\xf1 \xc0\xcf\xb7\xae.',

    '    winget uninstall --id %%i --source winget --silent >nul 2>&1\r\n'
    '    echo    \xc0\xa7\xc1\xa6: %%i\r\n'
    ')\r\n'
    'echo  [npm] npm \xc6\xa9\xb6\xb3\xc0\xce \xc1\xa6\xb0\xf1 \xc1\xa4...\r\n'
    'for %%p in (vercel supabase stripe resend @railway/cli @clerk/clerk-sdk-node prisma uploadthing) do (\r\n'
    '    npm uninstall -g %%p >nul 2>&1\r\n'
    '    echo    [npm] \xc0\xa7\xc1\xa6: %%p\r\n'
    ')\r\n'
    'echo.\r\n'
    'echo  [\xc0\xcf\xb7\xae] \xc0\xfc\xc3\xbc \xc1\xa6\xb0\xf1 \xc0\xcf\xb7\xae.',

    'REMOVE_ALL: npm uninstall 블록 추가'
)

# ============================================================
# 5. DONE_MSG: 치트시트 추가 + Cursor 문구 중립화
# ============================================================
# "Cursor 미설치 시 [8]..." 줄 제거/중립화
sub(
    'echo   5. Cursor \xb9\xcc\xbc\xb3\xc4\xa1 \xbd\xc3 [8] \xbc\xf6\xb5\xbf \xbc\xb3\xc4\xa1 \xb8\xde\xb4\xda\xbf\xa1\xbc\xad \xb4\xd9\xbf\xee\xb7\xce\xb5\xe5\r\n'
    'echo.\r\n'
    'echo  \xbb\xf5 \xc5\xcd\xb9\xcc\xb3\xca\xb8\xa6 \xbf\xad\xbe\xee \xbd\xc3\xc0\xcf\xc7\xcf\xbc\xbc\xbf\xe4.',

    'echo   5. \xb0\xa2 \xb5\xb5\xb1\xb8 \xb3\xfb\xb8\xa8\xb9\xd7 \xbc\xb3\xc4\xa1 \xc8\xae\xc0\xce: [9] \xbc\xb3\xc4\xa1 \xc8\xae\xc0\xce \xb8\xde\xb4\xda \xc0\xcc\xbf\xeb\r\n'
    'echo.\r\n'
    'echo  --- \xc4\xa1\xc6\xae\xbd\xc3\xc6\xae ---\r\n'
    'echo   vercel --version\r\n'
    'echo   supabase --version\r\n'
    'echo   npx prisma --version\r\n'
    'echo   claude --version\r\n'
    'echo.\r\n'
    'echo  \xbb\xf5 \xc5\xcd\xb9\xcc\xb3\xca\xb8\xa6 \xbf\xad\xbe\xee \xbd\xc3\xc0\xcf\xc7\xcf\xbc\xbc\xbf\xe4.',

    'DONE_MSG: 치트시트 + Cursor 문구 중립화'
)

# ============================================================
# 저장
# ============================================================
if content == orig:
    print('\n[경고] 변경사항 없음!')
    sys.exit(1)

result = content.encode('cp949')
with open(bat, 'wb') as f:
    f.write(result)

print(f'\n[완료] DEV-KIT.bat 업데이트 성공! ({len(raw)}→{len(result)} bytes)')
