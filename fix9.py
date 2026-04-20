# -*- coding: utf-8 -*-
# fix9.py - UPGRADE_MODE 초기화 누락 버그 수정
#   set START_TIME=%TIME% 직후 set UPGRADE_MODE=skip 삽입
import sys

bat = r"D:\AI_Dev_Work\2026y\26y_04m_22d_One-click setting-file\DEV-KIT.bat"

with open(bat, 'rb') as f:
    raw = f.read()

content = raw.decode('cp949')
orig = content

ANCHOR = 'set START_TIME=%TIME%\r\n'
INSERT = 'set UPGRADE_MODE=skip\r\n'

if ANCHOR not in content:
    print("[FAIL] 앵커 패턴 미발견: set START_TIME=%TIME%")
    sys.exit(1)

if INSERT in content:
    print("[SKIP] 이미 적용됨: set UPGRADE_MODE=skip 존재")
    sys.exit(0)

content = content.replace(ANCHOR, ANCHOR + INSERT, 1)

if content == orig:
    print('\n[경고] 변경사항 없음!')
    sys.exit(1)

result = content.encode('cp949')
with open(bat, 'wb') as f:
    f.write(result)

print(f'[OK] UPGRADE_MODE=skip 초기화 삽입 완료')
print(f'\n[완료] DEV-KIT.bat 업데이트 성공! ({len(raw)}->{len(result)} bytes)')
