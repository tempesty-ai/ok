import sys                         # 파이썬 시스템 설정 관련 모듈
import time                        # 시간 지연(sleep)에 사용
import os                          # 파일 경로 처리에 사용

sys.stdout.reconfigure(encoding="utf-8")

from selenium import webdriver

from selenium.webdriver.common.by import By

from selenium.webdriver.common.keys import Keys

from selenium.webdriver.support.ui import WebDriverWait, Select

from selenium.webdriver.support import expected_conditions as EC

from selenium.webdriver.common.action_chains import ActionChains


PAGE_URL = "file:///" + os.path.abspath("demo_page.html").replace("\\", "/")

PASS = "\033[92m[PASS]\033[0m"
FAIL = "\033[91m[FAIL]\033[0m"

results = []


def log(name, passed, msg=""):
    """
    테스트 한 건의 결과를 출력하고 results 리스트에 저장하는 함수
    name   : 테스트 항목 이름 (설명용 문자열)
    passed : True면 PASS, False면 FAIL
    msg    : 추가로 보여줄 값 (선택사항, 예: 실제 반환값)
    """
    status = PASS if passed else FAIL
    print(f"  {status} {name}" + (f" → {msg}" if msg else ""))
    results.append((name, passed))


options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")   # 브라우저를 최대화 상태로 시작

driver = webdriver.Chrome(options=options)

wait = WebDriverWait(driver, 10)

driver.get(PAGE_URL)

time.sleep(0.5)

print("\n" + "="*55)
print("  [QA] QA Selenium Demo - 테스트 시작")
print("="*55)


print("\n[TC-01] 로그인 성공")

driver.find_element(By.ID, "username").clear()

driver.find_element(By.ID, "username").send_keys("admin")
driver.find_element(By.ID, "password").send_keys("qa1234")

driver.find_element(By.ID, "login-btn").click()

result_el = wait.until(EC.visibility_of_element_located((By.ID, "login-result")))

log("로그인 성공 메시지 표시", result_el.is_displayed())

log("성공 data-result 값 확인", result_el.get_attribute("data-result") == "success",
    result_el.get_attribute("data-result"))


print("\n[TC-02] 로그인 실패")

driver.find_element(By.ID, "reset-btn").click()
time.sleep(0.3)   # UI 초기화 애니메이션 대기

driver.find_element(By.ID, "username").send_keys("admin")
driver.find_element(By.ID, "password").send_keys("wrong!")   # 틀린 비밀번호
driver.find_element(By.ID, "login-btn").click()

result_el = wait.until(EC.visibility_of_element_located((By.ID, "login-result")))
log("실패 메시지 표시",         result_el.is_displayed())
log("실패 data-result 값 확인", result_el.get_attribute("data-result") == "fail",
    result_el.get_attribute("data-result"))

driver.find_element(By.ID, "reset-btn").click()
time.sleep(0.2)
log("초기화 버튼 동작 확인",
    driver.find_element(By.ID, "username").get_attribute("value") == ""
    and driver.find_element(By.ID, "password").get_attribute("value") == ""
    and not driver.find_element(By.ID, "login-result").is_displayed())


print("\n[TC-03] 테이블 검색 필터")

search = driver.find_element(By.ID, "search-input")
search.clear()
search.send_keys("QA")   # "QA" 검색

time.sleep(0.3)   # 필터 적용될 때까지 잠깐 대기

visible_rows = [r for r in driver.find_elements(By.CSS_SELECTOR, "#table-body tr")
                if r.is_displayed()]
log("'QA' 검색 시 2건 필터링", len(visible_rows) == 2, f"{len(visible_rows)}건")

search.clear()
search.send_keys(Keys.CONTROL + "a")   # 전체 선택 (Ctrl+A)
search.send_keys("비활성")
time.sleep(0.3)

visible_rows = [r for r in driver.find_elements(By.CSS_SELECTOR, "#table-body tr")
                if r.is_displayed()]
log("'비활성' 검색 시 1건 필터링", len(visible_rows) == 1, f"{len(visible_rows)}건")

search.clear()
search.send_keys(" ")
search.send_keys(Keys.BACK_SPACE)
driver.find_element(By.ID, "search-btn").click()
time.sleep(0.2)


print("\n[TC-04] 테이블 행 데이터 검증")

rows = driver.find_elements(By.CSS_SELECTOR, "#table-body tr")
log("테이블 총 5행 확인", len(rows) == 5, f"{len(rows)}행")

first_row_cells = rows[0].find_elements(By.TAG_NAME, "td")

log("1행 이름 '김민준' 확인", first_row_cells[1].text == "김민준", first_row_cells[1].text)
log("1행 역할 'QA Engineer' 확인", first_row_cells[2].text == "QA Engineer")
log("1행 상태 '활성' 확인", "활성" in first_row_cells[4].text)


print("\n[TC-05] 드롭다운 선택")

