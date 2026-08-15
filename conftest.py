import os
import json
import pytest
from dotenv import load_dotenv

load_dotenv()


def _env_available() -> bool:
    #Whether a real, reachable WorkFlow Pro environment was provided.
    return os.getenv("WORKFLOWPRO_ENV_AVAILABLE", "false").strip().lower() == "true"


@pytest.fixture(scope="session")
def base_url():
    return os.getenv("BASE_URL", "https://app.workflowpro.com")


@pytest.fixture(scope="session")
def company1():
    return {
        "id": os.getenv("COMPANY1_ID", "company1"),
        "email": os.getenv("COMPANY1_EMAIL", ""),
        "password": os.getenv("COMPANY1_PASSWORD", ""),
        "token": os.getenv("COMPANY1_TOKEN", ""),
    }


@pytest.fixture(scope="session")
def company2():
    return {
        "id": os.getenv("COMPANY2_ID", "company2"),
        "email": os.getenv("COMPANY2_EMAIL", ""),
        "password": os.getenv("COMPANY2_PASSWORD", ""),
        "token": os.getenv("COMPANY2_TOKEN", ""),
    }


@pytest.fixture(autouse=True)
def _require_live_env():
    #Every test here talks to a real WorkFlow Pro instance.

    #Without WORKFLOWPRO_ENV_AVAILABLE=true, skip instead of failing on DNS/SSL errors against the assessment's placeholder URL.
    
    if not _env_available():
        pytest.skip("WorkFlow Pro live test environment is not available.")


@pytest.fixture
def require_company1_login(company1):
    if not company1["email"] or not company1["password"]:
        pytest.skip("COMPANY1_EMAIL/COMPANY1_PASSWORD are not configured.")


@pytest.fixture
def require_company2_login(company2):
    if not company2["email"] or not company2["password"]:
        pytest.skip("COMPANY2_EMAIL/COMPANY2_PASSWORD are not configured.")


@pytest.fixture
def require_company1_token(company1):
    if not company1["token"]:
        pytest.skip("COMPANY1_TOKEN is not configured.")


@pytest.fixture
def require_company2_token(company2):
    if not company2["token"]:
        pytest.skip("COMPANY2_TOKEN is not configured.")


@pytest.fixture(scope="session")
def test_users():
    path = os.path.join(os.path.dirname(__file__), "test_data", "users.json")
    with open(path) as f:
        return json.load(f)


@pytest.fixture(scope="session")
def test_projects():
    path = os.path.join(os.path.dirname(__file__), "test_data", "projects.json")
    with open(path) as f:
        return json.load(f)
