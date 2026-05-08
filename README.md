# Senior QA Engineer 포트폴리오 - Web 자동화 기반

> 회귀 리스크를 줄이기 위한 실무형 UI 자동화 기반을 정리한 저장소입니다.
> 핵심은 자동화 자체가 아니라, QA가 무엇을 자동화할 가치가 있는지 판단하는 방식입니다.

## 데이터 안내

이 저장소의 테스트 시나리오, selector, 검증 기준은 `practicesoftwaretesting.com` 같은 공개 데모 사이트를 기반으로 합니다. 현재 또는 과거 회사/고객사 시스템의 화면, 데이터, selector, 내부 명세는 포함하지 않습니다.

## 문제

릴리즈 전 수동 회귀 점검은 시간이 오래 걸리고 사람마다 결과가 달라질 수 있습니다. 반대로 모든 화면을 자동화하는 것도 비용이 크고 가치가 낮은 경우가 많습니다.

이 저장소는 리스크 기반 접근을 보여줍니다. 반복적이고 영향도가 높은 핵심 사용자 흐름은 자동화로 보호하고, 탐색적이거나 불확실한 영역은 사람의 QA 판단 영역으로 남깁니다.

## 포지셔닝

| 영역 | 방향 |
| --- | --- |
| 역할 | 제품 품질 전체를 보는 QA Engineer |
| 강점 | 요구사항 검토, 테스트 전략, 회귀 범위 선정, 결함 분석, 릴리즈 게이트 |
| 자동화 활용 | 반복 회귀와 핵심 흐름 보호를 지원 |
| 범위 | QA 팀이 이해하고 운영할 수 있는 실용적 자동화 |

## Selenium과 Playwright를 함께 둔 이유

| 폴더 | 목적 | 특징 | 자동화 대상 |
| --- | --- | --- | --- |
| `selenium/` | 핵심 UI 흐름 smoke check | 단일 실행 스크립트, WebDriverWait, Select, ActionChains | 주요 진입 흐름 빠른 확인 |
| `playwright/` | pytest 기반 구조화 회귀 테스트 | Fixtures, Page Object, API mock, screenshots, headed mode | 유지보수성이 필요한 반복 회귀 |

어느 도구가 항상 더 좋다는 뜻이 아닙니다. 리스크, 반복 빈도, 유지보수 비용에 따라 도구를 선택하는 것이 핵심입니다.

## 테스트 전략

| 영역 | 접근 | 기준 |
| --- | --- | --- |
| 핵심 사용자 흐름 | 자동화 우선 | 회귀 빈도와 실패 영향도가 모두 높음 |
| 신규 기능 검증 | 수동 및 탐색적 테스트 | 요구사항이나 UX가 아직 불확실함 |
| UI 상호작용 | 리스크 기반 자동화 | 입력, dropdown, modal, 동적 loading, 반복 검증 |
| 실패 분석 | 증거 수집 | 빠른 진단을 위한 screenshot, log, state 값 |

## Selenium 케이스

| ID | 시나리오 | 검증 의도 |
| --- | --- | --- |
| TC-01 | 로그인 성공 | 기대 성공 상태 확인 |
| TC-02 | 로그인 실패/reset | 잘못된 입력과 reset 동작 확인 |
| TC-03 | 테이블 검색 필터 | 표시된 행이 키워드와 일치하는지 확인 |
| TC-04 | 테이블 행 데이터 | 주요 cell 값이 기대값과 일치하는지 확인 |
| TC-05 | Dropdown 선택 | value/text/index 선택 동작 확인 |
| TC-06 | 다중 checkbox | 선택 및 해제 상태 확인 |
| TC-07 | Modal popup | 열기, 닫기, 확인, 취소 상태 확인 |
| TC-08 | 동적 콘텐츠 로딩 | 생성된 DOM에 대한 explicit wait 확인 |
| TC-09 | Counter 클릭 | 반복 동작과 reset 상태 확인 |
| TC-10 | Drag and drop | ActionChains 이동 결과 확인 |

## Playwright 케이스

| 영역 | ID | 시나리오 |
| --- | --- | --- |
| Navigation | PW-01 to PW-06 | Tab, tooltip, notice, page title |
| Task Management | PW-07 to PW-15 | 추가, Enter key, empty value, progress, filter, delete |
| FAQ | PW-16 to PW-18 | Accordion open, single-open 정책, close toggle |
| API / Network | PW-19 to PW-20 | Mock API response와 aborted request 처리 |
| Evidence / Stats | PW-21 to PW-24 | Screenshot, tab capture, chart/stat 검증 |

## 결과

| 항목 | 측정 |
| --- | --- |
| 자동화된 핵심 회귀 케이스 | Selenium 10 + Playwright 24 = 34 cases |
| 핵심 흐름 회귀 시간 | 수동 약 30분 -> 자동화 약 3~4분 |
| 실패 증거 | Screenshot, console log, state capture |
| 유지보수 방식 | Page Object와 fixture 분리 |

위 값은 저장소 수준의 샘플 측정값이며, 회사 운영 시스템의 결과가 아닙니다.

## 빠른 실행

데모 페이지를 수동으로 엽니다.

```bash
open_selenium_demo.bat
open_playwright_demo.bat
```

자동화를 실행합니다.

```bash
run_selenium_tests.bat
run_playwright_tests.bat
run_playwright_headed.bat
```

Playwright를 직접 실행합니다.

```bash
cd playwright
py test_demo.py --headed --slowmo 800
```

## 설정

Python 3.10+를 권장합니다.

```bash
cd selenium
pip install -r requirements.txt
python test_demo.py

cd ../playwright
pip install -r requirements.txt
playwright install
pytest -v
```

Allure는 선택 사항입니다. 기본 pytest 흐름은 Allure가 설치되어 있지 않아도 실행할 수 있도록 구성했습니다.

## 운영 메모

- 목표는 자동화 개수가 아니라 릴리즈 안정성입니다.
- 낮은 가치의 넓은 커버리지보다 반복 회귀 후보를 우선합니다.
- 테스트 코드는 팀 의사결정을 지원하는 품질 증거로 봅니다.
- 실행 중 생성되는 산출물은 제외하고, 재현 가능한 코드와 문서만 git에 남깁니다.

## 로드맵

- API 계층 회귀 케이스 추가
- 시각적 회귀는 형제 저장소 `UI_Test`에서 관리
- CI 실패 알림을 형제 프로젝트 `botserver`와 연결

## 저장소 이름 변경 제안

`ok`는 더 명확한 저장소 이름으로 바꾸는 것을 고려할 수 있습니다.

- `qa-automation-portfolio`
- `web-regression-suite`
- `ui-automation-foundation`

변경 경로: GitHub web -> Settings -> General -> Repository name -> Rename.

이름을 바꾼 뒤에는 로컬 remote URL을 업데이트합니다.

```bash
git remote set-url origin https://github.com/tempesty-ai/<new-name>.git
```
