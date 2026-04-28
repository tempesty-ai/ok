"""
═══════════════════════════════════════════════════════════
 QA Portfolio - Playwright 기본 동작 테스트
 대상 페이지 : demo_page.html (프로젝트 대시보드)
 실행 방법   : pytest test_demo.py -v
               pytest test_demo.py -v --headed          ← 브라우저 눈으로 보기
               pytest test_demo.py -v --headed --slowmo=800  ← 천천히 보기
═══════════════════════════════════════════════════════════
"""

# ── 기본 라이브러리 임포트 ─────────────────────────────
import re                          # 정규표현식 (텍스트 패턴 비교에 사용)
import pytest                      # 파이썬 테스트 프레임워크
from pathlib import Path           # 파일 경로를 다루는 모듈
from playwright.sync_api import Page, expect
# Page   : 브라우저 탭 한 장을 나타내는 객체
# expect : "이 요소가 ~이어야 한다"는 검증(단언)을 해주는 함수


# ── 테스트 대상 페이지 경로 설정 ───────────────────────
# __file__  → 현재 이 파이썬 파일의 경로
# .parent   → 파일이 있는 폴더
# / "demo_page.html" → 같은 폴더 안의 HTML 파일
# 브라우저가 로컬 파일을 열려면 "file:///" 로 시작해야 함
PAGE_URL = "file:///" + str(Path(__file__).parent / "demo_page.html").replace("\\", "/")


# ── fixture: 각 테스트 시작 전 공통으로 실행되는 준비 코드 ─
# @pytest.fixture() 를 붙이면 pytest가 테스트 함수마다
# 자동으로 이 함수를 먼저 실행해서 준비해줌
# → 매번 테스트할 때마다 새 브라우저 탭에서 페이지를 열어줌
@pytest.fixture()
def page(page: Page):
    page.goto(PAGE_URL)   # 브라우저로 데모 페이지 열기
    return page           # 준비된 page 객체를 테스트 함수에 전달


# ════════════════════════════════════════════════════
# TC-01 | 탭 전환
# 목적: 탭 버튼을 클릭하면 해당 화면만 보이는지 확인
# ════════════════════════════════════════════════════
def test_tab_switch_click(page: Page):
    # '작업 관리' 버튼을 role(역할) 기반으로 찾아 클릭
    # get_by_role("button", name="작업 관리") 은
    # HTML에서 <button>태그 중 텍스트가 "작업 관리"인 것을 찾는다
    page.get_by_role("button", name="작업 관리").click()

    # locator("#panel-tasks") → id가 panel-tasks인 요소를 찾음 (CSS 선택자)
    # to_be_visible() → 화면에 보여야 함
    expect(page.locator("#panel-tasks")).to_be_visible()

    # 나머지 탭 패널은 숨겨져 있어야 함
    # to_be_hidden() → 화면에 안 보여야 함
    expect(page.locator("#panel-overview")).to_be_hidden()


def test_tab_switch_all(page: Page):
    # 탭 이름 목록과 대응되는 패널 id 목록을 나란히 정의
    tabs   = ["작업 관리", "FAQ", "통계", "개요"]
    panels = ["panel-tasks", "panel-faq", "panel-stats", "panel-overview"]

    # zip() : 두 리스트를 쌍으로 묶어서 함께 반복
    # 예) ("작업 관리", "panel-tasks") → ("FAQ", "panel-faq") → ...
    for name, panel_id in zip(tabs, panels):
        page.get_by_role("button", name=name).click()           # 탭 클릭
        expect(page.locator(f"#{panel_id}")).to_be_visible()    # 해당 패널 표시 확인


# ════════════════════════════════════════════════════
# TC-02 | 호버 툴팁
# 목적: 마우스를 올렸을 때 툴팁(말풍선)이 나타나는지 확인
# ════════════════════════════════════════════════════
def test_hover_tooltip(page: Page):
    # id가 stat-total 인 통계 카드 전체를 가져옴
    card    = page.locator("#stat-total")
    # 카드 안에 있는 .tooltip 클래스 요소를 가져옴
    tooltip = card.locator(".tooltip")

    # 마우스를 올리기 전에는 툴팁이 숨겨져 있어야 함
    expect(tooltip).to_be_hidden()

    # .hover() → 마우스 커서를 해당 요소 위로 이동 (클릭 아님)
    card.hover()

    # 마우스를 올린 후에는 툴팁이 보여야 함
    expect(tooltip).to_be_visible()

    # 툴팁 텍스트 내용도 확인
    # to_contain_text() → 해당 텍스트가 포함되어 있으면 통과
    expect(tooltip).to_contain_text("전체 등록 작업 수")


