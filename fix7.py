# -*- coding: utf-8 -*-
# fix7.py - BAT 이식성: REPORT_FILE/LOG_FILE에 %~dp0 추가
import sys

bat = r"D:\AI_Dev_Work\2026y\26y_04m_22d_One-click setting-file\DEV-KIT.bat"

with open(bat, 'rb') as f:
    raw = f.read()

content = raw.decode('cp949')
orig = content

def sub(old, new, label):
    global content
    if old not in content:
        print(f"[FAIL] {label}: 패턴 미발견 {repr(old)}")
        sys.exit(1)
    content = content.replace(old, new, 1)
    print(f"[OK] {label}")

sub('set REPORT_FILE=install-report-', 'set REPORT_FILE=%~dp0install-report-', 'REPORT_FILE %~dp0 추가')
sub('set LOG_FILE=install-log-',       'set LOG_FILE=%~dp0install-log-',       'LOG_FILE %~dp0 추가')

if content == orig:
    print('\n[경고] 변경사항 없음!')
    sys.exit(1)

result = content.encode('cp949')
with open(bat, 'wb') as f:
    f.write(result)

print(f'\n[완료] DEV-KIT.bat 업데이트 성공! ({len(raw)}->{len(result)} bytes)')
