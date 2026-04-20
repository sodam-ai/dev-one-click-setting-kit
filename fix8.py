# -*- coding: utf-8 -*-
# fix8.py - 이미 설치된 도구 처리 방법 선택 기능
#   1. DO_LEVEL_1~4: UPGRADE_MODE 선택 프롬프트 삽입 (4곳)
#   2. DO_SELECT: UPGRADE_MODE 선택 프롬프트 삽입
#   3. :INSTALL Block1 (첫 시도 실패 후) UPGRADE_MODE 분기
#   4. :INSTALL Block2 (재시도 실패 후) UPGRADE_MODE 분기
#   5. :NPM_INSTALL UPGRADE_MODE 분기
import re, sys

bat = r"D:\AI_Dev_Work\2026y\26y_04m_22d_One-click setting-file\DEV-KIT.bat"

with open(bat, 'rb') as f:
    raw = f.read()

content = raw.decode('cp949')
orig = content

UPGRADE_PROMPT = (
    'echo.\r\n'
    'echo  \uc774\ubbf8 \uc124\uce58\ub41c \ub3c4\uad6c \ucc98\ub9ac \ubc29\ubc95:\r\n'
    'echo    [1] \uac74\ub108\ub700    (\ud604\uc7ac \ubc84\uc804 \uc720\uc9c0)\r\n'
    'echo    [2] \uc5c5\uadf8\ub808\uc774\ub4dc (\ucd5c\uc2e0 \ubc84\uc804\uc73c\ub85c)\r\n'
    'echo    [3] \uc81c\uac70       (\uc0ad\uc81c\ub9cc)\r\n'
    'set /p UPGRADE_CHOICE="  \uc120\ud0dd (\uae30\ubcf8\uac12=1): "\r\n'
    'if "!UPGRADE_CHOICE!"=="" set UPGRADE_CHOICE=1\r\n'
    'if "!UPGRADE_CHOICE!"=="2" (set UPGRADE_MODE=upgrade) else (\r\n'
    'if "!UPGRADE_CHOICE!"=="3" (set UPGRADE_MODE=remove)  else (\r\n'
    'set UPGRADE_MODE=skip))\r\n'
)

# ============================================================
# 1. DO_LEVEL_1~4: CONFIRM_INST 직후 프롬프트 삽입 (4곳 동시)
# ============================================================
ANCHOR_INST = 'if /i "!CONFIRM_INST!" NEQ "y" goto MAIN_MENU\r\n'
if ANCHOR_INST not in content:
    print("[FAIL] 1: CONFIRM_INST 패턴 미발견")
    sys.exit(1)
n1 = content.count(ANCHOR_INST)
content = content.replace(ANCHOR_INST, ANCHOR_INST + UPGRADE_PROMPT)
print(f"[OK] 1: DO_LEVEL UPGRADE_MODE 프롬프트 삽입 ({n1}곳)")

# ============================================================
# 2. DO_SELECT: CONFIRM_SEL 직후 프롬프트 삽입
# ============================================================
ANCHOR_SEL = 'if /i "!CONFIRM_SEL!" NEQ "y" goto DO_SELECT\r\n'
if ANCHOR_SEL not in content:
    print("[FAIL] 2: CONFIRM_SEL 패턴 미발견")
    sys.exit(1)
content = content.replace(ANCHOR_SEL, ANCHOR_SEL + UPGRADE_PROMPT, 1)
print("[OK] 2: DO_SELECT UPGRADE_MODE 프롬프트 삽입")

