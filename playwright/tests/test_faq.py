"""
test_faq.py — FAQ 아코디언 테스트

이 파일에서 배울 것:
- 파라미터라이즈로 4개 아코디언 항목을 한 번에 검증
- exclusive open(하나만 열리는) 동작을 다양한 조합으로 검증
- FAQPage POM을 통해 테스트 코드에서 locator 분리
"""

import pytest
import allure
from pages.faq_page import FAQPage    # POM 클래스 임포트


@allure.epic("Project Dashboard")
@allure.feature("FAQ")
class TestAccordion:

    @allure.story("아코디언 열기")
    @allure.severity(allure.severity_level.NORMAL)
    # 4개 항목 × (faq_id, 본문에 포함되어야 할 텍스트) 조합으로 파라미터라이즈
    @pytest.mark.parametrize(
        "faq_id, expected_text",
        [
            ("faq-1", "Microsoft"),   # Playwright 소개 → 본문에 "Microsoft" 있어야 함
            ("faq-2", "CSS"),         # 학습 순서 → 본문에 "CSS" 있어야 함
            ("faq-3", "페이지"),       # POM 설명 → 본문에 "페이지" 있어야 함
            ("faq-4", "Headless"),    # Headless 설명 → 본문에 "Headless" 있어야 함
        ],
        ids=["Playwright소개", "학습순서", "POM설명", "Headless설명"],
    )
    def test_accordion_open_content(
        self,
        faq_page: FAQPage,       # conftest.py의 faq_page fixture 자동 주입
        faq_id: str,             # 파라미터: 아코디언 id
        expected_text: str,      # 파라미터: 본문에 있어야 할 텍스트
    ):
        """각 아코디언 항목을 열면 .open 클래스가 붙고 본문 내용이 노출되는지 확인"""
        faq_page.expect_closed(faq_id)            # 클릭 전: 닫혀있어야 함
        faq_page.toggle(faq_id)                   # 헤더 클릭 → 열기
        faq_page.expect_open(faq_id)              # 클릭 후: .open 클래스 확인
        faq_page.expect_body_text(faq_id, expected_text)  # 본문 텍스트 확인

    @allure.story("Exclusive Open (하나만 열리는 동작)")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    # A→B, B→C, C→D 순으로 인접한 항목 전환 조합 3가지 테스트
    @pytest.mark.parametrize(
        "first_id, second_id",
        [
            ("faq-1", "faq-2"),   # faq-1 열고 → faq-2 열면 → faq-1 닫혀야 함
            ("faq-2", "faq-3"),
            ("faq-3", "faq-4"),
        ],
        ids=["1→2", "2→3", "3→4"],
    )
    def test_accordion_exclusive(
        self,
        faq_page: FAQPage,
        first_id: str,    # 먼저 열 항목
        second_id: str,   # 나중에 열 항목
    ):
        """A를 열고 B를 열면 A는 자동으로 닫히는지 확인 (동시에 하나만 열림)"""
        faq_page.toggle(first_id)          # A 열기
        faq_page.expect_open(first_id)     # A 열렸는지 확인

        faq_page.toggle(second_id)         # B 클릭
        faq_page.expect_closed(first_id)   # A는 자동으로 닫혀야 함
        faq_page.expect_open(second_id)    # B는 열려야 함

    @allure.story("아코디언 토글 닫기")
    @allure.severity(allure.severity_level.MINOR)
    def test_accordion_toggle_close(self, faq_page: FAQPage):
        """같은 항목을 두 번 클릭하면 닫히는지 확인 (토글 동작)"""
        faq_page.toggle("faq-1")          # 첫 번째 클릭 → 열림
        faq_page.expect_open("faq-1")     # 열렸는지 확인

        faq_page.toggle("faq-1")          # 두 번째 클릭 → 닫힘
        faq_page.expect_closed("faq-1")   # 닫혔는지 확인
