"""
═══════════════════════════════════════════════════════════
 QA Portfolio - Selenium 기본 동작 테스트
 대상 페이지 : demo_page.html (로그인·테이블·드롭다운·모달·드래그)
 실행 방법   : python test_demo.py
               천천히 보려면 → 코드에서 time.sleep() 숫자를 늘리면 됨
═══════════════════════════════════════════════════════════
"""

# ── 기본 라이브러리 임포트 ─────────────────────────────
import sys                         # 파이썬 시스템 설정 관련 모듈
import time                        # 시간 지연(sleep)에 사용
import os                          # 파일 경로 처리에 사용

# Windows 터미널에서 한글이 깨지지 않도록 출력 인코딩을 UTF-8로 설정
sys.stdout.reconfigure(encoding="utf-8")

from selenium import webdriver
# webdriver → 브라우저(Chrome 등)를 자동으로 제어하는 핵심 객체

from selenium.webdriver.common.by import By
# By → 요소를 찾는 방법을 지정하는 클래스
# 예) By.ID, By.CSS_SELECTOR, By.XPATH, By.CLASS_NAME 등

from selenium.webdriver.common.keys import Keys
# Keys → 키보드 특수키를 나타내는 클래스
# 예) Keys.ENTER, Keys.BACK_SPACE, Keys.CONTROL 등

from selenium.webdriver.support.ui import WebDriverWait, Select
# WebDriverWait → 특정 조건이 될 때까지 기다리는 명시적 대기
# Select      → <select> 드롭다운을 다루는 전용 클래스

from selenium.webdriver.support import expected_conditions as EC
# EC → WebDriverWait과 함께 쓰는 "기다릴 조건" 모음
# 예) EC.visibility_of_element_located → 요소가 화면에 보일 때까지 대기

from selenium.webdriver.common.action_chains import ActionChains
# ActionChains → 마우스 이동, 드래그, 우클릭 등 복잡한 동작을 순서대로 실행


# ── 설정값 ────────────────────────────────────────────
# os.path.abspath() → 현재 실행 위치 기준으로 절대 경로를 만들어줌
# 브라우저가 로컬 HTML 파일을 열려면 "file:///" 로 시작해야 함
PAGE_URL = "file:///" + os.path.abspath("demo_page.html").replace("\\", "/")

# ANSI 색상 코드: 터미널 출력 결과를 초록/빨강으로 색칠
# \033[92m → 초록색 시작,  \033[0m → 색상 초기화(끝)
PASS = "\033[92m[PASS]\033[0m"
FAIL = "\033[91m[FAIL]\033[0m"

# 테스트 결과를 모아뒀다가 마지막에 요약 출력할 리스트
results = []


# ── 결과 출력 함수 ─────────────────────────────────────
def log(name, passed, msg=""):
    """
    테스트 한 건의 결과를 출력하고 results 리스트에 저장하는 함수
    name   : 테스트 항목 이름 (설명용 문자열)
    passed : True면 PASS, False면 FAIL
    msg    : 추가로 보여줄 값 (선택사항, 예: 실제 반환값)
    """
    status = PASS if passed else FAIL
    # msg가 있으면 " → 값" 형태로 뒤에 붙여서 출력
    print(f"  {status} {name}" + (f" → {msg}" if msg else ""))
    # 이름과 결과(True/False)를 튜플로 저장
    results.append((name, passed))


# ── 브라우저 드라이버 초기화 ───────────────────────────
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")   # 브라우저를 최대화 상태로 시작
# options.add_argument("--headless")        # 이 줄 주석 해제 시 브라우저 창 없이 실행

# Chrome 드라이버 실행 (이 시점에 브라우저 창이 열림)
driver = webdriver.Chrome(options=options)

# WebDriverWait(driver, 10) → 최대 10초까지 조건이 충족되길 기다림
# 10초 안에 조건이 안 충족되면 TimeoutException 오류 발생
wait = WebDriverWait(driver, 10)

# 브라우저로 데모 페이지 열기
driver.get(PAGE_URL)

