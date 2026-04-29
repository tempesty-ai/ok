# Senior QA Engineer Portfolio

자동화 전담 포지션보다는 릴리즈 품질과 리스크 관리를 중심으로 하는 Senior QA Engineer 포트폴리오입니다.

Selenium과 Playwright를 모두 사용했지만, 목적은 "자동화 프레임워크를 깊게 만든다"보다 "QA 관점에서 어떤 흐름을 자동화 대상으로 고르고, 어떻게 회귀 리스크를 줄일지 판단한다"에 가깝습니다.

## 포지셔닝

| 구분 | 방향 |
|---|---|
| 역할 | 제품 품질 전반을 보는 QA Engineer |
| 강점 | 요구사항 리뷰, 테스트 전략 수립, 회귀 범위 관리, 결함 분석, 릴리즈 게이트 운영 |
| 자동화 활용 | 반복 회귀와 핵심 플로우 보호를 위한 보조 수단 |
| 표현 수준 | 자동화 전문 엔지니어 수준의 과한 구조보다는, 실무 QA가 충분히 이해하고 운영 가능한 수준 |

## 프로젝트 구성

| 폴더 | 목적 | 특징 |
|---|---|---|
| `selenium/` | 핵심 UI 플로우를 빠르게 확인하는 스모크 테스트 | 단일 실행 파일, WebDriverWait, Select, ActionChains 중심 |
| `playwright/` | pytest 기반의 구조화된 회귀 테스트 | fixture, Page Object, API mock, screenshot, headed 실행 지원 |

상세 케이스 설명은 각 폴더 README에 더 자세히 정리했습니다.

- `selenium/README.md`: Selenium 기반 TC-01 ~ TC-10
- `playwright/README.md`: Playwright 기반 PW-01 ~ PW-24

## 테스트 전략

| 영역 | 접근 방식 | 기준 |
|---|---|---|
| 핵심 사용자 플로우 | 자동화 우선 | 회귀 빈도가 높고 실패 영향이 큰 기능 |
| 신규 기능 초기 검증 | 수동 + 탐색 테스트 | 요구사항 불확실성이 높고 UX 확인이 필요한 구간 |
| UI 상호작용 | 위험도 기반 선별 자동화 | 입력, 선택, 모달, 동적 로딩처럼 반복 검증이 많은 영역 |
| 실패 분석 | 로그/스크린샷/상태값 확인 | 실패 원인을 빠르게 공유할 수 있는 증거 확보 |

## Selenium 케이스 요약

| ID | 시나리오 | 검증 의도 |
|---|---|---|
| TC-01 | 로그인 성공 | 정상 계정 입력 시 성공 메시지와 상태값 확인 |
| TC-02 | 로그인 실패/초기화 | 잘못된 입력과 reset 동작 검증 |
| TC-03 | 테이블 검색 필터 | 키워드 입력에 따른 표시 행 개수 확인 |
| TC-04 | 테이블 행 데이터 | 주요 셀 데이터가 기대값과 일치하는지 확인 |
| TC-05 | 드롭다운 선택 | value/text/index 방식의 선택 결과 확인 |
| TC-06 | 체크박스 다중 선택 | 선택/해제 상태와 결과 영역 반영 확인 |
| TC-07 | 모달 팝업 | 열기/닫기/확인/취소 상태 검증 |
| TC-08 | 동적 콘텐츠 로드 | Explicit Wait 기반 DOM 생성 확인 |
| TC-09 | 카운터 반복 클릭 | 반복 액션 후 상태값과 reset 확인 |
| TC-10 | 드래그 앤 드롭 | ActionChains 기반 이동 결과 확인 |

## Playwright 케이스 요약

| 영역 | ID | 시나리오 |
|---|---|---|
| Navigation | PW-01 ~ PW-06 | 탭 전환, 툴팁, 공지 수정, 페이지 타이틀 확인 |
| Task Management | PW-07 ~ PW-15 | 작업 추가, Enter 입력, 빈 값 예외, 완료/진행률, 필터, 삭제 |
| FAQ | PW-16 ~ PW-18 | 아코디언 열기, 단일 열림 정책, 토글 닫기 |
| API / Network | PW-19 ~ PW-20 | API 응답 mock, 요청 abort 시 오류 처리 |
| Evidence / Stats | PW-21 ~ PW-24 | 스크린샷 생성, 탭별 캡처, 차트/통계 카드 값 검증 |

## 빠른 실행

페이지를 브라우저로 열어서 눈으로 확인:

```bat
open_selenium_demo.bat
open_playwright_demo.bat
```

자동화 테스트 실행:

```bat
run_selenium_tests.bat
run_playwright_tests.bat
```

Playwright를 브라우저가 보이는 상태로 실행:

```bat
run_playwright_headed.bat
```

Playwright 폴더에서 직접 실행할 수도 있습니다.

```bat
cd playwright
py test_demo.py --headed --slowmo 800
```

## 실행 전 준비

Python 3.10 이상이 필요합니다. 처음 실행하는 환경에서는 각 폴더의 의존성을 설치합니다.

```bat
cd selenium
pip install -r requirements.txt
python test_demo.py
```

```bat
cd playwright
pip install -r requirements.txt
playwright install
pytest -v
```

Allure는 선택 사항입니다. 설치되어 있지 않아도 기본 pytest 실행이 막히지 않도록 구성했습니다.

## 제출 포인트

| 포인트 | 설명 |
|---|---|
| QA 관점 | 자동화 자체보다 어떤 리스크를 줄이기 위한 테스트인지 드러나도록 구성 |
| Selenium | 한 파일에서 핵심 UI 상호작용을 빠르게 확인하는 스모크 성격 |
| Playwright | pytest fixture, Page Object, API mocking, screenshot을 포함해 유지보수 관점 반영 |
| 실행 편의성 | 루트 batch 파일로 브라우저 확인과 테스트 실행을 바로 할 수 있게 정리 |
| 저장소 관리 | 실행 산출물은 `.gitignore`로 제외하고 재현 가능한 코드와 문서 중심으로 관리 |

## 운영 메모

- 자동화 커버리지 숫자보다 릴리즈 안정성 향상에 집중했습니다.
- 모든 기능을 무리하게 자동화하기보다 반복 회귀 가능성이 높은 기능을 우선 선정했습니다.
- 테스트 코드는 팀 의사결정을 돕는 품질 증거로 사용한다는 관점으로 작성했습니다.
