# Changelog

All notable changes to this project will be documented in this file.

---

## [v1.1.0] - 2026-04-22

### Fixed

- **B1** findstr 오탐 수정 - for 이중 루프 정확 매칭으로 교체
- **B2** 디스크 여유 공간 체크 추가 - C드라이브 3GB 미만 시 경고 및 중단 선택
- **B3** timeout /nobreak 추가 - 재시도 대기 중 Ctrl+C 스킵 방지
- **B4** 설치 카운터 수정 - LEVEL_3: 15->16개, LEVEL_4: 17->18개
- **B5** PATH_CHECK cursor 제거 - winget PATH 미등록 항목 오탐 방지

### Changed

- **S1** 전체 업데이트 - winget upgrade --all -> 키트 18개 도구 개별 업그레이드
- **S2** 수동 설치 메뉴 - Antigravity 항목 완전 제거 (메뉴/start/echo 포함)
- **U1** ANSI 색상 코드 초기화 - Windows 10+ 가상 터미널 시퀀스 자동 활성화
- **U2** npm 패키지 설치 방식 - 자동 일괄 -> Vercel/Supabase/Stripe/Resend 개별 Y/N 선택
- **U3** 소요 시간 표시 - 완료 시 총 분/초 화면 출력 및 로그 기록

### Removed

- fix6b.py fix6c.py fix7.py fix8.py fix9.py upgrade6.py - 내부 패치 스크립트 삭제


## [v1.0.0] - 2026-04-20

### Added

- **원클릭 자동 설치** — Windows 기본 패키지 관리자(winget) 기반 자동 설치
- **4단계 설치 레벨** — 초보자(5종) / 중급(+5종) / 고급(+4종) / 새로운(+2종), 총 16종 도구
- **이미 설치된 도구 감지** — 건너뜀 / 업그레이드 / 제거 선택 기능
- **이식성 보장** — `%~dp0` 기반으로 BAT 파일 위치·이름 변경 후에도 정상 작동
- **자동 재시도** — 첫 시도 실패 시 1회 자동 재시도
- **설치 리포트 자동 저장** — `install-report-날짜.txt`, `install-log-날짜.txt`
- **PATH 경로 확인** — 설치 후 환경 변수 등록 여부 자동 점검
- **CLI 버전 치트시트** — 완료 후 주요 명령어 버전 확인 안내
- **개별 선택 설치** — `[5]` 메뉴에서 [1]~[26] 중 원하는 도구만 선택
- **npm 패키지 선택 설치** — Vercel, Supabase, Stripe, Railway, Prisma, Claude CLI, Uploadthing
- **업데이트 메뉴** — `[6]` npm 패키지 일괄 최신화
- **제거 메뉴** — `[7]` 개별 제거 / `[8]` 전체 제거
- **README.md** — 한국어 완전 초보자 가이드 포함
- **README_EN.md** — 영어 가이드 (동일 구조)
- **LICENSE** — MIT 라이선스, Copyright © 2026 SoDam AI Studio