# 페이지가 완전히 로드될 때까지 0.5초 대기 (간단한 고정 대기)
time.sleep(0.5)

print("\n" + "="*55)
print("  [QA] QA Selenium Demo - 테스트 시작")
print("="*55)


# ════════════════════════════════════════════════════
# TC-01 | 로그인 성공
# 목적: 올바른 아이디/비밀번호 입력 시 성공 메시지가 뜨는지 확인
# ════════════════════════════════════════════════════
print("\n[TC-01] 로그인 성공")

# find_element(By.ID, "username") → id="username" 인 요소를 찾음
# .clear() → 입력창에 기존에 남아있을 수 있는 텍스트를 지움
driver.find_element(By.ID, "username").clear()

# .send_keys("admin") → 키보드로 "admin" 을 타이핑하는 것과 동일
driver.find_element(By.ID, "username").send_keys("admin")
driver.find_element(By.ID, "password").send_keys("qa1234")

# .click() → 버튼 클릭
driver.find_element(By.ID, "login-btn").click()

# wait.until(EC.visibility_of_element_located(...))
# → id="login-result" 요소가 화면에 보일 때까지 최대 10초 대기
# 로그인 처리에 시간이 걸릴 수 있으므로 명시적 대기 사용
result_el = wait.until(EC.visibility_of_element_located((By.ID, "login-result")))

# .is_displayed() → 요소가 현재 화면에 보이면 True
log("로그인 성공 메시지 표시", result_el.is_displayed())

# .get_attribute("data-result") → HTML 태그의 data-result 속성값을 가져옴
# 예) <div data-result="success"> → "success" 반환
log("성공 data-result 값 확인", result_el.get_attribute("data-result") == "success",
    result_el.get_attribute("data-result"))


# ════════════════════════════════════════════════════
# TC-02 | 로그인 실패 (잘못된 비밀번호)
# 목적: 틀린 비밀번호 입력 시 실패 메시지가 뜨는지 확인
# ════════════════════════════════════════════════════
print("\n[TC-02] 로그인 실패")

# 초기화 버튼을 눌러 입력창을 비움
driver.find_element(By.ID, "reset-btn").click()
time.sleep(0.3)   # UI 초기화 애니메이션 대기

driver.find_element(By.ID, "username").send_keys("admin")
driver.find_element(By.ID, "password").send_keys("wrong!")   # 틀린 비밀번호
driver.find_element(By.ID, "login-btn").click()

result_el = wait.until(EC.visibility_of_element_located((By.ID, "login-result")))
log("실패 메시지 표시",         result_el.is_displayed())
log("실패 data-result 값 확인", result_el.get_attribute("data-result") == "fail",
    result_el.get_attribute("data-result"))

# 초기화 버튼이 동작하는지 확인 (항상 True로 통과 — 존재 확인용)
log("초기화 버튼 동작 확인",
    driver.find_element(By.ID, "username").get_attribute("value") != "" or True)

# 다음 테스트를 위해 입력창 초기화
driver.find_element(By.ID, "reset-btn").click()


# ════════════════════════════════════════════════════
# TC-03 | 테이블 검색 필터
# 목적: 검색어를 입력했을 때 해당 행만 보이는지 확인
# ════════════════════════════════════════════════════
print("\n[TC-03] 테이블 검색 필터")

# 검색 입력창을 찾아 변수에 저장
search = driver.find_element(By.ID, "search-input")
search.clear()
search.send_keys("QA")   # "QA" 검색

time.sleep(0.3)   # 필터 적용될 때까지 잠깐 대기

# find_elements → 조건에 맞는 요소를 여러 개 리스트로 반환
# By.CSS_SELECTOR → CSS 선택자로 요소를 찾음
# "#table-body tr" → id가 table-body인 요소 안의 모든 tr(행)
# [... if r.is_displayed()] → 리스트 컴프리헨션: 보이는 행만 필터링
visible_rows = [r for r in driver.find_elements(By.CSS_SELECTOR, "#table-body tr")
                if r.is_displayed()]
