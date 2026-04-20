# 바이브코딩 환경 키트 -- 프로젝트 스펙 v3.1

> AI가 코드를 짤 때 반드시 지켜야 할 규칙. 매번 이 파일을 함께 공유하세요.

---

## 기술 스택

| 영역 | Phase 1 | Phase 2 | 이유 |
|------|---------|---------|------|
| 진입점 | BAT (.bat) | BAT (.bat) | 더블클릭 즉시 실행 |
| 로직 | BAT (.bat) | PowerShell 7 (.ps1) | Phase 2에서 UI 강화 |
| 패키지 관리 | winget | winget | Microsoft 서명 검증 내장 |
| 인코딩 | UTF-8 (chcp 65001) | UTF-8 | 한국어 메뉴 필수 |

---

## 메뉴 구조 (Phase 1)

```
[1] 왕초보 설치   처음 시작하는 분 (5개, ~7분)
[2] 중급 설치     어느 정도 써본 분 (10개, ~15분)  ← 왕초보 포함
[3] 고급 설치     앱/서버 개발하는 분 (14개, ~35분) ← 중급 포함
[4] 올인원 설치   모든 도구 다 설치 (16개, ~45분)  ← 고급 포함
[5] 선택 설치     원하는 것만 골라서
[6] 업데이트      설치된 것 전체 최신으로
[7] 제거          도구 삭제 (개별/전체)
[8] 수동 설치     Cursor (최우선) + Docker 등 URL 안내
[9] 설치 확인     O/X + 버전 상태 표시
[0] 종료
```

---

## 보안 설계 원칙

1. **관리자 권한 불필요** — winget 사용자 범위 설치. 기업/학교 PC 대응
2. **winget 공식 소스만** — `--source winget` 항상 명시. 서드파티 소스 추가 금지
3. **사용자 입력 최소화** — 메뉴 번호만 입력. 임의 명령어 실행 경로 없음
4. **Git 설정 수동 처리** — 이메일/이름 자동 저장·출력 금지. 안내 텍스트만 표시

---

## 설치 의존성 순서 (코드에 반드시 반영)

```
1순위: Git.Git
2순위: Python.Python.3 + OpenJS.NodeJS.LTS
3순위: pnpm.pnpm + Oven-sh.Bun          ← Node.js 이후
4순위: EclipseAdoptium.Temurin.21.JDK
5순위: Google.FlutterSDK                ← Java 이후
순위무관: VS Code, Windows Terminal, GitHub CLI,
          PowerShell 7, Ollama, Go, Rust, Ruby, PHP
```

---

## winget 패키지 ID 목록 (검증 완료)

```
왕초보 (5개):
  Git.Git
  Python.Python.3
  OpenJS.NodeJS.LTS
  Microsoft.VisualStudioCode
  Microsoft.WindowsTerminal

중급 추가 (5개):
  GitHub.cli
  Microsoft.PowerShell
  pnpm.pnpm
  Ollama.Ollama
  Oven-sh.Bun

고급 추가 (4개):
  EclipseAdoptium.Temurin.21.JDK
  Google.FlutterSDK
  GoLang.Go
  Rustlang.Rustup

올인원 추가 (2개):
  RubyInstallerTeam.RubyWithDevKit.3.3
  PHP.PHP

Cursor (URL 직접 안내):
  winget 시도 없음  ← [8] 수동 설치에서 https://cursor.sh 바로 오픈
```

---

## 오류 처리 요구사항

