import os
from pathlib import Path

from pydantic import BaseSettings

env_file_path = Path(__file__).parent.parent / ".env"


class DevSettings(BaseSettings):
    is_local_dev: bool = False

    @property
    def is_under_test(self):
        return "PYTEST_CURRENT_TEST" in os.environ

    class Config:
        env_file = env_file_path


dev_settings = DevSettings()
