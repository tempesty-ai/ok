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
- `test_demo.py`: 주요 시나리오
- `conftest.py`: 공통 fixture + 실패 시 스크린샷(Allure 첨부)
- `pages/`: 페이지 객체 구조
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

## 실행 방법
```bash
cd playwright
pip install -r requirements.txt
playwright install
pytest -v
```

브라우저 확인 실행:
```bash
pytest -v --headed --slowmo=800
```

Allure 리포트:
```bash
pytest -v --alluredir=allure-results
allure serve allure-results
```

## 실무 활용 포인트
- 회귀 시나리오의 안정적 반복 실행
- 실패 근거 자동 수집으로 분석 시간 단축
- 기능 변경 시 영향 범위 확인을 위한 빠른 안전망
