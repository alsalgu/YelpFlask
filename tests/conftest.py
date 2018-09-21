from app import create_app
from config import Config
import pytest


class TestConfig(Config):
    TESTING = True
    WTF_CSRF_ENABLED = False

@pytest.fixture
def app():
    app = create_app(TestConfig)
    return app