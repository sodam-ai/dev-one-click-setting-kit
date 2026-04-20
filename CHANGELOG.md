# Changelog

All notable changes to this project will be documented in this file.

---

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
