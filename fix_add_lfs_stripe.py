# -*- coding: utf-8 -*-
import shutil

BAT_PATH = r"D:\AI_Dev_Work\2026y\26y_04m_22d_dev-one-click-setting-kit\dev-one-click-setting-kit.bat"
shutil.copy(BAT_PATH, BAT_PATH + '.bak')

with open(BAT_PATH, 'r', encoding='cp949') as f:
    content = f.read()

changes = []

# 1. echo 목록: AI 도구 그룹 앞에 개발 확장 CLI 그룹 삽입
old_echo = (
    'echo.\n'
    'echo   --- AI \xb5\xb5\xb1\xb8 (\xba\xb0\xb5\xb5 \xbc\xb3\xc4\xa1 \xc7\xca\xbf\xe4) ---\n'
)
new_echo = (
    'echo.\n'
    'echo   --- \xb0\xb3\xb9\xdf 확\xc7\xb0 CLI ---\n'
    'echo    [20] GitHub LFS        https://git-lfs.com/\n'
    'echo    [21] Stripe CLI        https://docs.stripe.com/stripe-cli\n'
    'echo.\n'
    'echo   --- AI \xb5\xb5\xb1\xb8 (\xba\xb0\xb5\xb5 \xbc\xb3\xc4\xa1 \xc7\xca\xbf\xe4) ---\n'
)

# CP949로 정확히 매칭하기 위해 Unicode로 작성
old_echo2 = 'echo.\necho   --- AI 도구 (별도 설치 필요) ---\n'
new_echo2 = (
    'echo.\n'
    'echo   --- 개발 확장 CLI ---\n'
    'echo    [20] GitHub LFS        https://git-lfs.com/\n'
    'echo    [21] Stripe CLI        https://docs.stripe.com/stripe-cli\n'
    'echo.\n'
    'echo   --- AI 도구 (별도 설치 필요) ---\n'
)

if old_echo2 in content:
    content = content.replace(old_echo2, new_echo2, 1)
    changes.append('echo [20][21] 삽입')
    print('  [OK] echo 목록 삽입')
else:
    # fallback: 직접 위치 탐색
    s = content.find(':DO_MANUAL')
    e = content.find('\n:: ====', s+1)
    section = content[s:e]
    ai_idx = section.find('--- AI ')
    if ai_idx > 0:
        insert_before = section[ai_idx-7:ai_idx]  # 'echo.\n' 앞
        print('  [!!] 패턴 미발견, AI 섹션 직접 확인:', repr(section[ai_idx-10:ai_idx+30]))
    else:
        print('  [!!] AI 도구 그룹 미발견')

# 2. start 명령: _OPENED 확인 라인 바로 앞에 삽입
old_start = 'if "!_OPENED!"=="1" echo.'
new_start = (
    'if "!MAN_CHOICE!"=="20" start "" "https://git-lfs.com/"                                          & set _OPENED=1\n'
    'if "!MAN_CHOICE!"=="21" start "" "https://docs.stripe.com/stripe-cli"                            & set _OPENED=1\n'
    '\n'
    'if "!_OPENED!"=="1" echo.'
)

if old_start in content:
    content = content.replace(old_start, new_start, 1)
    changes.append('start [20][21] 삽입')
    print('  [OK] start 명령 삽입')
else:
    print('  [!!] start 패턴 미발견')

if changes:
    with open(BAT_PATH, 'w', encoding='cp949') as f:
        f.write(content)

# 검증
with open(BAT_PATH, 'r', encoding='cp949') as f:
    verify = f.read()

s2 = verify.find(':DO_MANUAL')
e2 = verify.find('\n:: ====', s2+1)
url_count = verify[s2:e2].count('start ""')
print(f'  [검증] DO_MANUAL start 명령: {url_count}개 (기대 21)')
print(f'  [검증] git-lfs.com 포함: {"git-lfs.com" in verify}')
print(f'  [검증] docs.stripe.com 포함: {"docs.stripe.com/stripe-cli" in verify}')
print(f'\n완료: {len(changes)}개 변경')
