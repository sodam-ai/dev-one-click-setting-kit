# -*- coding: utf-8 -*-
import shutil

BAT_PATH = r"D:\AI_Dev_Work\2026y\26y_04m_22d_dev-one-click-setting-kit\dev-one-click-setting-kit.bat"
shutil.copy(BAT_PATH, BAT_PATH + '.bak')

with open(BAT_PATH, 'r', encoding='cp949') as f:
    content = f.read()

old = (
    'echo  ---------------------------------------------------\n'
    'echo.\n'
    'echo   --- 초보자 도구 ---\n'
)
new = (
    'echo  ---------------------------------------------------\n'
    'echo  번호를 입력하거나, URL 위에서 Ctrl+클릭 하면 브라우저에서 열립니다.\n'
    'echo.\n'
    'echo   --- 초보자 도구 ---\n'
)

if old in content:
    content = content.replace(old, new, 1)
    print('  [OK] Ctrl+클릭 안내 문구 추가')
else:
    print('  [!!] 패턴 미발견')
    s = content.find(':DO_MANUAL')
    print(repr(content[s:s+300]))

with open(BAT_PATH, 'w', encoding='cp949') as f:
    f.write(content)

with open(BAT_PATH, 'r', encoding='cp949') as f:
    verify = f.read()
print(f'  [검증] Ctrl+클릭 포함: {"Ctrl+클릭" in verify}')
