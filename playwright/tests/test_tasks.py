"""
test_tasks.py — 작업 관리 탭 테스트

━━━ 이 파일에서 배울 핵심 패턴 ━━━━━━━━━━━━━━━━━━━━━━
1. @pytest.mark.parametrize
   - 같은 테스트 로직을 다른 데이터로 반복 실행
   - 예) 우선순위 3가지(높음/중간/낮음)를 따로 3개 테스트로 쓰지 않고
         데이터만 바꿔서 1개 테스트로 처리

2. @allure.epic / @allure.feature / @allure.story
   - Allure 리포트에 계층 구조(트리) 형태로 표시
   - epic > feature > story 순서 (큰 범위 → 작은 범위)

3. @allure.severity
   - 테스트 중요도 표시: CRITICAL > NORMAL > MINOR
   - 리포트에서 심각도별로 필터링 가능

4. POM 사용
   - 테스트 코드에 locator("#task-input") 같은 코드가 없음
   - 전부 task_page.add_task(), task_page.expect_count() 같은 메서드 호출만 함
"""

import pytest
import allure
from pages.task_page import TaskPage    # POM 클래스 임포트


# ════════════════════════════════════════════════════
# @allure.epic, @allure.feature 는 클래스 전체에 적용
# 클래스 안의 모든 테스트 메서드가 이 분류에 속하게 됨
# ════════════════════════════════════════════════════
@allure.epic("Project Dashboard")      # 가장 큰 분류 (앱 이름 수준)
@allure.feature("작업 관리")            # 기능 단위 분류
class TestTaskAdd:

    @allure.story("작업 추가")                          # 세부 시나리오 분류
    @allure.severity(allure.severity_level.CRITICAL)   # 심각도: 가장 중요한 기능
    @pytest.mark.smoke                                  # smoke 마커: pytest -m smoke 로 이것만 실행 가능
    # ─────────────────────────────────────────────────
    # @pytest.mark.parametrize 사용법
    #   첫 번째 인자: 파라미터 이름들 (콤마로 구분된 문자열 또는 리스트)
    #   두 번째 인자: 각 케이스 데이터 리스트 [(값1, 값2, ...), ...]
    #   ids         : 터미널/리포트에 표시될 케이스 이름
    # → 아래 3개 튜플이 각각 1번씩 총 3회 실행됨
    # ─────────────────────────────────────────────────
    @pytest.mark.parametrize(
        "task_text, priority, expected_tag",   # 테스트 함수의 인자 이름과 일치해야 함
        [
            ("긴급 서버 다운 버그",  "high",   "높음"),   # 케이스 1
            ("로그인 UI 개선",       "medium", "중간"),   # 케이스 2
            ("릴리즈 노트 문서화",   "low",    "낮음"),   # 케이스 3
        ],
        ids=["우선순위_높음", "우선순위_중간", "우선순위_낮음"],   # 각 케이스 이름
    )
    def test_add_task_with_priority(
        self,
        task_page: TaskPage,       # conftest.py의 task_page fixture가 자동 주입됨
        task_text: str,            # parametrize에서 넘어온 첫 번째 값
        priority: str,             # parametrize에서 넘어온 두 번째 값
        expected_tag: str,         # parametrize에서 넘어온 세 번째 값
    ):
        """우선순위별 작업 추가 후 태그가 올바른지 확인"""
        task_page.add_task(task_text, priority)     # TaskPage의 메서드 호출
        task_page.expect_task_count(1)              # 작업 1개 추가됐는지 확인
        task_page.expect_priority_tag(expected_tag) # 우선순위 태그 텍스트 확인

    @allure.story("작업 추가 — 빈값 예외 처리")
    @allure.severity(allure.severity_level.NORMAL)   # 심각도: 일반
    def test_add_empty_task_shows_error(self, task_page: TaskPage):
        """아무것도 입력하지 않고 추가 버튼 클릭 시 에러 토스트가 표시되는지 확인"""
        # task_page.ADD_BTN : TaskPage에 정의된 로케이터 상수
        # 직접 "#add-task-btn" 을 쓰지 않고 상수를 통해 접근
        task_page.page.locator(task_page.ADD_BTN).click()
        task_page.expect_toast("error", "작업 내용을 입력해주세요")

    @allure.story("다건 추가")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.parametrize(
        "task_count",       # 파라미터가 1개일 때는 리스트로 전달 (튜플 불필요)
        [1, 3, 5],
        ids=["1개", "3개", "5개"],
    )
    def test_add_multiple_tasks(self, task_page: TaskPage, task_count: int):
        """N개 작업을 추가했을 때 목록 개수가 정확한지 확인"""
        # range(task_count) → 0 ~ task_count-1 까지 반복
        # i + 1 → 1부터 시작하는 작업명 생성 ("테스트 작업 1", "테스트 작업 2", ...)
        for i in range(task_count):
            task_page.add_task(f"테스트 작업 {i + 1}")
        task_page.expect_task_count(task_count)   # 추가한 수만큼 있는지 확인