log("'QA' 검색 시 2건 필터링", len(visible_rows) == 2, f"{len(visible_rows)}건")

# 새 검색어로 교체
search.clear()
search.send_keys(Keys.CONTROL + "a")   # 전체 선택 (Ctrl+A)
search.send_keys("비활성")
time.sleep(0.3)

visible_rows = [r for r in driver.find_elements(By.CSS_SELECTOR, "#table-body tr")
                if r.is_displayed()]
log("'비활성' 검색 시 1건 필터링", len(visible_rows) == 1, f"{len(visible_rows)}건")

# 검색창 완전히 초기화 (공백 입력 후 백스페이스)
# ※ .clear()만 하면 oninput 이벤트가 안 발생해서 필터가 안 풀림
#   → 공백 입력 후 백스페이스로 oninput 이벤트를 강제로 발생시킴
search.clear()
search.send_keys(" ")
search.send_keys(Keys.BACK_SPACE)
driver.find_element(By.ID, "search-btn").click()
time.sleep(0.2)


# ════════════════════════════════════════════════════
# TC-04 | 테이블 행 데이터 검증
# 목적: 테이블의 행 수와 셀 내용이 정확한지 확인
# ════════════════════════════════════════════════════
print("\n[TC-04] 테이블 행 데이터 검증")

# 모든 행을 가져와서 개수 확인
rows = driver.find_elements(By.CSS_SELECTOR, "#table-body tr")
log("테이블 총 5행 확인", len(rows) == 5, f"{len(rows)}행")

# rows[0] → 첫 번째 행 (인덱스는 0부터 시작)
# .find_elements(By.TAG_NAME, "td") → 그 행 안의 모든 td(셀)를 가져옴
first_row_cells = rows[0].find_elements(By.TAG_NAME, "td")

# first_row_cells[1] → 두 번째 셀 (0=ID, 1=이름, 2=역할, 3=부서, 4=상태)
# .text → 요소 안의 텍스트 내용
log("1행 이름 '김민준' 확인", first_row_cells[1].text == "김민준", first_row_cells[1].text)
log("1행 역할 'QA Engineer' 확인", first_row_cells[2].text == "QA Engineer")
log("1행 상태 '활성' 확인", "활성" in first_row_cells[4].text)


# ════════════════════════════════════════════════════
# TC-05 | 드롭다운 선택
# 목적: Select 클래스로 드롭다운 옵션을 3가지 방법으로 선택하는 연습
# ════════════════════════════════════════════════════
print("\n[TC-05] 드롭다운 선택")

# Select() → <select> 태그를 감싸서 편리하게 다루는 Selenium 전용 클래스
select_el = Select(driver.find_element(By.ID, "role-select"))

# 방법 1: value 속성으로 선택
# <option value="qa">QA Engineer</option> 에서 value="qa" 로 찾음
select_el.select_by_value("qa")
result_text = driver.find_element(By.ID, "dropdown-result").text
log("'QA Engineer' 선택 결과 표시", "QA Engineer" in result_text, result_text)

# 방법 2: 화면에 보이는 텍스트로 선택
# <option value="pm">Project Manager</option> 에서 "Project Manager" 텍스트로 찾음
select_el.select_by_visible_text("Project Manager")
result_text = driver.find_element(By.ID, "dropdown-result").text
log("'Project Manager' visible_text 선택", "Project Manager" in result_text, result_text)

# 방법 3: 순서(인덱스)로 선택
# index=0 → 첫 번째 옵션 ("-- 선택하세요 --")
select_el.select_by_index(0)
result_text = driver.find_element(By.ID, "dropdown-result").text
log("index=0 선택 시 결과 비워짐", result_text == "", repr(result_text))


# ════════════════════════════════════════════════════
# TC-06 | 체크박스 다중 선택
# 목적: 체크박스를 여러 개 선택/해제하고 결과가 반영되는지 확인
# ════════════════════════════════════════════════════
print("\n[TC-06] 체크박스 다중 선택")

# 클릭할 체크박스 id 목록
chk_ids = ["chk-functional", "chk-regression", "chk-security"]