def test_hover_tooltip_all_cards(page: Page):
    # 딕셔너리(사전): { 카드 선택자 : 기대하는 툴팁 텍스트 } 형태로 정리
    expected = {
        "#stat-total":   "전체 등록 작업 수",
        "#stat-done":    "완료 처리된 작업",
        "#stat-high":    "우선순위 높음 작업",
        "#stat-members": "프로젝트 참여 인원",
    }

    # .items() → 딕셔너리를 (키, 값) 쌍으로 반복
    for selector, text in expected.items():
        page.locator(selector).hover()                                    # 마우스 올리기
        expect(page.locator(selector).locator(".tooltip")).to_contain_text(text)  # 툴팁 검증


# ════════════════════════════════════════════════════
# TC-03 | 작업 추가
# 목적: 작업을 버튼 / Enter 키로 추가하고, 빈값일 때 에러가 나는지 확인
# ════════════════════════════════════════════════════
def test_add_task_via_button(page: Page):
    # 먼저 '작업 관리' 탭으로 이동
    page.get_by_role("button", name="작업 관리").click()

    # .fill() → 입력창에 텍스트를 입력 (기존 내용 지우고 새로 씀)
    page.locator("#task-input").fill("로그인 회귀 테스트")

    # 추가 버튼 클릭
    page.locator("#add-task-btn").click()

    # 작업 목록 아이템 전체를 가져옴
    item = page.locator("#task-list .task-item")

    # to_have_count(1) → 목록에 아이템이 정확히 1개여야 함
    expect(item).to_have_count(1)

    # 아이템 안의 .task-text 에 입력한 텍스트가 들어있는지 확인
    expect(item.locator(".task-text")).to_contain_text("로그인 회귀 테스트")


def test_add_task_via_enter_key(page: Page):
    page.get_by_role("button", name="작업 관리").click()
    page.locator("#task-input").fill("성능 테스트 계획 수립")

    # keyboard.press("Enter") → 키보드 Enter 키를 누름
    # 마우스 없이 키보드만으로 동작하는지 테스트
    page.keyboard.press("Enter")

    # 아이템이 1개 추가됐는지만 확인
    expect(page.locator("#task-list .task-item")).to_have_count(1)


def test_add_task_empty_shows_toast(page: Page):
    # 아무것도 입력하지 않고 추가 버튼 클릭
    page.get_by_role("button", name="작업 관리").click()
    page.locator("#add-task-btn").click()

    # 에러 토스트(알림 메시지)가 나타나야 함
    # .toast.error → class가 "toast"이면서 "error"인 요소
    toast = page.locator(".toast.error")
    expect(toast).to_be_visible()
    expect(toast).to_contain_text("작업 내용을 입력해주세요")


# ════════════════════════════════════════════════════
# TC-04 | 작업 완료 체크 & 진행률 바
# 목적: 체크박스를 누르면 취소선이 생기고 진행률이 올라가는지 확인
# ════════════════════════════════════════════════════
def test_task_complete_and_progress(page: Page):
    page.get_by_role("button", name="작업 관리").click()
    page.locator("#task-input").fill("API 테스트 케이스 작성")
    page.keyboard.press("Enter")

    # CSS 선택자로 체크박스를 찾아 체크 (✓ 표시)
    # input[type=checkbox] → type 속성이 checkbox인 input 태그
    page.locator("#task-list .task-item input[type=checkbox]").check()

    # 완료된 항목에는 .done 클래스가 붙어 취소선이 생김
    expect(page.locator(".task-text.done")).to_be_visible()

    # 진행률 텍스트가 100%인지 확인
    # to_have_text() → 요소의 텍스트가 정확히 일치해야 함
    expect(page.locator("#progress-pct")).to_have_text("100%")

    # style 속성에 "width: 100%" 가 들어있는지 정규표현식으로 확인
    # re.compile() → 정규표현식 패턴 생성
    # r"width:\s*100%" → "width:" 뒤에 공백이 0개 이상 있고 "100%"인 패턴
    expect(page.locator("#progress-fill")).to_have_attribute("style", re.compile(r"width:\s*100%"))


