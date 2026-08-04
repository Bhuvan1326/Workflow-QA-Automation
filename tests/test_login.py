import os
import re
import pytest
from playwright.sync_api import Page, expect


def login(page: Page, base_url: str, email: str, password: str):
    page.goto(f"{base_url}/login")

    page.locator("#email").fill(email)
    page.locator("#password").fill(password)
    page.locator("#login-btn").click()

    otp_form = page.locator("[data-testid='two-factor-form']")

    if otp_form.is_visible(timeout=3000):
        otp = os.getenv("TEST_2FA_CODE")

        if not otp:
            pytest.fail("2FA code required but TEST_2FA_CODE is not set")

        page.locator("[data-testid='otp-input']").fill(otp)
        page.locator("[data-testid='verify-otp']").click()

    expect(page).to_have_url(re.compile(r".*/dashboard.*"), timeout=30000)
    expect(page.locator(".welcome-message")).to_be_visible(timeout=30000)


def test_user_login(page: Page, base_url, company1, require_company1_login):
    login(page, base_url, company1["email"], company1["password"])


def test_login_invalid_credentials_shows_error(page: Page, base_url):
    page.goto(f"{base_url}/login")

    page.locator("#email").fill("invalid.user@example.com")
    page.locator("#password").fill("wrong-password")
    page.locator("#login-btn").click()

    expect(page.locator("[data-testid='login-error']")).to_be_visible(timeout=10000)
