import os
from pathlib import Path

env_file_path = Path(__file__).parent.parent / ".env"


class DevSettings():
    is_local_dev: bool = False if not os.environ.get("LOCAL_DEV") else True

    @property
    def is_under_test(self):
        return "PYTEST_CURRENT_TEST" in os.environ

    class Config:
        env_file = env_file_path


dev_settings = DevSettings()