def test_progress_partial(page: Page):
    page.get_by_role("button", name="작업 관리").click()

    # 3개 작업을 반복문으로 빠르게 추가
    for text in ["작업 A", "작업 B", "작업 C"]:
        page.locator("#task-input").fill(text)
        page.keyboard.press("Enter")

    # .first → 목록에서 첫 번째 요소만 가져옴
    # 첫 번째 작업만 체크 → 3개 중 1개 완료 = 33%
    page.locator("#task-list .task-item").first.locator("input[type=checkbox]").check()

    expect(page.locator("#progress-pct")).to_have_text("33%")


# ════════════════════════════════════════════════════
# TC-05 | 우선순위 필터
# 목적: 필터 버튼을 누르면 해당 우선순위 작업만 보이는지 확인
# ════════════════════════════════════════════════════
def test_priority_filter(page: Page):
    page.get_by_role("button", name="작업 관리").click()

    # 드롭다운에서 "high" 값을 선택
    # select_option() → <select> 태그의 옵션을 선택하는 함수
    page.locator("#priority-select").select_option("high")
    page.locator("#task-input").fill("긴급 버그 수정")
    page.keyboard.press("Enter")   # 높음 우선순위로 작업 추가

    page.locator("#priority-select").select_option("low")
    page.locator("#task-input").fill("문서 정리")
    page.keyboard.press("Enter")   # 낮음 우선순위로 작업 추가

    # data-filter='high' 속성을 가진 필터 버튼 클릭
    # CSS 속성 선택자: [속성명='값'] 형태로 찾음
    page.locator(".filter-btn[data-filter='high']").click()

    items = page.locator("#task-list .task-item")
    # '높음' 필터를 선택했으니 1개만 보여야 함
    expect(items).to_have_count(1)
    # 보이는 항목의 태그가 "높음" 이어야 함
    expect(items.locator(".priority-tag")).to_contain_text("높음")


def test_filter_done(page: Page):
    page.get_by_role("button", name="작업 관리").click()

    # 2개 작업 추가
    for text in ["완료 작업", "미완료 작업"]:
        page.locator("#task-input").fill(text)
        page.keyboard.press("Enter")

    # 첫 번째 작업만 완료 처리
    page.locator("#task-list .task-item").first.locator("input[type=checkbox]").check()

    # '완료됨' 필터 클릭
    page.locator(".filter-btn[data-filter='done']").click()

    # 완료된 1개만 표시되어야 함
    expect(page.locator("#task-list .task-item")).to_have_count(1)
    # 표시된 항목에 취소선(.done)이 적용되어 있어야 함
    expect(page.locator(".task-text.done")).to_be_visible()


# ════════════════════════════════════════════════════
# TC-06 | 작업 삭제
# 목적: 삭제 버튼을 누르면 작업이 사라지고 빈 메시지가 뜨는지 확인
# ════════════════════════════════════════════════════
def test_delete_task(page: Page):
    page.get_by_role("button", name="작업 관리").click()
    page.locator("#task-input").fill("삭제할 작업")
    page.keyboard.press("Enter")

    # 삭제 전 1개 있는지 확인
    expect(page.locator("#task-list .task-item")).to_have_count(1)

    # 삭제 버튼(✕) 클릭
    page.locator(".del-btn").click()

    # 삭제 후 0개인지 확인
    expect(page.locator("#task-list .task-item")).to_have_count(0)

    # 목록이 비었을 때 "등록된 작업이 없습니다" 문구가 보여야 함
    expect(page.locator("#empty-msg")).to_be_visible()


def test_delete_shows_toast(page: Page):
    page.get_by_role("button", name="작업 관리").click()
    page.locator("#task-input").fill("삭제 토스트 확인용")
    page.keyboard.press("Enter")
    page.locator(".del-btn").click()

    # 삭제 후 파란색(info) 토스트 알림이 뜨는지 확인
    expect(page.locator(".toast.info")).to_be_visible()


