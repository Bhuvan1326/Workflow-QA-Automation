# Test Plan – WorkFlow Pro

## Objectives
Validate that WorkFlow Pro's login, project creation, and multi-tenant
isolation work correctly across browsers and devices, and that the
automation suite itself is reliable (non-flaky) enough for CI use.

## Scope
In scope: login (incl. optional 2FA), project creation (API + UI), tenant
data isolation, role-based access assumptions, cross-browser checks, and a
basic mobile check.

Out of scope: full regression of every WorkFlow Pro feature, performance/load
testing, and exhaustive BrowserStack device coverage (only a representative
sample is covered here given the 90-minute scope).

## Features Being Tested

### Login
- Successful login with valid credentials
- Error shown for invalid credentials
- Optional 2FA challenge handled when present

### 2FA
- If a 2FA form appears after login, an OTP is submitted from
  `TEST_2FA_CODE`; if the app requires 2FA but no code is configured, the
  test fails loudly instead of silently skipping.

### Project Creation
- Project created via `POST /api/v1/projects`
- Response validated for correct name/status
- Project visible in the web UI shortly after creation
- Project visible on a mobile viewport (iPhone 13 emulation)
- Project deleted during cleanup

### API Testing
- Response status and JSON body assertions for project creation
- Status code assertions (`403`/`404`) for cross-tenant access attempts

### Tenant Isolation
- Company2 users see Company2 data and not Company1 data
- Company1 token cannot fetch a resource under `X-Tenant-ID: company2` (or
  vice versa) even if the header is swapped manually

### Role-Based Access
- Assumption-based only in this take-home: Admin/Manager/Employee roles are
  captured in `test_data/users.json` for future permission tests, but no
  live permission checks are automated here (see Assumptions).

### Cross-Browser Testing
- Login flow can run against Chromium, Firefox, and WebKit via
  `pytest --browser`

### Mobile Testing
- One mobile check (project visibility) via Playwright's `iPhone 13`
  emulation; real-device coverage is described conceptually for BrowserStack
  but not executed here

## Browsers / Devices
- Desktop: Chromium, Firefox, WebKit (via Playwright)
- Mobile (emulated): iPhone 13
- Real-device matrix (BrowserStack, not run in this repo): Android + Chrome,
  iPhone + Safari

## Test Data Strategy
- Static, non-sensitive user/project metadata in `test_data/*.json`
- Dynamic project names generated per run with `uuid.uuid4()` to avoid
  collisions, especially under parallel execution
- Real credentials/tokens only ever come from environment variables, never
  from files committed to the repo

## Entry Criteria
- `BASE_URL` points to a reachable WorkFlow Pro environment
- Company1/Company2 test accounts and (for API tests) tokens exist
- Dependencies and Playwright browsers installed

## Exit Criteria
- All tests pass locally against the target environment
- No hard-coded secrets in the repo
- `reports/test_report.html` reflects an actual run (not a fabricated one)

## Risks
- WorkFlow Pro is a hypothetical app for this assignment, so tests are
  written against the documented behavior in the README but have not been
  run against a live system
- Selectors (`#email`, `.project-card`, etc.) are assumptions based on the
  README and may not match the real DOM
- 2FA delivery mechanism for automation is unspecified

## Assumptions
- A staging/test environment is available
- Test users exist for Company1 and Company2
- Test API tokens can be generated/provided securely via CI secrets
- 2FA can use a dedicated automation-friendly code (`TEST_2FA_CODE`)
- Projects can be deleted through the API
- BrowserStack credentials are available through CI secrets
- Role-based access is captured as test data now, with live checks left as a
  follow-up beyond this take-home's scope
