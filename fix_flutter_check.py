# -*- coding: utf-8 -*-
import shutil

BAT_PATH = r"D:\AI_Dev_Work\2026y\26y_04m_22d_dev-one-click-setting-kit\dev-one-click-setting-kit.bat"
shutil.copy(BAT_PATH, BAT_PATH + '.bak')

with open(BAT_PATH, 'r', encoding='cp949') as f:
    content = f.read()

# /dev/null 로 잘못 변환된 Flutter 체크 섹션을 올바른 >nul 버전으로 교체
old = (
    'where flutter >/dev/null 2>&1\n'
    'if errorlevel 1 (\n'
    '    echo    [X] Flutter\n'
    ') else (\n'
    '    set _FV=\n'
    '    for /f "tokens=2" %%v in (\'flutter --version 2^>/dev/null ^| findstr /B "Flutter"\') do if not defined _FV set _FV=%%v\n'
    '    if defined _FV (echo    [O] Flutter  !_FV!) else echo    [O] Flutter\n'
    ')'
)

new = (
    'where flutter >nul 2>&1\n'
    'if errorlevel 1 (\n'
    '    echo    [X] Flutter\n'
    ') else (\n'
    '    set _FV=\n'
    '    for /f "tokens=2" %%v in (\'flutter --version 2^>nul ^| findstr /B "Flutter"\') do if not defined _FV set _FV=%%v\n'
    '    if defined _FV (echo    [O] Flutter  !_FV!) else echo    [O] Flutter\n'
    ')'
)

if old in content:
    content = content.replace(old, new, 1)
    print('  [OK] /dev/null -> nul 수정 완료')
else:
    print('  [!!] 패턴 미발견 - 현재 Flutter 섹션:')
    s = content.find('where flutter')
    print(repr(content[s:s+300]))

with open(BAT_PATH, 'w', encoding='cp949') as f:
    f.write(content)

# 검증
with open(BAT_PATH, 'r', encoding='cp949') as f:
    verify = f.read()
dev_null_count = verify.count('/dev/null')
nul_count = verify.count('>nul')
print(f'  검증: /dev/null 잔여 {dev_null_count}건, >nul 정상 {nul_count}건')