# ════════════════════════════════════════════════════
# TC-07 | 아코디언 FAQ 열기 / 닫기
# 목적: 클릭으로 열고 닫히는지, 하나만 열리는지 확인
#
# ※ 주의: 이 아코디언은 CSS max-height 방식으로 열고 닫힘
#   → display:none 이 아니어서 to_be_hidden() 으로 못 잡음
#   → 대신 .open 클래스가 붙었는지/안 붙었는지로 상태 판단
# ════════════════════════════════════════════════════
def test_accordion_open(page: Page):
    page.get_by_role("button", name="FAQ").click()

    # id가 faq-1인 아코디언 항목 전체를 가져옴
    item = page.locator("#faq-1")

    # 클릭 전: .open 클래스가 없어야 함
    # get_attribute("class") → 요소의 class 속성값을 문자열로 반환
    # "open" not in ... → "open"이라는 문자열이 없어야 통과
    assert "open" not in (item.get_attribute("class") or "")

    # 헤더 클릭 → 아코디언 열기
    item.locator(".accordion-header").click()

    # 클릭 후: .open 클래스가 붙어야 함
    # re.compile(r"\bopen\b") → 단어 경계(\b)로 정확히 "open" 단어만 매칭
    # (예: "reopen" 같은 단어는 매칭 안 됨)
    expect(item).to_have_class(re.compile(r"\bopen\b"))

    # 펼쳐진 내용에 "Microsoft" 텍스트가 있는지도 확인
    expect(item.locator(".accordion-body-inner")).to_contain_text("Microsoft")


def test_accordion_exclusive(page: Page):
    # faq-1을 먼저 열고
    page.get_by_role("button", name="FAQ").click()
    page.locator("#faq-1 .accordion-header").click()

    # faq-2를 클릭하면 faq-1은 자동으로 닫혀야 함
    page.locator("#faq-2 .accordion-header").click()

    # faq-1 → 닫힘 확인 (.open 클래스 없음)
    assert "open" not in (page.locator("#faq-1").get_attribute("class") or "")

    # faq-2 → 열림 확인 (.open 클래스 있음)
    expect(page.locator("#faq-2")).to_have_class(re.compile(r"\bopen\b"))


def test_accordion_toggle_close(page: Page):
    page.get_by_role("button", name="FAQ").click()

    # 한 번 클릭 → 열림
    page.locator("#faq-3 .accordion-header").click()
    expect(page.locator("#faq-3")).to_have_class(re.compile(r"\bopen\b"))

    # 같은 곳 다시 클릭 → 닫힘
    page.locator("#faq-3 .accordion-header").click()
    assert "open" not in (page.locator("#faq-3").get_attribute("class") or "")


# ════════════════════════════════════════════════════
# TC-08 | 공지 인라인 수정
# 목적: 수정 버튼 → 입력창 열림 → 저장 → 내용 반영되는지 확인
# ════════════════════════════════════════════════════
def test_edit_notice(page: Page):
    # 공지 수정 버튼 클릭
    page.locator("#edit-notice-btn").click()

    # textarea 입력창이 나타나는지 확인
    editor = page.locator("#notice-editor")
    expect(editor).to_be_visible()

    # 새 공지 내용 입력 (.fill은 기존 내용을 지우고 새로 씀)
    editor.fill("새로운 공지: 다음 주 월요일 배포 예정입니다.")

    # 저장 버튼 클릭
    page.locator("#save-notice-btn").click()

    # 저장 후: 공지 텍스트에 새 내용이 반영되어야 함
    expect(page.locator("#notice-text")).to_contain_text("다음 주 월요일 배포 예정")

    # 저장 후: 입력창은 다시 숨겨져야 함
    expect(editor).to_be_hidden()

    # 저장 성공 토스트가 뜨는지 확인
    expect(page.locator(".toast.success")).to_be_visible()


# ════════════════════════════════════════════════════
# TC-09 | 네트워크 인터셉트 (route)
# 목적: API 요청을 가로채서 가짜 응답을 주거나 막을 수 있는지 확인
#
# ※ Playwright의 강력한 기능 중 하나!
#   실제 서버 없이도 "서버가 이렇게 응답했을 때" 를 테스트 가능
#   Selenium에는 없는 기능
# ════════════════════════════════════════════════════
def test_api_route_intercept(page: Page):
    # 가로챌 때 돌려줄 가짜(Mock) JSON 데이터
    mock_body = '{"userId":1,"id":1,"title":"QA 자동화 완료","completed":true}'

    # page.route(URL, 처리함수) → 해당 URL 요청을 가로챔
    # lambda route → 요청이 왔을 때 실행할 익명 함수
    # route.fulfill() → 실제 서버 대신 지정한 내용으로 응답
    page.route(
        "https://jsonplaceholder.typicode.com/todos/1",
        lambda route: route.fulfill(
            status=200,                        # HTTP 상태코드 200 = 성공
            content_type="application/json",   # 응답 형식: JSON
            body=mock_body,                    # 응답 내용: 가짜 데이터
        ),
    )

    # 통계 탭으로 이동 후 API 호출 버튼 클릭
    page.get_by_role("button", name="통계").click()
    page.locator("#fetch-api-btn").click()

    result = page.locator("#api-result")

    # 결과 영역이 보여야 함
    expect(result).to_be_visible()

    # 가짜 응답에 넣은 title이 화면에 표시되는지 확인
    expect(result).to_contain_text("QA 자동화 완료")

    # data-loaded 속성이 "true"인지 확인
    # get_attribute() → HTML 요소의 특정 속성값을 문자열로 가져옴
    assert result.get_attribute("data-loaded") == "true"


