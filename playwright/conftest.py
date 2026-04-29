import pytest
import allure
from pathlib import Path
from playwright.sync_api import Page

PAGE_URL = "file:///" + str(Path(__file__).parent / "demo_page.html").replace("\\", "/")


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield                  # 테스트 실행
    rep = outcome.get_result()       # 실행 결과 가져오기

    if rep.when == "call" and rep.failed:
        page: Page = item.funcargs.get("page")
        if page:
            allure.attach(
                page.screenshot(full_page=True),
                name=f"FAIL_{item.name}",
                attachment_type=allure.attachment_type.PNG,
            )


@pytest.fixture()
def page(page: Page):
    page.goto(PAGE_URL)
    return page



from pages.overview_page import OverviewPage
from pages.task_page import TaskPage
from pages.faq_page import FAQPage
from pages.stats_page import StatsPage


@pytest.fixture()
def overview_page(page: Page) -> OverviewPage:
    """개요 탭이 활성화된 OverviewPage 반환"""
    return OverviewPage(page)


@pytest.fixture()
def task_page(page: Page) -> TaskPage:
    """작업 관리 탭으로 이동한 TaskPage 반환"""
    p = TaskPage(page)
    p.go_to_tab()
    return p


@pytest.fixture()
def faq_page(page: Page) -> FAQPage:
    """FAQ 탭으로 이동한 FAQPage 반환"""
    p = FAQPage(page)
    p.go_to_tab()
    return p


@pytest.fixture()
def stats_page(page: Page) -> StatsPage:
    """통계 탭으로 이동한 StatsPage 반환"""
    p = StatsPage(page)
    p.go_to_tab()
    return p

