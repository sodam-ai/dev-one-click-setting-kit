# 바이브코딩 환경 키트 -- Phase 분리 계획 v3.0

---

## Phase 1: MVP (현재 구현 대상)

### 목표
수강생이 혼자 실행해서 선택한 레벨의 모든 도구를 설치하고 즉시 사용 가능한 상태가 된다

### 기능 체크리스트
- [ ] 사전 체크 (Windows 버전 / winget 버전 / winget source update / 디스크 / 인터넷 / 기존 설치 충돌)
- [ ] 4단계 레벨 메뉴 (왕초보/중급/고급/올인원)
- [ ] 선택 설치 (개별 번호 선택)
- [ ] 의존성 순서 보장 설치 + [n/N] 진행 카운터 표시
- [ ] 개별 도구 실패 시 5초 후 1회 자동 재시도
- [ ] Post-install 작업 (Git autocrlf 자동 / Git 설정 안내 / pip 업그레이드 / npm fund false / PATH 검증 출력)
- [ ] Cursor: [8] 수동 설치 메뉴에서 URL 직접 오픈 (winget 시도 없음)
- [ ] 설치 완료 리포트 2종 생성 (install-report-[날짜].txt 요약 + install-log-[날짜].txt 상세)
- [ ] 업데이트 (전체)
- [ ] 제거 (개별 + 전체)
- [ ] 수동 설치 안내 (Cursor 최상단 강조)
- [ ] 설치 상태 확인 (O/X + 버전)

### "완료" 체크리스트
- [ ] 새 Windows 11 PC에서 왕초보 설치 후 `git --version && python --version && node --version` 성공
- [ ] 새 Windows 10 21H2 PC에서 동일 테스트 성공
- [ ] 이미 설치된 환경 재실행 시 오류 없이 완료
- [ ] install-report.txt 정상 생성 확인
- [ ] Git 설정 안내 후 첫 커밋 성공

### Phase 1 시작 프롬프트
```
이 PRD를 읽고 DEV-KIT.bat를 구현해주세요.
@PRD/01_PRD.md
@PRD/02_DATA_MODEL.md
@PRD/04_PROJECT_SPEC.md

Phase 1 구현 범위:
- 4단계 레벨 메뉴 (왕초보/중급/고급/올인원)
- 사전 체크 (winget/디스크/인터넷/충돌)
- 의존성 순서 보장 설치
- Post-install 작업 (Git 설정, pip 업그레이드, Ollama 안내)
- Cursor winget 폴백 구조
- 설치 리포트 파일 생성
- 단일 BAT 파일로 완성

반드시 지켜야 할 것:
- 04_PROJECT_SPEC.md의 DO NOT 목록 준수
- 오류 시 강제 종료 없이 "건너뜀" 처리
- Git 이메일/이름 자동 저장 금지 (안내만)
```

---

## Phase 2: 확장

### 전제 조건
- Phase 1 BAT 파일이 10명 이상 수강생에게 배포 및 검증됨

### 목표
더 강력한 오류 처리 + 더 나은 사용자 경험

### 기능
- [ ] BAT 런처 + PowerShell 7 로직 분리 (더 강력한 UI)
- [ ] 설치 완료 후 각 도구 버전 자동 출력
- [ ] 단계별 업그레이드 경로 명확화 (왕초보 → 중급 추가만)
- [ ] 색상 구분 (성공=녹색, 실패=빨강, 건너뜀=노랑)
- [ ] 진행률 표시 (3/7 설치 완료...)
- [ ] VS Code 확장 자동 설치 옵션

---

## Phase 3: 고도화

### 기능
- [ ] GUI 런처 (.exe) 검토
- [ ] 설치 프로파일 저장/불러오기 (내 설정 공유)
- [ ] 오프라인 설치 패키지 지원
- [ ] PATH 새로고침 자동화 (재시작 없이 즉시 사용)
- [ ] 기업/학교 방화벽 환경 전용 모드

---

## Phase 로드맵

| Phase | 핵심 기능 | 기술 | 상태 |
|-------|----------|------|------|
| Phase 1 (MVP) | 4단계 레벨, post-install, 리포트 | 순수 BAT | 구현 대기 |
| Phase 2 | PS 분리, 색상, 진행률 | BAT + PS1 | Phase 1 완료 후 |
| Phase 3 | GUI, 프로파일, 오프라인 | TBD | Phase 2 완료 후 |
