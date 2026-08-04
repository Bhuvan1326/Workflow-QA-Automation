# WorkFlow Pro – QA Automation

QA automation for **WorkFlow Pro**, a hypothetical B2B multi-tenant SaaS
platform, built for a take-home assignment. Covers login, multi-tenant data
isolation, and an API-to-UI project creation flow.

## Tech Stack
- Python 3.11+
- pytest / pytest-playwright / pytest-xdist / pytest-html
- Playwright (Chromium, Firefox, WebKit)
- BrowserStack (concepts only — see `docs/testing_approach.md`)
- REST API testing via Playwright's `APIRequestContext`

## Repository Structure
```
workflowpro-qa-automation/
├── README.md
├── test_plan.md
├── requirements.txt
├── pytest.ini
├── conftest.py
├── .env.example
├── .gitignore
├── tests/
│   ├── test_login.py
│   ├── test_multi_tenant.py
│   └── test_project_creation_flow.py
├── test_data/
│   ├── users.json
│   └── projects.json
├── reports/
│   └── test_report.html
└── docs/
    └── testing_approach.md
```

## Setup

### 1. Install dependencies
```bash
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Install Playwright browsers
```bash
playwright install
```

### 3. Environment variables
Copy the example file and fill in real values (never commit `.env`):
```bash
cp .env.example .env
```
See `.env.example` for the full list of variables (base URL, tenant IDs,
test-user credentials/tokens, 2FA code, BrowserStack credentials).

`WORKFLOWPRO_ENV_AVAILABLE` controls whether tests run for real. It defaults
to `false`, so live tests are skipped until you set it to `true` and fill in
the matching credentials/tokens. See **Execution Note** below.

## Running Tests

Verify test discovery (does not require a live environment):
```bash
pytest --collect-only
```

Run the full suite:
```bash
pytest
```

Run a single file:
```bash
pytest tests/test_login.py
```

Run only integration tests:
```bash
pytest -m integration
```

Run in parallel:
```bash
pytest -n auto
```

### Run on different browsers
```bash
pytest --browser chromium
pytest --browser firefox
pytest --browser webkit
```

### Generate the HTML report
```bash
pytest --html=reports/test_report.html --self-contained-html
```
Note: `reports/test_report.html` currently contains a clearly labeled
placeholder, since these tests have not been run against a live WorkFlow Pro
environment. Running the command above will replace it with a real report.
Without a live environment (`WORKFLOWPRO_ENV_AVAILABLE=false`, the default),
that report will show tests as **skipped**, not failed or passed.

## What Parts 1–3 Cover
- **Part 1 – Login (`tests/test_login.py`)**: fixes the original flaky login
  test by waiting on real page state (URL pattern + welcome message) instead
  of fixed delays, and supports optional 2FA.
- **Part 2 – Multi-tenant isolation (`tests/test_multi_tenant.py`)**: confirms
  a Company2 user sees Company2 data and never sees Company1-only data, and
  guards against a false pass when zero projects load.
- **Part 3 – API + UI integration (`tests/test_project_creation_flow.py`)**:
  creates a project via the API, verifies it in the desktop and mobile UI,
  confirms another tenant cannot access it, and deletes it during cleanup.

## Execution Note

This assessment does not provide a live WorkFlow Pro test environment, and
valid Company1/Company2 credentials and API tokens were not supplied. The
automation suite itself is implementation-ready: all 5 tests are written
and discoverable (`pytest --collect-only`).

When `WORKFLOWPRO_ENV_AVAILABLE` is not set to `true`, and when required
per-test credentials/tokens are missing, the affected tests are **skipped**
with a clear reason rather than run against an unreachable host. This
avoids both false failures (from DNS/SSL errors on a non-existent domain)
and, more importantly, fake successful results from tests that never
actually executed their assertions.

Setting `WORKFLOWPRO_ENV_AVAILABLE=true` and providing real
Company1/Company2 credentials and API tokens in `.env` enables live
execution against a real WorkFlow Pro instance, with all original
assertions intact.

## Assumptions
See `test_plan.md` and `docs/testing_approach.md` for the full list. In
short: WorkFlow Pro is treated as hypothetical for this assignment, so
selectors and endpoints follow the take-home description but have not been
verified against a live system.
