"""
task_page.py — 작업 관리 탭 Page Object

━━━ 이 파일의 역할 ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
작업 관리 탭과 관련된 모든 동작(추가/삭제/필터/체크)을 메서드로 정의.
테스트 파일(test_tasks.py)에서는 이 클래스의 메서드만 호출하면 됨.

━━━ 로케이터를 상수로 관리하는 이유 ━━━━━━━━━━━━━━━━
  나쁜 예) page.locator("#task-input").fill(...)   ← 테스트 파일 곳곳에 "#task-input" 반복
  좋은 예) self.page.locator(self.INPUT).fill(...) ← INPUT 상수 하나만 관리
  → id가 "task-field"로 바뀌면 상수 한 줄만 수정하면 모든 테스트가 자동 반영됨
"""

import allure
from playwright.sync_api import Page, expect

# BasePage 를 상속받음: .으로 접근하는 relative import
# pages 폴더 안에서 같은 폴더의 base_page.py 를 가져옴
from .base_page import BasePage


class TaskPage(BasePage):

    # ── 로케이터 상수 (CSS 선택자) ─────────────────────────
    # 클래스 변수로 선언하면 인스턴스 없이도 TaskPage.INPUT 으로 접근 가능
    INPUT        = "#task-input"               # 작업 입력창
    SELECT       = "#priority-select"          # 우선순위 드롭다운
    ADD_BTN      = "#add-task-btn"             # 추가 버튼
    ITEMS        = "#task-list .task-item"     # 작업 목록 아이템 전체
    EMPTY_MSG    = "#empty-msg"                # 목록 비었을 때 안내 문구
    PROGRESS     = "#progress-pct"            # 진행률 텍스트 (예: "33%")
    PROGRESS_BAR = "#progress-fill"           # 진행률 바 요소

    # 우선순위 영문 키 → 한글 레이블 매핑 딕셔너리
    # 예) PRIORITY_LABEL["high"] → "높음"
    PRIORITY_LABEL = {"high": "높음", "medium": "중간", "low": "낮음"}

    def go_to_tab(self):
        """작업 관리 탭으로 이동 — BasePage의 click_tab 재사용"""
        self.click_tab("작업 관리")

    # ════════════════════════════════════════════════════
    # 액션 메서드: 실제 사용자 동작을 흉내냄
    # ════════════════════════════════════════════════════

    def add_task(self, text: str, priority: str = "medium"):
        """
        작업을 추가한다.
        text     : 입력할 작업 내용
        priority : "high" | "medium" | "low" (기본값: medium)

        with allure.step(...) 안에 로직을 넣으면
        → Allure 리포트에 "작업 추가 | '긴급 버그' / 우선순위: 높음" 처럼 단계로 표시됨
        """
        with allure.step(f"작업 추가 | '{text}' / 우선순위: {self.PRIORITY_LABEL[priority]}"):
            # 드롭다운에서 우선순위 선택
            self.page.locator(self.SELECT).select_option(priority)
            # 입력창에 텍스트 입력
            self.page.locator(self.INPUT).fill(text)
            # Enter 키로 추가 (버튼 클릭과 동일한 효과)
            self.page.keyboard.press("Enter")

    def delete_task(self, index: int = 0):
        """
        n번째 작업의 삭제 버튼(✕)을 클릭
        index: 0부터 시작 → 0이면 첫 번째, 1이면 두 번째 항목
        .nth(index) → 여러 개 중 index번째 요소를 선택
        """
        with allure.step(f"{index + 1}번째 작업 삭제"):
            self.page.locator(".del-btn").nth(index).click()

    def check_task(self, index: int = 0):
        """
        n번째 작업의 체크박스를 클릭해 완료 처리
        f"{self.ITEMS} input[type=checkbox]" → 작업 아이템 안에 있는 checkbox 만 선택
        """
        with allure.step(f"{index + 1}번째 작업 완료 처리"):
            self.page.locator(f"{self.ITEMS} input[type=checkbox]").nth(index).check()

    def filter_by(self, filter_key: str):
        """
        우선순위 / 완료 필터 버튼 클릭
        filter_key: "all" | "high" | "medium" | "low" | "done"
        CSS 속성 선택자 [data-filter='high'] → data-filter 속성값이 "high"인 요소
        """
        with allure.step(f"필터 적용: '{filter_key}'"):
            self.page.locator(f".filter-btn[data-filter='{filter_key}']").click()

    # ════════════════════════════════════════════════════
    # 검증 메서드: 기대 결과를 단언(Assert)
    # ════════════════════════════════════════════════════

    def expect_task_count(self, count: int):
        """
        화면에 표시된 작업 아이템 수가 count개인지 확인
        to_have_count() → 개수가 다르면 테스트 실패
        """
        expect(self.page.locator(self.ITEMS)).to_have_count(count)

    def expect_progress(self, pct: str):
        """
        진행률 텍스트가 pct와 일치하는지 확인
        예) expect_progress("33%") → 화면에 "33%" 가 표시되어야 통과
        """
        expect(self.page.locator(self.PROGRESS)).to_have_text(pct)

    def expect_empty(self):
        """작업이 0개일 때 '등록된 작업이 없습니다' 문구가 보이는지 확인"""
        expect(self.page.locator(self.EMPTY_MSG)).to_be_visible()

    def expect_toast(self, toast_type: str, text: str = ""):
        """
        토스트 알림(화면 우상단 팝업)이 표시되는지 확인
        toast_type : "success"(초록) | "error"(빨강) | "info"(파랑)
        text       : 추가로 확인할 텍스트 (없으면 표시 여부만 확인)
        """
        toast = self.page.locator(f".toast.{toast_type}")
        expect(toast).to_be_visible()
        if text:
            expect(toast).to_contain_text(text)

    def expect_priority_tag(self, label: str):
        """
        목록의 첫 번째 항목에 붙은 우선순위 태그 텍스트 확인
        .first → locator로 찾은 여러 요소 중 첫 번째만 가져옴
        """
        expect(
            self.page.locator(f"{self.ITEMS} .priority-tag").first
        ).to_contain_text(label)
