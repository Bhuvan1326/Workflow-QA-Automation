# Testing Approach

## Functional Testing
Core user flows (login, project creation) are validated through Playwright,
using condition-based waits instead of fixed sleeps.

## API Testing
`test_project_creation_flow.py` uses Playwright's `APIRequestContext` to call
`POST /api/v1/projects` directly, validating response status and payload
before checking the same data through the UI.

## UI Testing
Playwright's `sync_api` drives the browser, with `expect()` assertions that
retry until an element or URL condition is met, avoiding flaky exact-match
checks.

## Multi-Tenant Testing
`test_multi_tenant.py` logs in as a Company2 user and confirms both that
Company2 data is visible and that Company1-only data is not. The test
asserts `projects.count() > 0` before checking for absence, so it cannot
pass simply because nothing loaded.

## Tenant Security Boundaries
Isolation is checked at the API layer too: a Company2 token/tenant header
requesting a Company1 project must receive `403` or `404`. This also guards
against a user swapping only the `X-Tenant-ID` header.

## Cross-Browser Testing
Playwright supports Chromium, Firefox, and WebKit out of the box. Tests can
run against each with `pytest --browser chromium`, `--browser firefox`, or
`--browser webkit`.

## Mobile / BrowserStack Strategy
`test_project_creation_flow.py` uses Playwright's built-in `iPhone 13` device
emulation for a lightweight mobile check. Real device coverage (e.g. Android
+ Chrome, iPhone + Safari) would run through BrowserStack, using credentials
from CI secrets, kept separate from the core test logic.

## Test Data Management
Non-sensitive user/project metadata lives in `test_data/*.json`. Dynamic
values (like project names) are generated per test run with `uuid.uuid4()`
to avoid collisions during parallel execution.

## Parallel Execution
`pytest-xdist` allows tests to run concurrently (`pytest -n auto`). Unique
test data generation is what makes this safe.

## Flaky Test Prevention
All waits use Playwright's auto-retrying `expect()` and `is_visible(timeout=...)`
instead of `time.sleep()` or fixed `wait_for_timeout()`.

## Cleanup Strategy
`test_project_creation_flow.py` deletes the project it creates in a `finally`
block, so cleanup runs even if an assertion fails mid-test.

## CI/CD Approach
On pull requests: run Chromium-only tests for fast feedback. Nightly: run
the full browser matrix plus BrowserStack device coverage. Reports are
published as build artifacts using `pytest-html`.
