from playwright.sync_api import Page, expect
from tests.test_login import login


def test_company2_user_sees_own_data(page: Page, base_url, company2, require_company2_login):
    login(page, base_url, company2["email"], company2["password"])

    page.goto(f"{base_url}/projects")

    projects = page.locator(".project-card")
    expect(projects.first).to_be_visible(timeout=30000)

    assert projects.count() > 0, "Expected at least one project to load for Company2"

    expect(page.get_by_text("Company2 Test Project")).to_be_visible()


def test_company2_user_cannot_see_company1_data(page: Page, base_url, company2, require_company2_login):
    login(page, base_url, company2["email"], company2["password"])

    page.goto(f"{base_url}/projects")

    projects = page.locator(".project-card")
    expect(projects.first).to_be_visible(timeout=30000)

    assert projects.count() > 0, "Test would falsely pass if zero projects loaded"

    expect(page.get_by_text("Company1 Private Project")).to_have_count(0)
