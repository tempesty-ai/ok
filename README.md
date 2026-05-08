# Senior QA Engineer Portfolio - Web Automation Foundation

> A repository that documents a practical foundation for UI automation used to reduce regression risk.
> The focus is not automation for its own sake, but how QA chooses what is worth automating.

## Data Disclaimer

All test scenarios, selectors, and validation criteria in this repository are based on public demo sites such as `practicesoftwaretesting.com`. This repository does not contain screens, data, selectors, or internal specifications from any current or former company or customer system.

## Problem

Manual regression checks before release take time and can become inconsistent. Automating every screen is also expensive and often low-value.

This repository shows a risk-based approach: protect repeated, high-impact user flows with automation while keeping exploratory and uncertain areas in human QA review.

## Positioning

| Area | Direction |
| --- | --- |
| Role | QA Engineer focused on product quality as a whole |
| Strength | Requirements review, test strategy, regression scope, defect analysis, release gates |
| Automation use | Supporting repeated regression and core flow protection |
| Scope | Practical automation that a QA team can understand and operate |

## Why Selenium And Playwright Are Both Included

| Folder | Purpose | Characteristics | Automation target |
| --- | --- | --- | --- |
| `selenium/` | Smoke checks for core UI flows | Single-run scripts, WebDriverWait, Select, ActionChains | Fast confirmation of key entry flows |
| `playwright/` | Structured pytest-based regression | Fixtures, Page Object, API mock, screenshots, headed mode | Repeated regression that benefits from maintainability |

The point is not that one tool is universally better. The point is choosing the tool based on risk, frequency, and maintenance cost.

## Test Strategy

| Area | Approach | Criteria |
| --- | --- | --- |
| Core user flow | Prioritize automation | High regression frequency and high failure impact |
| New feature validation | Manual and exploratory | Requirements or UX are still uncertain |
| UI interaction | Risk-based automation | Inputs, dropdowns, modals, dynamic loading, repeated validation |
| Failure analysis | Evidence capture | Screenshots, logs, and state values for quick diagnosis |

## Selenium Cases

| ID | Scenario | Validation intent |
| --- | --- | --- |
| TC-01 | Successful login | Confirms expected success state |
| TC-02 | Failed login/reset | Confirms invalid input and reset behavior |
| TC-03 | Table search filter | Confirms displayed rows match the keyword |
| TC-04 | Table row data | Confirms key cells match expected values |
| TC-05 | Dropdown selection | Confirms value/text/index selection behavior |
| TC-06 | Multiple checkboxes | Confirms selected and cleared states |
| TC-07 | Modal popup | Confirms open, close, confirm, and cancel states |
| TC-08 | Dynamic content load | Confirms explicit wait for generated DOM |
| TC-09 | Counter clicks | Confirms repeated action and reset state |
| TC-10 | Drag and drop | Confirms ActionChains movement result |

## Playwright Cases

| Area | IDs | Scenario |
| --- | --- | --- |
| Navigation | PW-01 to PW-06 | Tabs, tooltips, notices, page title |
| Task Management | PW-07 to PW-15 | Add, enter key, empty value, progress, filters, delete |
| FAQ | PW-16 to PW-18 | Accordion open, single-open policy, close toggle |
| API / Network | PW-19 to PW-20 | Mock API response and aborted request handling |
| Evidence / Stats | PW-21 to PW-24 | Screenshots, tab capture, chart/stat validation |

## Outcome

| Item | Measurement |
| --- | --- |
| Automated core regression cases | Selenium 10 + Playwright 24 = 34 cases |
| Core flow regression time | Manual about 30 minutes -> automated about 3 to 4 minutes |
| Failure evidence | Screenshot, console log, and state capture |
| Maintenance approach | Page Object and fixture separation |

These are repository-level sample measurements, not results from a company production system.

## Quick Run

Open demo pages manually:

```bash
open_selenium_demo.bat
open_playwright_demo.bat
```

Run automation:

```bash
run_selenium_tests.bat
run_playwright_tests.bat
run_playwright_headed.bat
```

Run Playwright directly:

```bash
cd playwright
py test_demo.py --headed --slowmo 800
```

## Setup

Python 3.10+ is recommended.

```bash
cd selenium
pip install -r requirements.txt
python test_demo.py

cd ../playwright
pip install -r requirements.txt
playwright install
pytest -v
```

Allure is optional. The repository is designed so the basic pytest flow can run without Allure being installed.

## Operating Notes

- The goal is release stability, not a high automation count.
- Repeated regression candidates are prioritized before low-value broad coverage.
- Test code is treated as quality evidence that supports team decisions.
- Runtime artifacts are ignored; reproducible code and documentation stay in git.

## Roadmap

- Add API-layer regression cases
- Keep visual regression in the sibling `UI_Test` repository
- Connect CI failure notifications to the sibling `botserver` project

## Repository Rename Suggestion

Consider renaming `ok` to a clearer repository name:

- `qa-automation-portfolio`
- `web-regression-suite`
- `ui-automation-foundation`

Rename path: GitHub web -> Settings -> General -> Repository name -> Rename.

After renaming, update the local remote URL:

```bash
git remote set-url origin https://github.com/tempesty-ai/<new-name>.git
```