def test_api_route_abort(page: Page):
    # route.abort() → 요청을 아예 차단 (네트워크 오류 발생시킴)
    # 네트워크 오류 상황에서 UI가 올바르게 처리하는지 테스트
    page.route(
        "https://jsonplaceholder.typicode.com/todos/1",
        lambda route: route.abort(),
    )

    page.get_by_role("button", name="통계").click()
    page.locator("#fetch-api-btn").click()

    result = page.locator("#api-result")
    expect(result).to_be_visible()

    # 오류 상황이므로 data-loaded 속성이 "error"여야 함
    assert result.get_attribute("data-loaded") == "error"


# ════════════════════════════════════════════════════
# TC-10 | 스크린샷 & 페이지 제목
# 목적: 페이지 타이틀 확인 및 자동으로 스크린샷 찍기
# ════════════════════════════════════════════════════
def test_page_title(page: Page):
    # 브라우저 탭에 표시되는 페이지 제목이 맞는지 확인
    # to_have_title() → <title> 태그 내용과 비교
    expect(page).to_have_title("Playwright 데모 - 프로젝트 대시보드")


def test_screenshot_overview(page: Page, tmp_path):
    # tmp_path → pytest가 자동으로 만들어주는 임시 폴더 경로
    path = tmp_path / "overview.png"

    # page.screenshot() → 현재 브라우저 화면을 이미지로 저장
    # full_page=True → 스크롤 내려야 보이는 부분까지 전체 캡처
    page.screenshot(path=str(path), full_page=True)

    # 파일이 실제로 생성됐는지, 내용이 비어있지 않은지 확인
    assert path.exists() and path.stat().st_size > 0


def test_screenshot_per_tab(page: Page, tmp_path):
    # 탭 4개를 순서대로 클릭하면서 각각 스크린샷 저장
    for tab in ["개요", "작업 관리", "FAQ", "통계"]:
        page.get_by_role("button", name=tab).click()

        # f-string: f"tab_{tab}.png" → "tab_개요.png", "tab_작업 관리.png" 등
        path = tmp_path / f"tab_{tab}.png"
        page.screenshot(path=str(path))
        assert path.exists()


# ════════════════════════════════════════════════════
# TC-11 | 통계 차트 데이터 검증
# 목적: 통계 탭의 숫자 데이터가 올바른지 확인
# ════════════════════════════════════════════════════
def test_stats_chart_values(page: Page):
    page.get_by_role("button", name="통계").click()

    # 막대 차트 각 항목의 숫자가 맞는지 확인
    # to_have_text() → 요소 텍스트가 정확히 해당 값이어야 통과
    expect(page.locator("#bar-high-val")).to_have_text("3")
    expect(page.locator("#bar-medium-val")).to_have_text("6")
    expect(page.locator("#bar-low-val")).to_have_text("3")

    # 완료율 텍스트 확인
    expect(page.locator("#completion-rate")).to_have_text("58%")


def test_stat_card_numbers(page: Page):
    # 검증할 (선택자, 기대값) 쌍을 리스트로 정리
    # 이렇게 하면 항목이 늘어도 코드 구조는 그대로 유지됨
    checks = [
        ("#stat-num-total",   "12"),   # 전체 작업 수
        ("#stat-num-done",    "7"),    # 완료 수
        ("#stat-num-high",    "3"),    # 긴급 수
        ("#stat-num-members", "5"),    # 팀원 수
    ]

    # 리스트를 반복하며 각 숫자를 한 번에 검증
    for selector, expected in checks:
        expect(page.locator(selector)).to_have_text(expected)
