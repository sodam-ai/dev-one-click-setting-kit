# -*- coding: utf-8 -*-
# fix6c.py - 치트시트 위치 수정
#   A. POST 내 잘못 삽입된 치트시트 제거 + 원래 줄 복원 (4칸 들여쓰기)
#   B. DONE_MSG "새 터미널을 열어..." 줄 앞에 치트시트 올바르게 삽입
import re, sys

bat = r"D:\AI_Dev_Work\2026y\26y_04m_22d_One-click setting-file\DEV-KIT.bat"

with open(bat, 'rb') as f:
    raw = f.read()

content = raw.decode('cp949')
orig = content

# ============================================================
# A. POST 내 잘못 삽입된 치트시트 제거 + 원줄 복원 (4칸 들여쓰기)
# ============================================================
pattern_a = re.compile(
    r'    echo  --- [^\r\n]+ ---\r\n'
    r'echo   vercel --version\r\n'
    r'echo   supabase --version\r\n'
    r'echo   npx prisma --version\r\n'
    r'echo   claude --version\r\n'
    r'echo\.\r\n'
    r'(echo  [^\r\n]+claude --version[^\r\n]*\r\n)'
)

def repl_a(m):
    return '    ' + m.group(1)

new_content, count_a = pattern_a.subn(repl_a, content)
if count_a == 0:
    print("[FAIL] A: POST 내 치트시트 패턴 미발견")
    sys.exit(1)
content = new_content
print(f"[OK] A: POST 내 치트시트 제거 + 원줄 복원 ({count_a}건)")

# ============================================================
# B. DONE_MSG: "새 터미널을 열어..." 줄 앞에 치트시트 삽입
#    앵커: 새=\uc0c8 터미널을=\ud130\ubbf8\ub110\uc744
# ============================================================
cheatsheet = (
    'echo  --- \uc8fc\uc694 CLI \ubc84\uc804 \ud655\uc778 ---\r\n'
    'echo   vercel --version\r\n'
    'echo   supabase --version\r\n'
    'echo   npx prisma --version\r\n'
    'echo   claude --version\r\n'
    'echo.\r\n'
)

pattern_b = re.compile(
    r'(echo  [^\r\n]*\uc0c8 \ud130\ubbf8\ub110\uc744 [^\r\n]+\r\n'
    r'echo  \([^\r\n]+\)\r\n)'
)

def repl_b(m):
    return cheatsheet + m.group(1)

new_content, count_b = pattern_b.subn(repl_b, content, count=1)
if count_b == 0:
    print("[FAIL] B: DONE_MSG '새 터미널을' 패턴 미발견")
    sys.exit(1)
content = new_content
print(f"[OK] B: DONE_MSG 치트시트 삽입 ({count_b}건)")

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