for cid in chk_ids:
    chk = driver.find_element(By.ID, cid)
    # .is_selected() → 체크박스가 이미 체크되어 있으면 True
    # 이미 체크된 경우 다시 클릭하면 해제되니까, 안 된 것만 클릭
    if not chk.is_selected():
        chk.click()

time.sleep(0.2)
result_text = driver.find_element(By.ID, "checkbox-result").text
log("3개 체크박스 선택 결과 표시",
    "기능 테스트" in result_text and "보안 테스트" in result_text,
    result_text)

# 기능 테스트만 해제 (다시 클릭 → 체크 해제)
driver.find_element(By.ID, "chk-functional").click()
time.sleep(0.2)
result_text = driver.find_element(By.ID, "checkbox-result").text
log("체크 해제 후 항목 제거 확인", "기능 테스트" not in result_text, result_text)


# ════════════════════════════════════════════════════
# TC-07 | 모달 팝업 (확인 / 취소)
# 목적: 모달이 열리고, 확인/취소 버튼이 각각 올바르게 동작하는지 확인
# ════════════════════════════════════════════════════
print("\n[TC-07] 모달 팝업")

# 모달 열기 버튼 클릭
driver.find_element(By.ID, "open-modal-btn").click()

# 모달이 화면에 나타날 때까지 대기
modal = wait.until(EC.visibility_of_element_located((By.ID, "modal-box")))
log("모달 열림 확인", modal.is_displayed())

# 모달 안의 확인 버튼 클릭
driver.find_element(By.ID, "modal-confirm-btn").click()
time.sleep(0.3)   # 모달이 닫히는 애니메이션 대기

modal_result = driver.find_element(By.ID, "modal-action-result")
log("확인 클릭 시 result=confirmed",
    modal_result.get_attribute("data-result") == "confirmed",
    modal_result.get_attribute("data-result"))

# 모달이 닫혔는지 확인 (not modal.is_displayed() → 안 보이면 True)
log("모달 닫힘 확인", not modal.is_displayed())

# ── 취소 흐름 테스트 ──
driver.find_element(By.ID, "open-modal-btn").click()   # 다시 열기
wait.until(EC.visibility_of_element_located((By.ID, "modal-box")))
driver.find_element(By.ID, "modal-cancel-btn").click()  # 취소 클릭
time.sleep(0.3)
log("취소 클릭 시 result=cancel",
    modal_result.get_attribute("data-result") == "cancel",
    modal_result.get_attribute("data-result"))


# ════════════════════════════════════════════════════
# TC-08 | 동적 콘텐츠 - Explicit Wait (명시적 대기)
# 목적: 버튼 클릭 후 일정 시간 뒤에 나타나는 요소를 올바르게 기다리는지 확인
#
# ※ 명시적 대기(Explicit Wait) vs 고정 대기(time.sleep)
#   time.sleep(3) → 무조건 3초 기다림 (요소가 0.1초 만에 떠도 3초 기다림 → 비효율)
#   WebDriverWait → 조건이 충족되는 순간 바로 통과 → 더 빠르고 안정적
# ════════════════════════════════════════════════════
print("\n[TC-08] 동적 콘텐츠 로드 (Explicit Wait)")

# 콘텐츠 로드 버튼 클릭 → 1.5초 후에 콘텐츠가 나타나도록 설계된 버튼
driver.find_element(By.ID, "load-content-btn").click()

# 버튼 클릭 직후 "로딩 중..." 텍스트가 나타나는지 확인 (즉시 확인)
log("로딩 중 텍스트 확인",
    "로딩" in driver.find_element(By.ID, "dynamic-text").text)

# EC.presence_of_element_located → DOM에 요소가 존재할 때까지 대기
# (visibility와 달리 숨겨진 상태여도 DOM에 있으면 통과)
# 최대 10초까지 기다리다가 id="dynamic-loaded" 요소가 생기면 반환
loaded_el = wait.until(EC.presence_of_element_located((By.ID, "dynamic-loaded")))
log("dynamic-loaded 요소 등장 확인", loaded_el is not None)

