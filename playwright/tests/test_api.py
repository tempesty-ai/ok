"""
test_api.py — API 인터셉트 테스트

━━━ Playwright route 란? ━━━━━━━━━━━━━━━━━━━━━━━━━━━━
page.route(URL, 처리함수) 를 사용하면
브라우저가 해당 URL로 요청을 보낼 때 실제 서버 대신 처리함수가 실행됨.

활용 시나리오:
1. Mock 응답 주입 (route.fulfill)
   → 서버가 없거나 특정 응답 데이터를 원할 때
   → 예) "서버가 '완료' 응답을 줬을 때 UI가 올바른지" 테스트

2. 요청 차단 (route.abort)
   → 네트워크 오류 상황을 시뮬레이션
   → 예) "API 호출 실패했을 때 에러 메시지가 뜨는지" 테스트

3. 요청 지연, 헤더 수정 등 다양한 조작도 가능

━━━ Selenium vs Playwright ━━━━━━━━━━━━━━━━━━━━━━━━━
Selenium: 네트워크 인터셉트 기본 미지원 (별도 프록시 툴 필요)
Playwright: page.route() 로 기본 내장 지원
"""

import pytest
import allure
from pages.stats_page import StatsPage


@allure.epic("Project Dashboard")
@allure.feature("통계 / API")
class TestApiIntercept:

    @allure.story("Mock 응답 주입")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    @pytest.mark.api    # api 마커: pytest -m api 로 API 관련 테스트만 실행 가능
    # "완료"와 "미완료" 두 가지 응답 케이스를 파라미터로 테스트
    @pytest.mark.parametrize(
        "title, completed",
        [
            ("QA 자동화 완료",    "true"),    # completed: true → 완료 케이스
            ("회귀 테스트 진행중", "false"),   # completed: false → 미완료 케이스
        ],
        ids=["완료_케이스", "미완료_케이스"],
    )
    def test_api_mock_response(
        self,
        stats_page: StatsPage,
        title: str,
        completed: str,
    ):
        """API 응답을 Mock으로 대체했을 때 화면에 올바르게 표시되는지 확인"""
        # f-string으로 JSON 문자열 동적 생성
        # {{ }} → f-string에서 중괄호 자체를 출력할 때 두 번 씀
        mock_body = f'{{"userId":1,"id":1,"title":"{title}","completed":{completed}}}'

        # stats_page.mock_api() → page.route() 인터셉트 등록
        # 이 시점에는 아직 요청이 안 보내진 상태. 등록만 해둠
        stats_page.mock_api(mock_body)

        # API 호출 버튼 클릭 → 이때 fetch 요청 발생 → route가 가로채서 mock_body 응답
        stats_page.click_api_btn()

        # 화면에 결과가 표시되고 data-loaded="true" 인지 확인
        stats_page.expect_api_result_loaded("true")

        # 화면에 mock 응답의 title 텍스트가 나오는지 확인
        stats_page.expect_api_contains(title)

    @allure.story("네트워크 오류 처리")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.api
    def test_api_abort_shows_error(self, stats_page: StatsPage):
        """
        API 요청을 강제 차단했을 때 UI가 오류 상태로 처리되는지 확인
        abort_api() → route.abort() 로 요청 자체를 막음 → fetch 에러 발생
        → JS의 .catch() 가 실행되어 data-loaded="error" 로 설정됨
        """
        stats_page.abort_api()           # 네트워크 차단 등록
        stats_page.click_api_btn()       # API 호출 시도 → 차단됨
        stats_page.expect_api_result_loaded("error")   # 오류 상태 확인


@allure.epic("Project Dashboard")
@allure.feature("통계 / API")
class TestChartData:

    @allure.story("막대 차트 데이터")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    # 막대 차트 3개 항목(높음/중간/낮음)의 숫자를 파라미터로 검증
    @pytest.mark.parametrize(
        "bar_id, expected_value",
        [
            ("bar-high-val",   "3"),   # 높음 바의 숫자 = 3
            ("bar-medium-val", "6"),   # 중간 바의 숫자 = 6
            ("bar-low-val",    "3"),   # 낮음 바의 숫자 = 3
        ],
        ids=["높음바", "중간바", "낮음바"],
    )
    def test_bar_chart_values(
        self,
        stats_page: StatsPage,
        bar_id: str,
        expected_value: str,
    ):
        """막대 차트 각 항목의 수치가 올바른지 확인"""
        stats_page.expect_bar_value(bar_id, expected_value)

    @allure.story("완료율")
    @allure.severity(allure.severity_level.MINOR)
    def test_completion_rate(self, stats_page: StatsPage):
        """완료율이 58%로 표시되는지 확인"""
        stats_page.expect_completion_rate("58%")
