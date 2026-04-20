# -*- coding: utf-8 -*-
# fix6b.py - upgrade6.py 미완료 2건 처리
#   A. REMOVE_ALL: npm uninstall 블록 삽입
#   B. DONE_MSG: Cursor 줄 중립화 + 치트시트 추가
import re, sys

bat = r"D:\AI_Dev_Work\2026y\26y_04m_22d_One-click setting-file\DEV-KIT.bat"

with open(bat, 'rb') as f:
    raw = f.read()

content = raw.decode('cp949')
orig = content

# ============================================================
# A. REMOVE_ALL: for 루프 닫힌 후 npm uninstall 블록 삽입
# ============================================================
pattern_a = re.compile(
    r'(    winget uninstall --id %%i --source winget --silent >nul 2>&1\r\n'
    r'    echo [^\r\n]+: %%i\r\n'
    r'\)\r\n'
    r'echo\.\r\n)'
)

npm_block = (
    'echo  [npm] npm \ud328\ud0a4\uc9c0 \uc81c\uac70 \uc911...\r\n'
    'for %%p in (vercel supabase stripe resend @railway/cli @clerk/clerk-sdk-node prisma uploadthing) do (\r\n'
    '    npm uninstall -g %%p >nul 2>&1\r\n'
    '    echo    [npm] \uc81c\uac70: %%p\r\n'
    ')\r\n'
    'echo.\r\n'
)

def repl_a(m):
    return m.group(1) + npm_block

new_content, count_a = pattern_a.subn(repl_a, content)
if count_a == 0:
    print("[FAIL] A: REMOVE_ALL 패턴 미발견")
    sys.exit(1)
content = new_content
print(f"[OK] A: REMOVE_ALL npm 블록 삽입 ({count_a}건)")

# ============================================================
# B1. DONE_MSG: "5. Cursor ..." 줄 중립화
# ============================================================
pattern_b1 = re.compile(r'echo   5\. Cursor [^\r\n]+\r\n')
new_b1 = 'echo   5. \uac01 \ub3c4\uad6c \uc124\uce58 \ud655\uc778: [9] \uc124\uce58 \ud655\uc778 \uba54\ub274 \uc774\uc6a9\r\n'

new_content, count_b1 = pattern_b1.subn(new_b1, content)
if count_b1 == 0:
    print("[FAIL] B1: DONE_MSG Cursor 줄 미발견")
    sys.exit(1)
content = new_content
print(f"[OK] B1: DONE_MSG Cursor 줄 중립화 ({count_b1}건)")

# ============================================================
# B2. DONE_MSG: "새 터미널을..." 앞에 치트시트 삽입
# ============================================================
pattern_b2 = re.compile(r'(echo  [^\r\n]*\uc0c8 \ud130\ubbf8\ub110[^\r\n]+\r\n)')

cheatsheet = (
    'echo  --- \uc8fc\uc694 CLI \ubc84\uc804 \ud655\uc778 ---\r\n'
    'echo   vercel --version\r\n'
    'echo   supabase --version\r\n'
    'echo   npx prisma --version\r\n'
    'echo   claude --version\r\n'
    'echo.\r\n'
)

def repl_b2(m):
    return cheatsheet + m.group(1)

new_content, count_b2 = pattern_b2.subn(repl_b2, content, count=1)
if count_b2 == 0:
    print("[FAIL] B2: DONE_MSG 새 터미널 줄 미발견")
    sys.exit(1)
content = new_content
print(f"[OK] B2: DONE_MSG 치트시트 삽입 ({count_b2}건)")

# ============================================================
# 저장
# ============================================================
if content == orig:
    print('\n[경고] 변경사항 없음!')
    sys.exit(1)

result = content.encode('cp949')
with open(bat, 'wb') as f:
    f.write(result)

print(f'\n[완료] DEV-KIT.bat 업데이트 성공! ({len(raw)}\u2192{len(result)} bytes)')