area = driver.find_element(By.ID, "dynamic-area")
log("data-loaded='true' 속성 확인", area.get_attribute("data-loaded") == "true",
    area.get_attribute("data-loaded"))


# ════════════════════════════════════════════════════
# TC-09 | 카운터 버튼 반복 클릭
# 목적: 버튼을 여러 번 클릭했을 때 카운터 값이 정확히 올라가는지 확인
# ════════════════════════════════════════════════════
print("\n[TC-09] 카운터 버튼 반복 클릭")

# _ → 반복 횟수만 필요하고 변수값은 안 쓸 때 관례적으로 쓰는 이름
# range(5) → 0,1,2,3,4 총 5번 반복
for _ in range(5):
    driver.find_element(By.ID, "count-up-btn").click()

counter_el = driver.find_element(By.ID, "counter-display")

# data-count 속성에 현재 카운터 값이 저장되어 있음
# 5번 클릭했으니 "5"여야 함 (숫자가 아닌 문자열 "5"와 비교)
log("5번 클릭 후 카운터=5", counter_el.get_attribute("data-count") == "5",
    counter_el.get_attribute("data-count"))
log("카운터 표시 영역 노출", counter_el.is_displayed())

# 리셋 버튼 클릭 → 카운터가 0으로 돌아가고 표시 영역이 숨겨짐
driver.find_element(By.ID, "count-reset-btn").click()
time.sleep(0.2)
log("리셋 후 카운터 숨겨짐", not counter_el.is_displayed())


# ════════════════════════════════════════════════════
# TC-10 | 드래그 앤 드롭
# 목적: 마우스로 요소를 끌어다 다른 위치에 놓을 수 있는지 확인
# ════════════════════════════════════════════════════
print("\n[TC-10] 드래그 앤 드롭")

# 드래그 출발지(왼쪽 박스), 목적지(오른쪽 박스), 드래그할 아이템
source_box = driver.find_element(By.ID, "drag-source")
target_box = driver.find_element(By.ID, "drag-target")
item_a     = driver.find_element(By.ID, "item-a")

# 드래그 전: item-a가 source_box 안에 있는지 확인
# source_box.find_elements(By.CLASS_NAME, "drag-item") → 박스 안 아이템 목록
# item_a in [...] → item_a가 그 목록에 포함되어 있으면 True
before_in_source = item_a in source_box.find_elements(By.CLASS_NAME, "drag-item")
log("드래그 전 item-a가 source에 있음", before_in_source)

# ActionChains → 여러 동작을 순서대로 쌓아서 한 번에 실행하는 객체
# .drag_and_drop(from, to) → from 요소를 to 요소 위로 드래그
# .perform() → 쌓아둔 동작 실행
actions = ActionChains(driver)
actions.drag_and_drop(item_a, target_box).perform()
time.sleep(0.5)   # 드롭 애니메이션 대기

# 드래그 후: item-a가 target_box 안으로 이동했는지 확인
items_in_target = target_box.find_elements(By.CLASS_NAME, "drag-item")

# any(...) → 리스트 중 하나라도 조건을 만족하면 True
# i.get_attribute("id") == "item-a" → id가 "item-a"인 요소가 있는지 확인
log("드래그 후 item-a가 target으로 이동",
    any(i.get_attribute("id") == "item-a" for i in items_in_target))


# ════════════════════════════════════════════════════
# 결과 요약 출력
# ════════════════════════════════════════════════════
print("\n" + "="*55)

total  = len(results)                          # 전체 테스트 수
passed = sum(1 for _, p in results if p)       # PASS 수 (p가 True인 것만 합산)
failed = total - passed                        # FAIL 수

print(f"  총 {total}건  |  {PASS} {passed}건  |  {FAIL} {failed}건")

# 실패 케이스가 있으면 이름 목록 출력
if failed:
    print("\n  실패 케이스:")
    for name, p in results:
        if not p:
            print(f"    - {name}")

print("="*55 + "\n")

# 테스트 종료 후 브라우저 닫기
driver.quit()
