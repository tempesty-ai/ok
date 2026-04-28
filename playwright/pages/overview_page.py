"""
overview_page.py — 개요 탭 Page Object

이 파일의 역할:
개요 탭의 통계 카드, 호버 툴팁, 공지 수정 동작을 메서드로 정의.
"""

import allure
from playwright.sync_api import Page, expect
from .base_page import BasePage


class OverviewPage(BasePage):

    # ── 통계 카드 정보 딕셔너리 ─────────────────────────────
    # 카드 키 → (카드 전체 선택자, 숫자 선택자, 툴팁 텍스트) 튜플로 구성
    # 예) STAT_CARDS["total"] → ("#stat-total", "#stat-num-total", "전체 등록 작업 수")
    # 인덱스 0: 카드 전체, 1: 숫자 요소, 2: 기대 툴팁 텍스트
    STAT_CARDS = {
        "total":   ("#stat-total",   "#stat-num-total",   "전체 등록 작업 수"),
        "done":    ("#stat-done",    "#stat-num-done",    "완료 처리된 작업"),
        "high":    ("#stat-high",    "#stat-num-high",    "우선순위 높음 작업"),
        "members": ("#stat-members", "#stat-num-members", "프로젝트 참여 인원"),
    }

    # ════════════════════════════════════════════════════
    # 액션 메서드
    # ════════════════════════════════════════════════════

    def hover_stat_card(self, card_key: str):
        """
        통계 카드에 마우스 커서를 올림 (클릭 아님)
        STAT_CARDS[card_key][0] → 딕셔너리에서 카드 키로 튜플을 꺼내고, 첫 번째(인덱스 0) 값인 카드 선택자를 사용
        .hover() → 마우스 이동 동작 (CSS :hover 상태 트리거)
        """
        card_selector = self.STAT_CARDS[card_key][0]
        with allure.step(f"'{card_key}' 카드 호버"):
            self.page.locator(card_selector).hover()

    def get_tooltip_text(self, card_key: str) -> str:
        """
        카드 안의 툴팁 텍스트를 반환
        f"{card_selector} .tooltip" → 카드 안에 있는 .tooltip 클래스 요소를 찾음
        .text_content() → 요소의 텍스트를 문자열로 반환
        or "" → None 방지
        """
        card_selector = self.STAT_CARDS[card_key][0]
        return self.page.locator(f"{card_selector} .tooltip").text_content() or ""

    def edit_notice(self, new_text: str):
        """
        공지 수정 전체 흐름을 한 번에 처리하는 메서드
        순서: 수정 버튼 클릭 → textarea에 새 내용 입력 → 저장 버튼 클릭
        new_text[:20] → 문자열의 앞 20글자만 잘라서 allure step 이름에 표시
        """
        with allure.step(f"공지 수정: '{new_text[:20]}...'"):
            self.page.locator("#edit-notice-btn").click()   # 수정 버튼 → textarea 열림
            self.page.locator("#notice-editor").fill(new_text)  # 새 공지 입력
            self.page.locator("#save-notice-btn").click()   # 저장

    # ════════════════════════════════════════════════════
    # 검증 메서드
    # ════════════════════════════════════════════════════

    def expect_stat_number(self, card_key: str, value: str):
        """
        통계 카드의 숫자가 기대값과 일치하는지 확인
        STAT_CARDS[card_key][1] → 튜플의 두 번째(인덱스 1) 값인 숫자 요소 선택자
        to_have_text() → 정확히 일치해야 통과
        """
        num_selector = self.STAT_CARDS[card_key][1]
        expect(self.page.locator(num_selector)).to_have_text(value)

    def expect_tooltip_visible(self, card_key: str):
        """마우스 올린 후 툴팁이 보이는지 확인"""
        card_selector = self.STAT_CARDS[card_key][0]
        # 카드 선택자 안의 .tooltip 요소가 화면에 보여야 통과
        expect(self.page.locator(f"{card_selector} .tooltip")).to_be_visible()

    def expect_notice_contains(self, text: str):
        """공지 영역에 특정 텍스트가 포함되는지 확인"""
        expect(self.page.locator("#notice-text")).to_contain_text(text)

    def expect_editor_hidden(self):
        """저장 후 textarea(입력창)가 다시 숨겨졌는지 확인"""
        expect(self.page.locator("#notice-editor")).to_be_hidden()
