# Playwright QA Portfolio

Playwright + Pytest 기반으로 유지보수 가능한 UI 회귀 테스트를 구성한 QA 시나리오 모음입니다.

## QA 관점
- 목적: 핵심 사용자 여정의 회귀 리스크를 구조적으로 관리
- 방식: 테스트를 기능 단위로 분리하고, 실패 증거(스크린샷)를 자동 수집
- 포지셔닝: 자동화 자체보다 품질 판단과 릴리즈 안정성 확보에 초점

## 테스트 전략
| 시나리오 유형 | 적용 방식 | 기대 효과 |
|---|---|---|
| 핵심 사용자 플로우 | pytest 기반 회귀 자동화 | 변경 영향 빠른 탐지 |
| 상태/필터/진행률 검증 | 데이터 기반 검증 | 기능 신뢰도 확보 |
| 실패 분석 | Allure + 스크린샷 첨부 | 원인 파악 및 커뮤니케이션 속도 향상 |

## 품질 지표 (이 폴더 기준)
- 회귀 안정성: 동일 커밋에서 반복 실행 시 결과 일관성
- 실패 분석 리드타임: 실패 발생부터 원인 파악까지 시간
- 변경 영향 탐지율: 기능 변경 시 연관 시나리오에서의 조기 탐지 수준

## 구성
- `tests/`: 기능별 pytest 테스트
- `pages/`: Page Object Model 기반 화면 동작/검증 분리
- `conftest.py`: 공통 fixture + 실패 시 스크린샷(Allure 첨부)
- `test_demo.py`: 같은 기능을 한 파일로 확인할 수 있는 학습용 샘플
- `demo_page.html`: 테스트 대상 페이지
- `requirements.txt`: 의존성

## 테스트 범위
- 탭 전환
- 툴팁 검증
- 작업 추가/완료/삭제
- 진행률 계산
- 우선순위/완료 필터
- FAQ 아코디언
- 공지 수정
- API intercept/abort
- 페이지 타이틀/스크린샷/통계 검증

## 테스트 케이스 상세
### Navigation / Overview
| ID | 테스트 함수 | 시나리오 | 검증 포인트 |
|---|---|---|---|
| PW-01 | `test_tab_switch_click` | 개요에서 작업 관리 탭으로 이동 | 선택한 탭 패널은 보이고 기존 패널은 숨겨지는지 확인 |
| PW-02 | `test_tab_switch_all` | 전체 탭 순차 이동 | 개요, 작업 관리, FAQ, 통계 탭 전환이 모두 정상 동작하는지 확인 |
| PW-03 | `test_hover_tooltip` | 통계 카드 툴팁 단건 확인 | 마우스 hover 시 툴팁이 표시되고 설명 문구가 맞는지 확인 |
| PW-04 | `test_hover_tooltip_all_cards` | 통계 카드 툴팁 전체 확인 | 전체/완료/긴급/팀원 카드의 툴팁 문구가 각각 맞는지 확인 |
| PW-05 | `test_edit_notice` | 공지 인라인 수정 | 수정 입력창 노출, 저장 후 텍스트 반영, 성공 토스트 표시를 확인 |
| PW-06 | `test_page_title` | 페이지 제목 확인 | 브라우저 title이 기대값과 일치하는지 확인 |