# ============================================================
# 3. :INSTALL Block1 (첫 시도 실패, goto :eof 포함)
# ============================================================
UPG1 = (
    'if "!UPGRADE_MODE!"=="upgrade" (\r\n'
    '        winget upgrade --id %~2 --source winget --accept-source-agreements --accept-package-agreements --silent >nul 2>&1\r\n'
    '        echo         [\uc5c5\uadf8\ub808\uc774\ub4dc] %~1\r\n'
    '        >> "%LOG_FILE%" echo   \uacb0\uacfc: \uc5c5\uadf8\ub808\uc774\ub4dc (errorlevel=!INST_ERR!)\r\n'
    '        set /a INSTALL_COUNT+=1\r\n'
    '        >> "%REPORT_FILE%.tmp" echo   [\uc5c5\uadf8\ub808\uc774\ub4dc] %~1\r\n'
    '    ) else if "!UPGRADE_MODE!"=="remove" (\r\n'
    '        winget uninstall --id %~2 --source winget --silent >nul 2>&1\r\n'
    '        echo         [\uc81c\uac70] %~1\r\n'
    '        >> "%LOG_FILE%" echo   \uacb0\uacfc: \uc81c\uac70\r\n'
    '        set /a SKIP_COUNT+=1\r\n'
    '        >> "%REPORT_FILE%.tmp" echo   [\uc81c\uac70] %~1\r\n'
    '    ) else (\r\n'
    '        echo         [\uac74\ub108\ub700] %~1 (\uc774\ubbf8 \uc124\uce58\ub428)\r\n'
    '        >> "%LOG_FILE%" echo   \uacb0\uacfc: \uac74\ub108\ub700 (\uc774\ubbf8 \uc124\uce58\ub428, errorlevel=!INST_ERR!)\r\n'
    '        set /a SKIP_COUNT+=1\r\n'
    '        >> "%REPORT_FILE%.tmp" echo   [\uac74\ub108\ub700] %~1\r\n'
    '    )\r\n'
    '    goto :eof\r\n'
    ')\r\n'
)
p3 = re.compile(
    r'winget list --id %~2 --source winget >nul 2>&1\r\n'
    r'if not errorlevel 1 \(\r\n'
    r'    echo [^\r\n]+\r\n'
    r'    >> [^\r\n]+errorlevel=!INST_ERR![^\r\n]*\r\n'
    r'    set /a SKIP_COUNT\+=1\r\n'
    r'    >> [^\r\n]+\r\n'
    r'    goto :eof\r\n'
    r'\)\r\n'
)
new3 = 'winget list --id %~2 --source winget >nul 2>&1\r\nif not errorlevel 1 (\r\n    ' + UPG1
new_content, c3 = p3.subn(new3, content)
if c3 == 0:
    print("[FAIL] 3: :INSTALL Block1 패턴 미발견")
    sys.exit(1)
content = new_content
print(f"[OK] 3: :INSTALL Block1 분기 ({c3}건)")

# ============================================================
# 4. :INSTALL Block2 (재시도 실패, else+goto :eof 포함)
# ============================================================
UPG2 = (
    'if "!UPGRADE_MODE!"=="upgrade" (\r\n'
    '        winget upgrade --id %~2 --source winget --accept-source-agreements --accept-package-agreements --silent >nul 2>&1\r\n'
    '        echo         [\uc5c5\uadf8\ub808\uc774\ub4dc] %~1\r\n'
    '        >> "%LOG_FILE%" echo   \uacb0\uacfc: \uc5c5\uadf8\ub808\uc774\ub4dc\r\n'
    '        set /a INSTALL_COUNT+=1\r\n'
    '        >> "%REPORT_FILE%.tmp" echo   [\uc5c5\uadf8\ub808\uc774\ub4dc] %~1\r\n'
    '    ) else if "!UPGRADE_MODE!"=="remove" (\r\n'
    '        winget uninstall --id %~2 --source winget --silent >nul 2>&1\r\n'
    '        echo         [\uc81c\uac70] %~1\r\n'
    '        >> "%LOG_FILE%" echo   \uacb0\uacfc: \uc81c\uac70\r\n'
    '        set /a SKIP_COUNT+=1\r\n'
    '        >> "%REPORT_FILE%.tmp" echo   [\uc81c\uac70] %~1\r\n'
    '    ) else (\r\n'
    '        echo         [\uac74\ub108\ub700] %~1 (\uc774\ubbf8 \uc124\uce58\ub428)\r\n'
    '        >> "%LOG_FILE%" echo   \uacb0\uacfc: \uac74\ub108\ub700\r\n'
    '        set /a SKIP_COUNT+=1\r\n'
    '        >> "%REPORT_FILE%.tmp" echo   [\uac74\ub108\ub700] %~1\r\n'
    '    )\r\n'
)
p4 = re.compile(
    r'winget list --id %~2 --source winget >nul 2>&1\r\n'
    r'if not errorlevel 1 \(\r\n'
    r'    echo [^\r\n]+\r\n'
    r'    >> [^\r\n]+\r\n'
    r'    set /a SKIP_COUNT\+=1\r\n'
    r'    >> [^\r\n]+\r\n'
    r'\) else \(\r\n'
    r'    echo [^\r\n]+\r\n'
    r'    >> [^\r\n]+\r\n'
    r'    set /a FAIL_COUNT\+=1\r\n'
    r'    >> [^\r\n]+\r\n'
    r'\)\r\n'
    r'goto :eof\r\n'
)
new4 = (
    'winget list --id %~2 --source winget >nul 2>&1\r\n'
    'if not errorlevel 1 (\r\n'
    '    ' + UPG2 +
    ') else (\r\n'
    '    echo         [\uac74\ub108\ub700] %~1 \uc124\uce58 \uc2e4\ud328 \u2192 \ub098\uc911\uc5d0 \uc218\ub3d9 \uc124\uce58\r\n'
    '    >> "%LOG_FILE%" echo   \uc7ac\uc2dc\ub3c4 \uc2e4\ud328 (errorlevel=!RETRY_ERR!): %TIME%\r\n'
    '    set /a FAIL_COUNT+=1\r\n'
    '    >> "%REPORT_FILE%.tmp" echo   [\uc2e4\ud328] %~1\r\n'
    ')\r\n'
    'goto :eof\r\n'
)
new_content, c4 = p4.subn(new4, content)
if c4 == 0:
    print("[FAIL] 4: :INSTALL Block2 패턴 미발견")
    sys.exit(1)