@allure.epic("Project Dashboard")
@allure.feature("작업 관리")
class TestTaskProgress:

    @allure.story("진행률 바")
    @allure.severity(allure.severity_level.NORMAL)
    # (완료 수, 전체 수, 기대 진행률 문자열) 4가지 조합을 파라미터로 전달
    @pytest.mark.parametrize(
        "done_count, total_count, expected_pct",
        [
            (1, 1, "100%"),   # 1개 중 1개 완료 = 100%
            (1, 3, "33%"),    # 3개 중 1개 완료 = 33%
            (2, 4, "50%"),    # 4개 중 2개 완료 = 50%
            (3, 4, "75%"),    # 4개 중 3개 완료 = 75%
        ],
        ids=["1/1=100%", "1/3=33%", "2/4=50%", "3/4=75%"],
    )
    def test_progress_rate(
        self,
        task_page: TaskPage,
        done_count: int,
        total_count: int,
        expected_pct: str,
    ):
        """N개 중 M개 완료 시 진행률이 올바른지 확인"""
        # total_count 개만큼 작업 추가
        for i in range(total_count):
            task_page.add_task(f"작업 {i + 1}")

        # done_count 개만큼 앞에서부터 완료 체크
        # check_task(i) → i번째(0부터) 작업 체크
        for i in range(done_count):
            task_page.check_task(i)

        # 진행률 텍스트가 expected_pct 와 일치하는지 확인
        task_page.expect_progress(expected_pct)


@allure.epic("Project Dashboard")
@allure.feature("작업 관리")
class TestTaskFilter:

    @allure.story("우선순위 필터")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression   # regression 마커: pytest -m regression 으로 이것만 실행 가능
    @pytest.mark.parametrize(
        "priority, filter_key, expected_count",
        [
            ("high",   "high",   1),   # 높음 필터 → 높음 1개만 표시
            ("medium", "medium", 1),   # 중간 필터 → 중간 1개만 표시
            ("low",    "low",    1),   # 낮음 필터 → 낮음 1개만 표시
        ],
        ids=["높음_필터", "중간_필터", "낮음_필터"],
    )
    def test_priority_filter(
        self,
        task_page: TaskPage,
        priority: str,
        filter_key: str,
        expected_count: int,
    ):
        """특정 우선순위 필터 선택 시 해당 항목만 표시되는지 확인"""
        # 3가지 우선순위 각각 1개씩 추가 (총 3개)
        task_page.add_task("높음 작업", "high")
        task_page.add_task("중간 작업", "medium")
        task_page.add_task("낮음 작업", "low")

        # 특정 우선순위 필터 적용
        task_page.filter_by(filter_key)

        # 해당 우선순위 1개만 보여야 함
        task_page.expect_task_count(expected_count)

    @allure.story("완료 필터")
    @allure.severity(allure.severity_level.MINOR)   # 심각도: 낮음
    def test_done_filter(self, task_page: TaskPage):
        """'완료됨' 필터 선택 시 체크된 항목만 표시되는지 확인"""
        task_page.add_task("완료 예정")
        task_page.add_task("미완료")
        task_page.check_task(0)          # 첫 번째 항목만 완료 처리
        task_page.filter_by("done")      # 완료된 항목만 보이는 필터
        task_page.expect_task_count(1)   # 완료된 1개만 보여야 함


@allure.epic("Project Dashboard")
@allure.feature("작업 관리")
class TestTaskDelete:

    @allure.story("작업 삭제")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    def test_delete_shows_empty_message(self, task_page: TaskPage):
        """마지막 작업 삭제 후 '등록된 작업이 없습니다' 메시지가 표시되는지 확인"""
        task_page.add_task("삭제될 작업")
        task_page.expect_task_count(1)   # 삭제 전: 1개

        task_page.delete_task(0)         # 첫 번째(0번) 작업 삭제

        task_page.expect_task_count(0)   # 삭제 후: 0개
        task_page.expect_empty()         # 빈 메시지 표시 확인

    @allure.story("작업 삭제")
    @allure.severity(allure.severity_level.MINOR)
    def test_delete_shows_toast(self, task_page: TaskPage):
        """삭제 시 파란색(info) 토스트 알림이 표시되는지 확인"""
        task_page.add_task("삭제 확인용")
        task_page.delete_task(0)
        # "info" → 파란색 토스트, text 인자 없이 표시 여부만 확인
        task_page.expect_toast("info")
