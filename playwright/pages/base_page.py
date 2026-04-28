"""
base_page.py — BasePage (모든 페이지 클래스의 부모)

━━━ POM(Page Object Model) 이란? ━━━━━━━━━━━━━━━━━━━━━━
페이지별로 "요소 찾기 + 동작 + 검증" 을 클래스 하나에 모아두는 설계 패턴.

[POM 없이 테스트 작성 시]
  page.locator("#task-input").fill("작업명")   ← 테스트 파일마다 이 코드가 반복됨
  → HTML id가 바뀌면 테스트 파일 10개를 다 수정해야 함

[POM 적용 시]
  task_page.add_task("작업명")                 ← 테스트 파일은 이 한 줄만 씀
  → HTML id가 바뀌면 task_page.py 1개만 수정하면 됨

BasePage: 모든 페이지에서 공통으로 쓰는 메서드를 여기에 모아둠
각 페이지 클래스(TaskPage, FAQPage 등)는 BasePage 를 상속받아 사용
"""

import allure
from playwright.sync_api import Page, expect


class BasePage:

    def __init__(self, page: Page):
        """
        생성자 — 페이지 오브젝트를 만들 때 Playwright의 page 객체를 받아서 저장
        page: 브라우저 탭 하나를 나타내는 객체. 모든 클릭/입력/검증의 출발점
        self.page 에 저장해두면 이 클래스의 모든 메서드에서 꺼내 쓸 수 있음
        """
        self.page = page

    def click_tab(self, tab_name: str):
        """
        상단 탭 버튼을 이름으로 찾아 클릭
        with allure.step(...) → Allure 리포트에 이 단계가 이름과 함께 기록됨
        f-string: f"'{tab_name}' 탭 클릭" → 변수 값이 문자열 안에 삽입됨
        """
        with allure.step(f"'{tab_name}' 탭 클릭"):
            # get_by_role("button", name=탭이름) → role이 button이고 텍스트가 탭이름인 요소 찾기
            self.page.get_by_role("button", name=tab_name).click()

    def expect_visible(self, selector: str):
        """
        요소가 화면에 보이는지 단언(Assert)
        expect(...).to_be_visible() → 보이지 않으면 테스트 실패로 처리됨
        selector: CSS 선택자 문자열 예) "#panel-tasks", ".toast"
        """
        expect(self.page.locator(selector)).to_be_visible()

    def expect_hidden(self, selector: str):
        """요소가 화면에 숨겨져 있는지 단언"""
        expect(self.page.locator(selector)).to_be_hidden()

    def expect_text(self, selector: str, text: str):
        """
        요소의 텍스트가 정확히 일치하는지 단언
        to_have_text() → 텍스트가 완전히 같아야 통과 (공백 포함)
        """
        expect(self.page.locator(selector)).to_have_text(text)

    def expect_contains(self, selector: str, text: str):
        """
        요소의 텍스트에 특정 문자열이 포함되는지 단언
        to_contain_text() → 일부만 포함되어 있어도 통과
        예) "로그인 성공! 환영합니다" 에서 "로그인 성공" 포함 여부 확인
        """
        expect(self.page.locator(selector)).to_contain_text(text)

    def get_attribute(self, selector: str, attr: str) -> str:
        """
        HTML 요소의 특정 속성값을 문자열로 반환
        예) get_attribute("#result", "data-result") → "success" 또는 "fail"
        or "" → 속성이 없으면 None 대신 빈 문자열 반환 (오류 방지)
        """
        return self.page.locator(selector).get_attribute(attr) or ""
