"""
conftest.py
pytest가 자동으로 읽는 설정 파일.
- 공통 fixture 정의
- 실패 시 자동 스크린샷 → Allure 리포트에 첨부
- 페이지 오브젝트 fixture 제공
"""

import pytest
import allure
from pathlib import Path
from playwright.sync_api import Page

# 테스트 대상 HTML 파일 경로 (로컬 파일)
PAGE_URL = "file:///" + str(Path(__file__).parent / "demo_page.html").replace("\\", "/")


# ── 실패 시 자동 스크린샷 ──────────────────────────────────────────
# pytest_runtest_makereport: 테스트가 끝날 때마다 자동으로 호출되는 훅
# tryfirst=True  → 다른 훅보다 먼저 실행
# hookwrapper=True → yield 전/후로 처리 가능
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield                  # 테스트 실행
    rep = outcome.get_result()       # 실행 결과 가져오기

    # 테스트 본문(call) 단계에서 실패했을 때만 스크린샷
    if rep.when == "call" and rep.failed:
        # item.funcargs: 해당 테스트에 주입된 fixture들
        page: Page = item.funcargs.get("page")
        if page:
            # allure.attach → Allure 리포트에 파일 첨부
            allure.attach(
                page.screenshot(full_page=True),
                name=f"FAIL_{item.name}",
                attachment_type=allure.attachment_type.PNG,
            )


# ── 기본 page fixture ─────────────────────────────────────────────
# tests/ 폴더의 모든 테스트 함수가 "page" 인자를 받으면 이게 실행됨
@pytest.fixture()
def page(page: Page):
    page.goto(PAGE_URL)
    return page


# ── POM fixture ───────────────────────────────────────────────────
# 각 테스트에서 페이지 오브젝트를 바로 받아 쓸 수 있도록 fixture로 등록
# 테스트 함수 인자 이름이 "task_page" 면 아래 fixture가 자동 주입됨

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
