# Selenium QA Portfolio

Selenium을 활용해 핵심 사용자 플로우의 회귀 리스크를 빠르게 확인하는 QA 시나리오 모음입니다.

## QA 관점
- 목적: 기능 데모가 아니라, 릴리즈 전 기본 동작/회귀 이상 유무를 빠르게 판별
- 방식: 단일 스크립트에서 핵심 플로우를 연속 검증해 스모크 체크에 활용
- 포지셔닝: 자동화 전담보다 QA 엔지니어의 품질 검증 업무를 보조하는 자동화

## 테스트 전략
| 시나리오 유형 | 적용 방식 | 기대 효과 |
|---|---|---|
| 로그인/입력/상태 전환 | 필수 스모크 자동화 | 배포 전 치명 회귀 조기 탐지 |
| 테이블/필터/선택 기능 | 반복 회귀 자동화 | 수동 반복 시간 절감 |
| 동적 로딩/모달/드래그 | 안정성 검증 자동화 | 상호작용 오류 재현성 향상 |

## 품질 지표 (이 폴더 기준)
- 스모크 통과율: 핵심 플로우의 최소 품질 게이트 충족 여부
- 회귀 점검 시간: 스크립트 1회 실행 기준 품질 확인 속도
- 결함 재현 성공률: 동일 절차로 재현 가능한 테스트 케이스 비율

## 구성
- `test_demo.py`: 시나리오 기반 E2E 테스트
- `demo_page.html`: 테스트 대상 페이지
- `requirements.txt`: 의존성

## 테스트 범위 (TC-01 ~ TC-10)
- 로그인 성공/실패
- 테이블 검색 필터/데이터 검증
- 드롭다운 선택
- 체크박스 다중 선택
- 모달 팝업
- 동적 콘텐츠 Explicit Wait
- 카운터 반복 클릭
- 드래그 앤 드롭

## 테스트 케이스 상세
| ID | 시나리오 | 검증 포인트 | 사용 기능 |
|---|---|---|---|
| TC-01 | 로그인 성공 | 정상 계정 입력 시 성공 메시지가 노출되고 `data-result=success` 상태가 기록되는지 확인 | input, button, explicit wait, attribute |
| TC-02 | 로그인 실패/초기화 | 잘못된 비밀번호 입력 시 실패 상태가 표시되고, 초기화 버튼으로 입력값/결과 메시지가 정리되는지 확인 | negative case, reset flow, visibility |
| TC-03 | 테이블 검색 필터 | `QA`, `비활성` 키워드 검색 시 표시 행 개수가 기대값과 일치하는지 확인 | keyboard input, table filtering |
| TC-04 | 테이블 행 데이터 검증 | 첫 번째 행의 이름/역할/상태 데이터가 기대값과 일치하는지 확인 | table row/cell assertion |
| TC-05 | 드롭다운 선택 | value, visible text, index 방식으로 선택했을 때 결과 영역이 올바르게 갱신되는지 확인 | `Select`, option handling |
| TC-06 | 체크박스 다중 선택 | 여러 체크박스 선택 결과가 반영되고, 해제 시 결과에서 제거되는지 확인 | checkbox state, multi-select |
| TC-07 | 모달 팝업 | 모달 열림/닫힘, 확인/취소 버튼의 결과 상태가 각각 기록되는지 확인 | modal, click action, data attribute |
| TC-08 | 동적 콘텐츠 로드 | 로딩 문구 이후 동적 요소가 생성되고 `data-loaded=true` 상태가 되는지 확인 | `WebDriverWait`, dynamic DOM |
| TC-09 | 카운터 반복 클릭 | 버튼 5회 클릭 후 카운터 값이 5가 되고, 리셋 시 표시 영역이 숨겨지는지 확인 | repeated click, state reset |
| TC-10 | 드래그 앤 드롭 | 드래그 전 항목 위치와 드롭 후 target 영역 이동 여부를 확인 | `ActionChains`, drag and drop |

## 케이스 선정 기준
- 배포 전 빠르게 확인해야 하는 핵심 UI 동작을 우선 선정
- 입력, 선택, 검색, 모달, 동적 로딩처럼 실제 서비스 회귀에서 자주 깨지는 상호작용을 포함
- Selenium 학습 목적에 맞게 Locator, Wait, Select, ActionChains를 한 번씩 경험할 수 있도록 구성

## 실행 방법
```bash
cd selenium
pip install -r requirements.txt
python test_demo.py
```

## 실무 활용 포인트
- 배포 전 스모크 회귀 체크
- 재현 가능한 결함 확인 절차 표준화
- 기본 플로우 실패 시 릴리즈 게이트 근거로 활용

## 개선/학습 포인트
- 단순 `sleep`은 데모 안정성을 위해 일부만 사용하고, 실제 검증은 `WebDriverWait` 중심으로 구성
- 실패 원인을 빠르게 볼 수 있도록 각 케이스를 PASS/FAIL 로그로 분리
- 대규모 회귀 테스트로 확장할 경우 pytest fixture와 Page Object 구조로 분리 가능
