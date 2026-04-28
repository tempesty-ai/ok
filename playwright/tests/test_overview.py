"""
test_overview.py — 개요 탭 테스트 (통계 카드 숫자, 호버 툴팁, 공지 수정)

이 파일에서 배울 것:
- 4개 통계 카드를 파라미터라이즈로 한 번에 검증
- hover(마우스 올리기) 동작 테스트
- 인라인 편집(입력창 열기 → 저장) 플로우 테스트
"""

import pytest
import allure
from pages.overview_page import OverviewPage


@allure.epic("Project Dashboard")
@allure.feature("개요")
class TestStatCards:

    @allure.story("통계 카드 숫자")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke   # 핵심 케이스: smoke 테스트에 포함
    # 카드 키와 화면에 표시되어야 할 숫자를 4가지 조합으로 테스트
    @pytest.mark.parametrize(
        "card_key, expected_value",
        [
            ("total",   "12"),   # 전체 작업 수 → 12
            ("done",    "7"),    # 완료 수 → 7
            ("high",    "3"),    # 긴급(높음) 수 → 3
            ("members", "5"),    # 팀원 수 → 5
        ],
        ids=["전체작업", "완료", "긴급", "팀원"],
    )
    def test_stat_card_numbers(
        self,
        overview_page: OverviewPage,   # conftest.py의 overview_page fixture 자동 주입
        card_key: str,
        expected_value: str,
    ):
        """각 통계 카드의 숫자가 올바른지 확인"""
        # OverviewPage의 expect_stat_number → 내부에서 locator 처리
        overview_page.expect_stat_number(card_key, expected_value)

    @allure.story("호버 툴팁")
    @allure.severity(allure.severity_level.MINOR)
    # 카드 키와 마우스를 올렸을 때 표시되어야 할 툴팁 텍스트를 파라미터로 전달
    @pytest.mark.parametrize(
        "card_key, expected_tooltip",
        [
            ("total",   "전체 등록 작업 수"),
            ("done",    "완료 처리된 작업"),
            ("high",    "우선순위 높음 작업"),
            ("members", "프로젝트 참여 인원"),
        ],
        ids=["전체툴팁", "완료툴팁", "긴급툴팁", "팀원툴팁"],
    )
    def test_hover_tooltip(
        self,
        overview_page: OverviewPage,
        card_key: str,
        expected_tooltip: str,
    ):
        """통계 카드에 마우스를 올리면 올바른 툴팁이 표시되는지 확인"""
        overview_page.hover_stat_card(card_key)          # 마우스 올리기
        overview_page.expect_tooltip_visible(card_key)   # 툴팁 표시 확인

        # 툴팁 텍스트 내용도 직접 꺼내서 검증
        actual = overview_page.get_tooltip_text(card_key)
        # assert 조건, 실패 메시지 형태
        # 조건이 False면 테스트 실패, 실패 메시지가 출력됨
        assert expected_tooltip in actual, \
            f"툴팁 불일치: 기대={expected_tooltip}, 실제={actual}"


@allure.epic("Project Dashboard")
@allure.feature("개요")
class TestNoticeEdit:

    @allure.story("공지 수정")
    @allure.severity(allure.severity_level.NORMAL)
    # 서로 다른 공지 내용 2가지를 각각 테스트
    @pytest.mark.parametrize(
        "new_notice",
        [
            "다음 주 월요일 배포 예정입니다.",
            "오늘 오후 6시 긴급 패치가 있습니다.",
        ],
        ids=["배포공지", "긴급패치공지"],
    )
    def test_edit_notice(self, overview_page: OverviewPage, new_notice: str):
        """공지 수정 후 내용이 반영되고 에디터(textarea)가 닫히는지 확인"""
        # edit_notice: 수정버튼 클릭 → 입력 → 저장까지 한 번에 처리
        overview_page.edit_notice(new_notice)

        # new_notice[:10] → 앞 10글자만 잘라서 포함 여부 확인
        # (전체 문자열로 확인해도 되지만, 앞부분만 확인하는 방식도 실무에서 자주 씀)
        overview_page.expect_notice_contains(new_notice[:10])

        # 저장 후 입력창이 사라졌는지 확인
        overview_page.expect_editor_hidden()