### Task Management
| ID | 테스트 함수 | 시나리오 | 검증 포인트 |
|---|---|---|---|
| PW-07 | `test_add_task_via_button` | 버튼으로 작업 추가 | 입력값이 작업 목록에 추가되고 텍스트가 올바른지 확인 |
| PW-08 | `test_add_task_via_enter_key` | Enter 키로 작업 추가 | 버튼 클릭 없이 키보드 입력만으로 작업이 추가되는지 확인 |
| PW-09 | `test_add_task_empty_shows_toast` | 빈 작업 추가 예외 처리 | 입력값 없이 추가 시 에러 토스트가 표시되는지 확인 |
| PW-10 | `test_task_complete_and_progress` | 작업 완료 및 진행률 100% | 체크박스 완료 처리 후 완료 스타일과 진행률 100% 반영을 확인 |
| PW-11 | `test_progress_partial` | 일부 완료 진행률 계산 | 3개 중 1개 완료 시 진행률이 33%로 계산되는지 확인 |
| PW-12 | `test_priority_filter` | 우선순위 필터 | 높음/낮음 작업 중 높음 필터 적용 시 대상 작업만 보이는지 확인 |
| PW-13 | `test_filter_done` | 완료 필터 | 완료된 작업만 필터링되어 표시되는지 확인 |
| PW-14 | `test_delete_task` | 작업 삭제 | 삭제 후 목록이 비고 empty 메시지가 표시되는지 확인 |
| PW-15 | `test_delete_shows_toast` | 삭제 알림 | 작업 삭제 시 안내 토스트가 표시되는지 확인 |

### FAQ / Accordion
| ID | 테스트 함수 | 시나리오 | 검증 포인트 |
|---|---|---|---|
| PW-16 | `test_accordion_open` | FAQ 항목 열기 | 아코디언 클릭 시 `open` 클래스가 붙고 본문이 노출되는지 확인 |
| PW-17 | `test_accordion_exclusive` | FAQ 단일 열림 정책 | 다른 항목을 열면 기존 항목이 자동으로 닫히는지 확인 |
| PW-18 | `test_accordion_toggle_close` | FAQ 토글 닫기 | 같은 항목을 다시 클릭하면 닫히는지 확인 |

### API / Network
| ID | 테스트 함수 | 시나리오 | 검증 포인트 |
|---|---|---|---|
| PW-19 | `test_api_route_intercept` | API 응답 Mock 처리 | 실제 서버 응답 대신 Mock JSON을 주입하고 UI 반영 여부를 확인 |
| PW-20 | `test_api_route_abort` | API 실패 처리 | 네트워크 요청을 강제 차단했을 때 오류 상태가 표시되는지 확인 |

### Evidence / Visual / Stats
| ID | 테스트 함수 | 시나리오 | 검증 포인트 |
|---|---|---|---|
| PW-21 | `test_screenshot_overview` | 개요 화면 스크린샷 | 스크린샷 파일이 생성되고 크기가 0보다 큰지 확인 |
| PW-22 | `test_screenshot_per_tab` | 탭별 스크린샷 | 주요 탭별 화면 캡처가 정상 생성되는지 확인 |
| PW-23 | `test_stats_chart_values` | 통계 차트 값 검증 | 높음/중간/낮음 막대 값과 완료율이 기대값과 일치하는지 확인 |
| PW-24 | `test_stat_card_numbers` | 통계 카드 숫자 검증 | 전체/완료/긴급/팀원 수치가 기대값과 일치하는지 확인 |

## 케이스 선정 기준
- Selenium보다 구조화된 회귀 테스트를 보여주기 위해 pytest fixture, marker, Page Object 구조를 적용
- UI 상호작용뿐 아니라 API Mock/Abort, 스크린샷 증거 수집까지 포함해 실패 분석 관점을 반영
- 모든 기능을 자동화하기보다 핵심 플로우, 상태 계산, 오류 처리처럼 회귀 영향이 큰 영역을 우선 선정

## 실행 방법
```bash
cd playwright
pip install -r requirements.txt
playwright install
pytest -v
```

선별 실행:
```bash
pytest -m smoke
pytest -m regression
pytest -m api
```

브라우저 확인 실행:
```bash
pytest -v --headed --slowmo 800
```

학습용 단일 파일 직접 실행:
```bash
py test_demo.py
py test_demo.py --headed --slowmo 800
```

Allure 리포트:
```bash
pytest -v --alluredir=allure-results --clean-alluredir
allure serve allure-results
```

## 실무 활용 포인트
- 회귀 시나리오의 안정적 반복 실행
- 실패 근거 자동 수집으로 분석 시간 단축
- 기능 변경 시 영향 범위 확인을 위한 빠른 안전망
- `allure-results/`, `__pycache__/` 등 실행 산출물은 Git 추적 대상에서 제외
