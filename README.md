# Senior QA Engineer Portfolio

자동화 전담 포지션이 아니라, 릴리즈 품질과 리스크 관리 중심의 Senior QA Engineer 포트폴리오입니다.

## QA 포지셔닝
- 테스트 자동화 엔지니어 전담이 아닌, 제품 품질 전반을 책임지는 QA 엔지니어
- 요구사항 리뷰, 테스트 전략 수립, 회귀 범위 관리, 결함 분석, 릴리즈 게이트 운영 중심
- Selenium/Playwright는 반복 회귀와 핵심 플로우 보호를 위한 수단으로 활용

## 이 저장소의 목적
동일한 데모 페이지를 대상으로
- `selenium/`: 빠른 E2E 시나리오 검증
- `playwright/`: pytest 기반 구조화된 자동화 검증
을 구성해, 도구별 실무 적용 방식을 비교할 수 있게 했습니다.

## 테스트 전략
| 영역 | 접근 방식 | 기준 |
|---|---|---|
| 핵심 사용자 플로우 (로그인/데이터 상태 변경) | 자동화 우선 | 회귀 빈도 높고 실패 영향이 큰 기능 |
| 신규 기능 초기 검증 | 수동 + 탐색 테스트 | 요구사항 불확실성이 높고 UX 확인이 필요한 구간 |
| UI 디테일/예외 흐름 | 위험도 기반 선별 자동화 | 결함 이력과 사용자 영향도를 기준으로 우선순위화 |

## 품질 지표 (실무 관점)
- 결함 누수율: 스테이징/운영 단계에서 발견되는 이슈 비율 추적
- 회귀 소요시간: 배포 전 핵심 시나리오 검증 완료까지의 리드타임
- 릴리즈 게이트 충족률: 차단 이슈(Blocking/Critical) 해결 여부 기준 배포 승인
- flaky 테스트 비율: 신뢰도 낮은 테스트 탐지 및 제거 우선 관리

## 디렉터리
- `selenium/README.md`: Selenium 기반 시나리오
- `playwright/README.md`: Playwright 기반 시나리오

## 빠른 실행
페이지를 눈으로 확인:
```bat
open_selenium_demo.bat
open_playwright_demo.bat
```

자동화 테스트 실행:
```bat
run_selenium_tests.bat
run_playwright_tests.bat
run_playwright_headed.bat
```

테스트 실행에는 Python 3.10+가 필요합니다. Python이 없으면 스크립트가 설치 안내를 출력합니다.

## 제출 포인트
- Selenium은 한 파일에서 핵심 UI 상호작용을 빠르게 확인하는 스모크 성격으로 구성
- Playwright는 pytest, fixture, Page Object, marker, API mocking까지 포함해 유지보수 관점을 반영
- 실행 산출물은 저장소에서 제외하고, 재현 가능한 테스트 코드와 README 중심으로 정리

## 운영 메모
- 자동화 커버리지 자체보다 릴리즈 안정성 향상에 집중
- 테스트 코드는 팀 의사결정을 돕는 품질 증거로 사용
