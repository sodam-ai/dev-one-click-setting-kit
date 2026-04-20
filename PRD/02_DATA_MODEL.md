# 바이브코딩 환경 키트 -- 도구 카탈로그 v3.1

> BAT 파일 프로젝트이므로 DB 대신 "설치 도구 목록"이 데이터 모델입니다.

---

## 4단계 누적 레벨 구조

```
[왕초보] 5개
  ├── Git
  ├── Python 3
  ├── Node.js LTS
  ├── VS Code
  └── Windows Terminal

[중급] 왕초보 + 5개 = 총 10개
  ├── GitHub CLI
  ├── PowerShell 7
  ├── pnpm
  ├── Ollama
  └── Bun

[고급] 중급 + 4개 = 총 14개
  ├── Java 21 LTS
  ├── Flutter + Dart
  ├── Go
  └── Rust + Cargo

[올인원] 고급 + 2개 = 총 16개
  ├── Ruby
  └── PHP
```

---

## 왕초보 도구 (5개)

| 도구 | winget ID | 포함 도구 | 디스크 | 다운로드 | 이유 |
|------|-----------|----------|--------|---------|------|
| Git | `Git.Git` | - | ~300MB | ~60MB | 코드 저장/공유 필수. GitHub 없이는 바이브코딩 불가 |
| Python 3 | `Python.Python.3` | pip 자동 | ~100MB | ~25MB | AI/ML 모든 도구의 기반 |
| Node.js LTS | `OpenJS.NodeJS.LTS` | npm, npx 자동 | ~200MB | ~30MB | Next.js, React 등 웹 앱 필수 |
| VS Code | `Microsoft.VisualStudioCode` | - | ~350MB | ~90MB | 기본 AI 코딩 에디터 |
| Windows Terminal | `Microsoft.WindowsTerminal` | - | ~50MB | ~20MB | 탭/색상/유니코드. Win10 필수, Win11 기본내장(건너뜀) |

**왕초보 합계: ~1GB 디스크 / ~225MB 다운로드 / ~7분**

---

## 중급 추가 도구 (5개)

| 도구 | winget ID | 포함 도구 | 디스크 | 다운로드 | 이유 |
|------|-----------|----------|--------|---------|------|
| GitHub CLI | `GitHub.cli` | - | ~30MB | ~10MB | `gh` 명령어로 GitHub 자동화 |
| PowerShell 7 | `Microsoft.PowerShell` | - | ~200MB | ~100MB | 기존 PS 5.1보다 강력한 스크립팅 |
| pnpm | `pnpm.pnpm` | - | ~50MB | ~10MB | npm보다 10배 빠름. Next.js 프로젝트 표준 |
| Ollama | `Ollama.Ollama` | - | ~500MB | ~500MB | 로컬 AI 실행. 모델은 별도 다운로드 필요 |
| Bun | `Oven-sh.Bun` | - | ~100MB | ~70MB | JS 런타임+패키지+번들러 통합. 최신 트렌드 |

**중급 추가 합계: ~880MB 디스크 / ~690MB 다운로드**
*Ollama 모델 별도: llama3.2 약 2GB, gemma3 약 3GB*

---

## 고급 추가 도구 (4개)

| 도구 | winget ID | 포함 도구 | 디스크 | 다운로드 | 이유 |
|------|-----------|----------|--------|---------|------|
| Java 21 LTS | `EclipseAdoptium.Temurin.21.JDK` | - | ~350MB | ~170MB | Android 앱, 서버. Flutter 빌드 전제 조건 |
| Flutter + Dart | `Google.FlutterSDK` | Dart 자동 | ~2GB | ~1GB | iOS/Android/웹 통합 앱 개발 |
| Go | `GoLang.Go` | - | ~500MB | ~150MB | 고성능 서버. AI 도구 백엔드 |
| Rust | `Rustlang.Rustup` | Cargo 자동 | ~1GB+ | ~300MB | 시스템 프로그래밍. CLI 도구 빌드 |

**고급 추가 합계: ~3.85GB 디스크 / ~1.62GB 다운로드**

---

## 올인원 추가 도구 (2개)

| 도구 | winget ID | 디스크 | 이유 |
|------|-----------|--------|------|
| Ruby | `RubyInstallerTeam.RubyWithDevKit.3.3` | ~500MB | 레거시/특수 용도 |
| PHP | `PHP.PHP` | ~100MB | 레거시 웹 서버 |

