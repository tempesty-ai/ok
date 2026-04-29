import re                          # 정규표현식 (텍스트 패턴 비교에 사용)
import sys                         # 직접 실행 시 CLI 옵션 전달에 사용
import pytest                      # 파이썬 테스트 프레임워크
from pathlib import Path           # 파일 경로를 다루는 모듈
from playwright.sync_api import Page, expect, sync_playwright


PAGE_URL = "file:///" + str(Path(__file__).parent / "demo_page.html").replace("\\", "/")


def pytest_addoption(parser):
    parser.addoption("--headed", action="store_true", help="브라우저 창을 띄워서 실행")
    parser.addoption("--slowmo", action="store", type=int, default=0, help="동작 사이 지연(ms)")


@pytest.fixture(scope="session")
def browser(request):
    """Chromium은 한 번만 띄워서 단일 파일 실행 속도를 안정화한다."""
    headed = request.config.getoption("--headed", default=False)
    slowmo = request.config.getoption("--slowmo", default=0)
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=not headed, slow_mo=slowmo)
        yield browser
        browser.close()


@pytest.fixture(scope="session")
def shared_page(browser):
    page = browser.new_page()
    page.set_default_timeout(5000)
    yield page
    page.close()


@pytest.fixture()
def page(shared_page):
    # 시연 중 브라우저/탭을 계속 새로 열지 않고, 테스트마다 화면 상태만 초기화한다.
    if hasattr(shared_page, "unroute_all"):
        shared_page.unroute_all()
    shared_page.goto(PAGE_URL)
    yield shared_page

def test_tab_switch_click(page: Page):
    page.get_by_role("button", name="작업 관리").click()

    expect(page.locator("#panel-tasks")).to_be_visible()

    expect(page.locator("#panel-overview")).to_be_hidden()


def test_tab_switch_all(page: Page):
    tabs   = ["작업 관리", "FAQ", "통계", "개요"]
    panels = ["panel-tasks", "panel-faq", "panel-stats", "panel-overview"]

    for name, panel_id in zip(tabs, panels):
        page.get_by_role("button", name=name).click()           # 탭 클릭
        expect(page.locator(f"#{panel_id}")).to_be_visible()    # 해당 패널 표시 확인


def test_hover_tooltip(page: Page):
    card    = page.locator("#stat-total")
    tooltip = card.locator(".tooltip")

    expect(tooltip).to_be_hidden()

    card.hover()

    expect(tooltip).to_be_visible()

    expect(tooltip).to_contain_text("전체 등록 작업 수")


def test_hover_tooltip_all_cards(page: Page):
    expected = {
        "#stat-total":   "전체 등록 작업 수",
        "#stat-done":    "완료 처리된 작업",
        "#stat-high":    "우선순위 높음 작업",
        "#stat-members": "프로젝트 참여 인원",
    }

    for selector, text in expected.items():
        page.locator(selector).hover()                                    # 마우스 올리기
        expect(page.locator(selector).locator(".tooltip")).to_contain_text(text)  # 툴팁 검증


def test_add_task_via_button(page: Page):
    page.get_by_role("button", name="작업 관리").click()

    page.locator("#task-input").fill("로그인 회귀 테스트")

    page.locator("#add-task-btn").click()

    item = page.locator("#task-list .task-item")

    expect(item).to_have_count(1)

    expect(item.locator(".task-text")).to_contain_text("로그인 회귀 테스트")


def test_add_task_via_enter_key(page: Page):
    page.get_by_role("button", name="작업 관리").click()
    page.locator("#task-input").fill("성능 테스트 계획 수립")

    page.keyboard.press("Enter")

    expect(page.locator("#task-list .task-item")).to_have_count(1)


def test_add_task_empty_shows_toast(page: Page):
    page.get_by_role("button", name="작업 관리").click()
    page.locator("#add-task-btn").click()

    toast = page.locator(".toast.error")
    expect(toast).to_be_visible()
    expect(toast).to_contain_text("작업 내용을 입력해주세요")


def test_task_complete_and_progress(page: Page):
    page.get_by_role("button", name="작업 관리").click()
    page.locator("#task-input").fill("API 테스트 케이스 작성")
    page.keyboard.press("Enter")

    page.locator("#task-list .task-item input[type=checkbox]").check()

    expect(page.locator(".task-text.done")).to_be_visible()

    expect(page.locator("#progress-pct")).to_have_text("100%")

    expect(page.locator("#progress-fill")).to_have_attribute("style", re.compile(r"width:\s*100%"))


def test_progress_partial(page: Page):
    page.get_by_role("button", name="작업 관리").click()

    for text in ["작업 A", "작업 B", "작업 C"]:
        page.locator("#task-input").fill(text)
        page.keyboard.press("Enter")

    page.locator("#task-list .task-item").first.locator("input[type=checkbox]").check()

    expect(page.locator("#progress-pct")).to_have_text("33%")


def test_priority_filter(page: Page):
    page.get_by_role("button", name="작업 관리").click()

    page.locator("#priority-select").select_option("high")
    page.locator("#task-input").fill("긴급 버그 수정")
    page.keyboard.press("Enter")   # 높음 우선순위로 작업 추가

    page.locator("#priority-select").select_option("low")
    page.locator("#task-input").fill("문서 정리")
    page.keyboard.press("Enter")   # 낮음 우선순위로 작업 추가

    page.locator(".filter-btn[data-filter='high']").click()

    items = page.locator("#task-list .task-item")
    expect(items).to_have_count(1)
    expect(items.locator(".priority-tag")).to_contain_text("높음")


