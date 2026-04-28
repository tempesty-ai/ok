"""
stats_page.py — 통계 탭 Page Object

이 파일의 핵심:
Playwright의 page.route() 를 사용한 네트워크 인터셉트 기능.
Selenium에는 없는 기능으로, 실제 서버 없이 API 응답을 가로채서
다양한 응답 시나리오(정상/오류)를 테스트할 수 있음.
"""

import allure
from playwright.sync_api import Page, expect
from .base_page import BasePage

# 인터셉트할 API URL 상수로 관리 (여러 메서드에서 반복 사용)
API_URL = "https://jsonplaceholder.typicode.com/todos/1"


class StatsPage(BasePage):

    def go_to_tab(self):
        """통계 탭으로 이동"""
        self.click_tab("통계")

    def click_api_btn(self):
        """API 호출 버튼 클릭 — 클릭 시 fetch 요청이 발생함"""
        with allure.step("API 호출 버튼 클릭"):
            self.page.locator("#fetch-api-btn").click()

    def mock_api(self, body: str):
        """
        API 응답을 가짜(Mock) 데이터로 대체
        page.route(URL, 처리함수) → URL 요청이 발생하면 실제 서버 대신 처리함수 실행
        lambda route → 익명 함수: route 객체를 받아 fulfill(응답)으로 처리
        route.fulfill() → 지정한 내용으로 응답을 돌려줌
          status=200           : HTTP 성공 코드
          content_type="..."   : 응답 형식 (JSON)
          body=body            : 실제 응답 내용 (JSON 문자열)
        """
        self.page.route(
            API_URL,
            lambda route: route.fulfill(
                status=200,
                content_type="application/json",
                body=body,
            ),
        )

    def abort_api(self):
        """
        API 요청을 강제로 차단 (네트워크 오류 시뮬레이션)
        route.abort() → 요청 자체를 막아버림 → 브라우저에서 fetch 에러 발생
        → UI가 네트워크 오류를 올바르게 처리하는지 테스트할 때 사용
        """
        self.page.route(
            API_URL,
            lambda route: route.abort(),
        )

    # ════════════════════════════════════════════════════
    # 검증 메서드
    # ════════════════════════════════════════════════════

    def expect_bar_value(self, bar_id: str, value: str):
        """
        막대 차트 특정 항목의 숫자가 맞는지 확인
        bar_id 예) "bar-high-val", "bar-medium-val", "bar-low-val"
        f"#{bar_id}" → id가 bar_id인 요소 선택
        """
        expect(self.page.locator(f"#{bar_id}")).to_have_text(value)

    def expect_completion_rate(self, rate: str):
        """완료율 텍스트 확인. 예) expect_completion_rate("58%")"""
        expect(self.page.locator("#completion-rate")).to_have_text(rate)

    def expect_api_result_loaded(self, state: str):
        """
        API 결과 영역이 표시되고, data-loaded 속성값이 state와 일치하는지 확인
        state: "true" (성공) | "error" (실패)
        assert 문: 조건이 False이면 AssertionError 발생 → 테스트 실패
        """
        result = self.page.locator("#api-result")
        expect(result).to_be_visible()   # 결과 영역이 보여야 함
        assert result.get_attribute("data-loaded") == state, \
            f"data-loaded 기대값={state}, 실제값={result.get_attribute('data-loaded')}"

    def expect_api_contains(self, text: str):
        """API 결과 영역에 특정 텍스트가 포함되는지 확인"""
        expect(self.page.locator("#api-result")).to_contain_text(text)