select_el = Select(driver.find_element(By.ID, "role-select"))

select_el.select_by_value("qa")
result_text = driver.find_element(By.ID, "dropdown-result").text
log("'QA Engineer' 선택 결과 표시", "QA Engineer" in result_text, result_text)

select_el.select_by_visible_text("Project Manager")
result_text = driver.find_element(By.ID, "dropdown-result").text
log("'Project Manager' visible_text 선택", "Project Manager" in result_text, result_text)

select_el.select_by_index(0)
result_text = driver.find_element(By.ID, "dropdown-result").text
log("index=0 선택 시 결과 비워짐", result_text == "", repr(result_text))


print("\n[TC-06] 체크박스 다중 선택")

chk_ids = ["chk-functional", "chk-regression", "chk-security"]

for cid in chk_ids:
    chk = driver.find_element(By.ID, cid)
    if not chk.is_selected():
        chk.click()

time.sleep(0.2)
result_text = driver.find_element(By.ID, "checkbox-result").text
log("3개 체크박스 선택 결과 표시",
    "기능 테스트" in result_text and "보안 테스트" in result_text,
    result_text)

driver.find_element(By.ID, "chk-functional").click()
time.sleep(0.2)
result_text = driver.find_element(By.ID, "checkbox-result").text
log("체크 해제 후 항목 제거 확인", "기능 테스트" not in result_text, result_text)


print("\n[TC-07] 모달 팝업")

driver.find_element(By.ID, "open-modal-btn").click()

modal = wait.until(EC.visibility_of_element_located((By.ID, "modal-box")))
log("모달 열림 확인", modal.is_displayed())

driver.find_element(By.ID, "modal-confirm-btn").click()
time.sleep(0.3)   # 모달이 닫히는 애니메이션 대기

modal_result = driver.find_element(By.ID, "modal-action-result")
log("확인 클릭 시 result=confirmed",
    modal_result.get_attribute("data-result") == "confirmed",
    modal_result.get_attribute("data-result"))

log("모달 닫힘 확인", not modal.is_displayed())

driver.find_element(By.ID, "open-modal-btn").click()   # 다시 열기
wait.until(EC.visibility_of_element_located((By.ID, "modal-box")))
driver.find_element(By.ID, "modal-cancel-btn").click()  # 취소 클릭
time.sleep(0.3)
log("취소 클릭 시 result=cancel",
    modal_result.get_attribute("data-result") == "cancel",
    modal_result.get_attribute("data-result"))


print("\n[TC-08] 동적 콘텐츠 로드 (Explicit Wait)")

driver.find_element(By.ID, "load-content-btn").click()

log("로딩 중 텍스트 확인",
    "로딩" in driver.find_element(By.ID, "dynamic-text").text)

loaded_el = wait.until(EC.presence_of_element_located((By.ID, "dynamic-loaded")))
log("dynamic-loaded 요소 등장 확인", loaded_el is not None)

area = driver.find_element(By.ID, "dynamic-area")
log("data-loaded='true' 속성 확인", area.get_attribute("data-loaded") == "true",
    area.get_attribute("data-loaded"))


print("\n[TC-09] 카운터 버튼 반복 클릭")

for _ in range(5):
    driver.find_element(By.ID, "count-up-btn").click()

counter_el = driver.find_element(By.ID, "counter-display")

log("5번 클릭 후 카운터=5", counter_el.get_attribute("data-count") == "5",
    counter_el.get_attribute("data-count"))
log("카운터 표시 영역 노출", counter_el.is_displayed())

driver.find_element(By.ID, "count-reset-btn").click()
time.sleep(0.2)
log("리셋 후 카운터 숨겨짐", not counter_el.is_displayed())


print("\n[TC-10] 드래그 앤 드롭")

source_box = driver.find_element(By.ID, "drag-source")
target_box = driver.find_element(By.ID, "drag-target")
item_a     = driver.find_element(By.ID, "item-a")

before_in_source = item_a in source_box.find_elements(By.CLASS_NAME, "drag-item")
log("드래그 전 item-a가 source에 있음", before_in_source)

actions = ActionChains(driver)
actions.drag_and_drop(item_a, target_box).perform()
time.sleep(0.5)   # 드롭 애니메이션 대기

items_in_target = target_box.find_elements(By.CLASS_NAME, "drag-item")

log("드래그 후 item-a가 target으로 이동",
    any(i.get_attribute("id") == "item-a" for i in items_in_target))


print("\n" + "="*55)

total  = len(results)                          # 전체 테스트 수
passed = sum(1 for _, p in results if p)       # PASS 수 (p가 True인 것만 합산)
failed = total - passed                        # FAIL 수

print(f"  총 {total}건  |  {PASS} {passed}건  |  {FAIL} {failed}건")

if failed:
    print("\n  실패 케이스:")
    for name, p in results:
        if not p:
            print(f"    - {name}")

print("="*55 + "\n")

driver.quit()