---

## 설치 의존성 순서 (반드시 준수)

```
순서 1: Git.Git
순서 2: Python.Python.3 / OpenJS.NodeJS.LTS  (병렬 가능)
순서 3: pnpm.pnpm / Oven-sh.Bun              (Node.js 이후 필수)
순서 4: EclipseAdoptium.Temurin.21.JDK
순서 5: Google.FlutterSDK                    (Java 이후 필수)
순서 무관: VS Code, Windows Terminal, GitHub CLI,
           PowerShell 7, Ollama, Go, Rust, Ruby, PHP
```

---

## Post-install 작업 목록 ★v3.1 확정

| 도구 | 작업 | 자동/수동 | 확정 이유 |
|------|------|---------|---------|
| Git | `git config --global user.name "이름"` | 안내만 | 개인정보 자동 저장 금지 |
| Git | `git config --global user.email "이메일"` | 안내만 | 개인정보 자동 저장 금지 |
| Git | `git config --global core.autocrlf true` | 자동 실행 | Windows 줄바꿈 표준, 첫 커밋 오류 예방 |
| Python | `pip install --upgrade pip` | 자동 실행 | pip 경고 제거 |
| Node.js | `npm config set fund false` | 자동 실행 | npm 광고 메시지 제거, 초보자 혼란 방지 |
| Ollama | `ollama pull llama3.2` (2GB 경고) | 안내만 | 2GB 부담, 수업 환경 부적합 |
| Rust | `rustup update stable` | 자동 실행 | 초기 toolchain 완성 |
| VS Code | Python 확장, Prettier 설치 URL | URL 안내만 | 취향 강요 금지 |
| 공통 | `where [tool]` PATH 검증 출력 | 자동 실행 | 설치 완료 눈으로 확인 |

---

## Cursor 설치 전략 ★v3.1 변경

```
전략: 처음부터 URL 직접 안내 (winget 시도 제거)

변경 이유:
  - Anysphere.Cursor winget ID 불안정 (공식 winget 패키지 아님)
  - 실패 경험 자체가 초보 수강생에게 공포 유발
  - URL 직접 안내가 더 신뢰성 높음

[8] 수동 설치 메뉴에서 최우선 안내:
  1. https://cursor.sh 브라우저 자동 오픈
  2. "AI 바이브코딩 핵심 에디터 — 직접 설치 필요" 안내
  3. 설치 완료 후 [9] 설치 확인에서 cursor --version 체크
```

---

## 수동 설치 필요 도구

| 도구 | URL | 우선도 | 비고 |
|------|-----|--------|------|
| Cursor | https://cursor.sh | 🔴 최우선 | AI 코딩 에디터 1위. URL 직접 안내 (winget 불안정) |
| Claude Desktop | https://claude.ai/download | 🔴 높음 | Claude Code 필수 |
| Docker Desktop | https://www.docker.com/products/docker-desktop | 🟡 중간 | 서버 배포 학습 시 |
| Android Studio | https://developer.android.com/studio | 🟡 중간 | Flutter Android 빌드 |
| GitHub Desktop | https://desktop.github.com | 🟢 선택 | Git GUI |

---

## 자동 포함 도구 (별도 설치 불필요)

| 도구 | 포함 경로 | 확인 명령 |
|------|----------|----------|
| pip | Python 설치 시 자동 | `pip --version` |
| npm, npx | Node.js 설치 시 자동 | `npm --version` |
| Cargo | Rust(rustup) 설치 시 자동 | `cargo --version` |
| Dart SDK | Flutter 설치 시 자동 | `dart --version` |

---

## 버전 고정 정책

| 도구 | 전략 | 지원 기간 |
|------|------|---------|
| Python | `Python.Python.3` (최신 3.x) | 3.x 계열 유지 |
| Node.js | `OpenJS.NodeJS.LTS` (LTS 고정) | 짝수 버전 (22, 24...) |
| Java | `Temurin.21.JDK` (21 LTS 고정) | 2028년까지 |
| Flutter | `Google.FlutterSDK` (stable) | stable 채널만 |
| 나머지 | 최신 안정 버전 | winget 기본값 |

> **검토 주기**: 연 2회 (1월, 7월) winget ID 유효성 재확인
