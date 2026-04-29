import pytest
from pathlib import Path
from playwright.sync_api import Page, sync_playwright

try:
    import allure
except ModuleNotFoundError:
    allure = None

PAGE_URL = "file:///" + str(Path(__file__).parent / "demo_page.html").replace("\\", "/")


def pytest_addoption(parser):
    parser.addoption("--headed", action="store_true", help="브라우저 창을 띄워서 실행")
    parser.addoption("--slowmo", action="store", type=int, default=0, help="동작 사이 지연(ms)")


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()

    if allure and rep.when == "call" and rep.failed:
        page: Page = item.funcargs.get("page")
        if page:
            allure.attach(
                page.screenshot(full_page=True),
                name=f"FAIL_{item.name}",
                attachment_type=allure.attachment_type.PNG,
            )


@pytest.fixture(scope="session")
def browser(request):
    """Chromium은 한 번만 띄워서 테스트 실행 속도를 안정화한다."""
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

@pytest.fixture()
def overview_page(page: Page):
    """개요 탭이 활성화된 OverviewPage 반환"""
    from pages.overview_page import OverviewPage
    return OverviewPage(page)


@pytest.fixture()
def task_page(page: Page):
    """작업 관리 탭으로 이동한 TaskPage 반환"""
    from pages.task_page import TaskPage
    p = TaskPage(page)
    p.go_to_tab()
    return p


@pytest.fixture()
def faq_page(page: Page):
    """FAQ 탭으로 이동한 FAQPage 반환"""
    from pages.faq_page import FAQPage
    p = FAQPage(page)
    p.go_to_tab()
    return p


@pytest.fixture()
def stats_page(page: Page):
    """통계 탭으로 이동한 StatsPage 반환"""
    from pages.stats_page import StatsPage
    p = StatsPage(page)
    p.go_to_tab()
    return p