| 상황 | 처리 | 금지 |
|------|------|------|
| Windows 10 21H1 이하 | winget 수동 설치 URL 안내 후 종료 | 강제 오류 없이 |
| winget 없음 | URL 안내 후 종료 | 강제 오류 없이 |
| winget source update 실패 | 경고만 출력 후 계속 | 강제 종료 금지 |
| 디스크 부족 | 경고 후 계속 여부 선택 | 강제 종료 금지 |
| 개별 도구 실패 | 5초 후 1회 자동 재시도 → 재실패 시 "건너뜀" | 전체 중단 금지 |
| 이미 설치됨 | errorlevel 확인 후 건너뜀 | 오류 메시지 금지 |
| 잘못된 입력 | 메뉴 재표시 | 오류 출력/종료 금지 |
| Cursor | [8] 메뉴에서 URL 직접 오픈 | winget 시도 금지 |

---

## 절대 하지 마 (DO NOT)

- BAT 파일을 여러 개로 분리하지 마 (단일 파일 배포 원칙)
- `exit /b 1`로 오류 시 강제 종료하지 마
- 한국어 주석을 제거하지 마
- winget 패키지 ID를 임의로 변경하지 마
- `pause` 없이 창이 바로 닫히게 하지 마
- 의존성 순서를 무시하고 설치하지 마 (pnpm은 Node.js 이후, Flutter는 Java 이후)
- `--source winget` 없이 설치하지 마
- Git user.email 등 개인정보를 자동으로 처리하지 마
- 설치 리포트에 PC 이름 외 개인정보를 포함하지 마

---

## 항상 해 (ALWAYS DO)

- `chcp 65001 >nul` 파일 첫 줄 유지
- `setlocal enabledelayedexpansion` 사용
- `--source winget --accept-source-agreements --accept-package-agreements` 항상 포함
- errorlevel로 설치 성공/실패 확인
- 개별 도구 실패 시 5초 후 1회 자동 재시도 후 건너뜀
- 설치 진행 카운터 표시 ([n/N] 설치 중...)
- 설치 완료 후 install-report-[날짜].txt (요약) + install-log-[날짜].txt (상세) 2종 생성
- install-log에 각 도구 errorlevel + 재시도 여부 기록
- pip 업그레이드 자동 실행 (Python 설치 후)
- `npm config set fund false` 자동 실행 (Node.js 설치 후)
- `git config --global core.autocrlf true` 자동 실행 (Git 설치 후)
- Git user.name / user.email 설정 안내 텍스트 출력 (자동 저장 금지)
- `where git`, `where python`, `where node` PATH 검증 출력 (완료 후)
- 완료 후 "새 터미널을 열어서 시작하세요" 안내

---

## 테스트 시나리오

```
[시나리오 1] 새 Windows 11 PC
  1. DEV-KIT.bat 더블클릭
  2. 사전 체크 통과 확인
  3. [1] 왕초보 설치
  4. Git 설정 안내 출력 확인
  5. pip 업그레이드 자동 실행 확인
  6. install-report-[날짜].txt + install-log-[날짜].txt 2종 생성 확인
  7. PATH 검증 출력 (where git, where python, where node) 확인
  8. 새 터미널: git --version && python --version && node --version 성공

[시나리오 2] 이미 설치된 환경 (재실행)
  1. Tier1 설치된 PC에서 [1] 왕초보 재실행
  2. 모두 "건너뜀" 처리 확인
  3. 오류 없이 완료 확인

[시나리오 3] 잘못된 입력
  1. 메뉴에서 abc, 99 입력
  2. 오류 없이 메뉴 재표시 확인
```

---

## [DECISIONS CONFIRMED] ★v3.1 전체 확정

| 항목 | 결정 |
|------|------|
| Cursor winget | ✅ winget 시도 제거 — URL 직접 안내 (ID 불안정) |
| Git 설정 방식 | ✅ 안내 텍스트만 출력 — 대화형 입력 금지 (개인정보) |
| Ollama 모델 | ✅ 안내만 — 자동 다운로드 금지 (2GB 부담) |
| VS Code 확장 | ✅ URL 안내만 — 자동 설치 금지 (취향 강요 금지) |
| Win10 21H1 이하 | ✅ 미지원 — winget 수동 설치 URL 안내 후 종료 |