content = new_content
print(f"[OK] 4: :INSTALL Block2 분기 ({c4}건)")

# ============================================================
# 5. :NPM_INSTALL already-installed 블록
# ============================================================
NPM_UPG = (
    'if "!UPGRADE_MODE!"=="upgrade" (\r\n'
    '        npm update -g %~2 >nul 2>&1\r\n'
    '        echo         [\uc5c5\uadf8\ub808\uc774\ub4dc] %~1 (npm)\r\n'
    '        >> "%LOG_FILE%" echo   \uacb0\uacfc: \uc5c5\uadf8\ub808\uc774\ub4dc (npm)\r\n'
    '        >> "%REPORT_FILE%.tmp" echo   [\uc5c5\uadf8\ub808\uc774\ub4dc] %~1 (npm)\r\n'
    '    ) else if "!UPGRADE_MODE!"=="remove" (\r\n'
    '        npm uninstall -g %~2 >nul 2>&1\r\n'
    '        echo         [\uc81c\uac70] %~1 (npm)\r\n'
    '        >> "%LOG_FILE%" echo   \uacb0\uacfc: \uc81c\uac70 (npm)\r\n'
    '        >> "%REPORT_FILE%.tmp" echo   [\uc81c\uac70] %~1 (npm)\r\n'
    '    ) else (\r\n'
    '        echo         [\uac74\ub108\ub700] %~1 (\uc774\ubbf8 \uc124\uce58\ub428)\r\n'
    '        >> "%LOG_FILE%" echo   \uacb0\uacfc: \uac74\ub108\ub700 (\uc774\ubbf8 \uc124\uce58\ub428)\r\n'
    '        >> "%REPORT_FILE%.tmp" echo   [\uac74\ub108\ub700] %~1 (npm)\r\n'
    '    )\r\n'
    '    goto :eof\r\n'
    ')\r\n'
)
p5 = re.compile(
    r'npm list -g %~2 >nul 2>&1\r\n'
    r'if not errorlevel 1 \(\r\n'
    r'    echo [^\r\n]+\r\n'
    r'    >> [^\r\n]+\r\n'
    r'    >> [^\r\n]+\r\n'
    r'    goto :eof\r\n'
    r'\)\r\n'
)
new5 = 'npm list -g %~2 >nul 2>&1\r\nif not errorlevel 1 (\r\n    ' + NPM_UPG
new_content, c5 = p5.subn(new5, content)
if c5 == 0:
    print("[FAIL] 5: :NPM_INSTALL 패턴 미발견")
    sys.exit(1)
content = new_content
print(f"[OK] 5: :NPM_INSTALL 분기 ({c5}건)")

# ============================================================
# 저장
# ============================================================
if content == orig:
    print('\n[경고] 변경사항 없음!')
    sys.exit(1)

result = content.encode('cp949')
with open(bat, 'wb') as f:
    f.write(result)

print(f'\n[완료] DEV-KIT.bat 업데이트 성공! ({len(raw)}->{len(result)} bytes)')