def test_filter_done(page: Page):
    page.get_by_role("button", name="작업 관리").click()

    for text in ["완료 작업", "미완료 작업"]:
        page.locator("#task-input").fill(text)
        page.keyboard.press("Enter")

    page.locator("#task-list .task-item").first.locator("input[type=checkbox]").check()

    page.locator(".filter-btn[data-filter='done']").click()

    expect(page.locator("#task-list .task-item")).to_have_count(1)
    expect(page.locator(".task-text.done")).to_be_visible()


def test_delete_task(page: Page):
    page.get_by_role("button", name="작업 관리").click()
    page.locator("#task-input").fill("삭제할 작업")
    page.keyboard.press("Enter")

    expect(page.locator("#task-list .task-item")).to_have_count(1)

    page.locator(".del-btn").click()

    expect(page.locator("#task-list .task-item")).to_have_count(0)

    expect(page.locator("#empty-msg")).to_be_visible()


def test_delete_shows_toast(page: Page):
    page.get_by_role("button", name="작업 관리").click()
    page.locator("#task-input").fill("삭제 토스트 확인용")
    page.keyboard.press("Enter")
    page.locator(".del-btn").click()

    expect(page.locator(".toast.info")).to_be_visible()


def test_accordion_open(page: Page):
    page.get_by_role("button", name="FAQ").click()

    item = page.locator("#faq-1")

    assert "open" not in (item.get_attribute("class") or "")

    item.locator(".accordion-header").click()

    expect(item).to_have_class(re.compile(r"\bopen\b"))

    expect(item.locator(".accordion-body-inner")).to_contain_text("Microsoft")


def test_accordion_exclusive(page: Page):
    page.get_by_role("button", name="FAQ").click()
    page.locator("#faq-1 .accordion-header").click()

    page.locator("#faq-2 .accordion-header").click()

    assert "open" not in (page.locator("#faq-1").get_attribute("class") or "")

    expect(page.locator("#faq-2")).to_have_class(re.compile(r"\bopen\b"))


def test_accordion_toggle_close(page: Page):
    page.get_by_role("button", name="FAQ").click()

    page.locator("#faq-3 .accordion-header").click()
    expect(page.locator("#faq-3")).to_have_class(re.compile(r"\bopen\b"))

    page.locator("#faq-3 .accordion-header").click()
    assert "open" not in (page.locator("#faq-3").get_attribute("class") or "")


def test_edit_notice(page: Page):
    page.locator("#edit-notice-btn").click()

    editor = page.locator("#notice-editor")
    expect(editor).to_be_visible()

    editor.fill("새로운 공지: 다음 주 월요일 배포 예정입니다.")

    page.locator("#save-notice-btn").click()

    expect(page.locator("#notice-text")).to_contain_text("다음 주 월요일 배포 예정")

    expect(editor).to_be_hidden()

    expect(page.locator(".toast.success")).to_be_visible()


def test_api_route_intercept(page: Page):
    mock_body = '{"userId":1,"id":1,"title":"QA 자동화 완료","completed":true}'

    page.route(
        "https://jsonplaceholder.typicode.com/todos/1",
        lambda route: route.fulfill(
            status=200,                        # HTTP 상태코드 200 = 성공
            content_type="application/json",   # 응답 형식: JSON
            body=mock_body,                    # 응답 내용: 가짜 데이터
        ),
    )

    page.get_by_role("button", name="통계").click()
    page.locator("#fetch-api-btn").click()

    result = page.locator("#api-result")

    expect(result).to_be_visible()

    expect(result).to_contain_text("QA 자동화 완료")

    assert result.get_attribute("data-loaded") == "true"


def test_api_route_abort(page: Page):
    page.route(
        "https://jsonplaceholder.typicode.com/todos/1",
        lambda route: route.abort(),
    )

    page.get_by_role("button", name="통계").click()
    page.locator("#fetch-api-btn").click()

    result = page.locator("#api-result")
    expect(result).to_be_visible()

    assert result.get_attribute("data-loaded") == "error"


def test_page_title(page: Page):
    expect(page).to_have_title("Playwright 데모 - 프로젝트 대시보드")


def test_screenshot_overview(page: Page, tmp_path):
    path = tmp_path / "overview.png"

    page.screenshot(path=str(path), full_page=True)

    assert path.exists() and path.stat().st_size > 0


def test_screenshot_per_tab(page: Page, tmp_path):
    for tab in ["개요", "작업 관리", "FAQ", "통계"]:
        page.get_by_role("button", name=tab).click()

        path = tmp_path / f"tab_{tab}.png"
        page.screenshot(path=str(path))
        assert path.exists()


def test_stats_chart_values(page: Page):
    page.get_by_role("button", name="통계").click()

    expect(page.locator("#bar-high-val")).to_have_text("3")
    expect(page.locator("#bar-medium-val")).to_have_text("6")
    expect(page.locator("#bar-low-val")).to_have_text("3")

    expect(page.locator("#completion-rate")).to_have_text("58%")


def test_stat_card_numbers(page: Page):
    checks = [
        ("#stat-num-total",   "12"),   # 전체 작업 수
        ("#stat-num-done",    "7"),    # 완료 수
        ("#stat-num-high",    "3"),    # 긴급 수
        ("#stat-num-members", "5"),    # 팀원 수
    ]

    for selector, expected in checks:
        expect(page.locator(selector)).to_have_text(expected)


if __name__ == "__main__":
    raise SystemExit(pytest.main([__file__, "-v", *sys.argv[1:]]))

