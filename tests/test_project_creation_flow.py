import uuid
import pytest
from playwright.sync_api import expect


@pytest.mark.integration
def test_project_creation_flow(
    playwright, page, base_url, company1, company2,
    require_company1_token, require_company2_token,
):
    project_name = f"Test Project {uuid.uuid4().hex[:8]}"

    api = playwright.request.new_context(base_url=base_url)
    project_id = None

    try:
        response = api.post(
            "/api/v1/projects",
            headers={
                "Authorization": f"Bearer {company1['token']}",
                "X-Tenant-ID": company1["id"],
            },
            data={
                "name": project_name,
                "description": "Automation project",
                "team_members": [],
            },
        )

        assert response.ok

        project = response.json()
        assert project["name"] == project_name

        project_id = project["id"]

        page.goto(f"{base_url}/projects")
        expect(page.get_by_text(project_name, exact=True)).to_be_visible(timeout=30000)

        iphone = playwright.devices["iPhone 13"]
        browser = playwright.webkit.launch()
        context = browser.new_context(**iphone)
        mobile_page = context.new_page()

        mobile_page.goto(f"{base_url}/projects")
        expect(mobile_page.get_by_text(project_name, exact=True)).to_be_visible(timeout=30000)

        context.close()
        browser.close()

        isolation = api.get(
            f"/api/v1/projects/{project_id}",
            headers={
                "Authorization": f"Bearer {company2['token']}",
                "X-Tenant-ID": company2["id"],
            },
        )

        assert isolation.status in (403, 404)

    finally:
        if project_id:
            api.delete(
                f"/api/v1/projects/{project_id}",
                headers={
                    "Authorization": f"Bearer {company1['token']}",
                    "X-Tenant-ID": company1["id"],
                },
            )

        api.dispose()
