"""
faq_page.py — FAQ 탭 Page Object

이 파일의 역할:
FAQ 탭의 아코디언(접었다 펼치는 메뉴) 동작을 메서드로 정의.

━━━ 아코디언 상태 판별 방식 주의사항 ━━━━━━━━━━━━━━━━
이 페이지의 아코디언은 CSS max-height 방식으로 열고 닫힘.
→ 닫혀 있어도 DOM에 요소가 존재하기 때문에 to_be_hidden()으로 감지 안 됨
→ 대신 .open 클래스가 붙었는지/안 붙었는지로 상태 판단
"""

import re      # 정규표현식 모듈: 클래스 이름에서 "open" 단어를 정확히 찾기 위해 사용
import allure
from playwright.sync_api import Page, expect
from .base_page import BasePage


class FAQPage(BasePage):

    def go_to_tab(self):
        """FAQ 탭으로 이동"""
        self.click_tab("FAQ")

    def toggle(self, faq_id: str):
        """
        아코디언 헤더를 클릭해서 열거나 닫음
        faq_id: "faq-1" ~ "faq-4" 중 하나
        f"#{faq_id} .accordion-header" → id가 faq_id인 요소 안의 .accordion-header 를 찾음
        """
        with allure.step(f"아코디언 클릭: #{faq_id}"):
            self.page.locator(f"#{faq_id} .accordion-header").click()

    # ════════════════════════════════════════════════════
    # 검증 메서드
    # ════════════════════════════════════════════════════

    def expect_open(self, faq_id: str):
        """
        아코디언이 열린 상태인지 확인 → .open 클래스가 붙어있어야 통과
        to_have_class(re.compile(r"\bopen\b"))
          re.compile() : 정규표현식 패턴 객체 생성
          r"\bopen\b"  : \b 는 단어 경계. "open" 이라는 단어만 정확히 매칭
                         예) "reopen" 이나 "opened" 는 매칭 안 됨
        """
        expect(self.page.locator(f"#{faq_id}")).to_have_class(re.compile(r"\bopen\b"))

    def expect_closed(self, faq_id: str):
        """
        아코디언이 닫힌 상태인지 확인 → .open 클래스가 없어야 통과
        get_attribute("class") : 요소의 class 속성 전체를 문자열로 반환
        or ""                  : class 속성이 없을 경우 None 대신 빈 문자열 반환
        assert "open" not in   : "open" 이 포함되어 있으면 AssertionError 발생 → 테스트 실패
        """
        assert "open" not in (
            self.page.locator(f"#{faq_id}").get_attribute("class") or ""
        ), f"#{faq_id} 는 닫혀 있어야 합니다"   # 실패 시 출력할 메시지

    def expect_body_text(self, faq_id: str, text: str):
        """
        아코디언이 열렸을 때 본문 내용에 특정 텍스트가 포함되는지 확인
        faq_id-body 패턴: "faq-1" → "#faq-1-body" 선택자로 본문 요소를 찾음
        """
        expect(
            self.page.locator(f"#{faq_id}-body")
        ).to_contain_text(text)
