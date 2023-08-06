from typing import Dict, Any
from pathlib import Path
import yaml

class DevUtils():
    """ DevUtils class is used in development (Local Machine) environement to load yaml configuration
        It can be used in Notebooks or Python test code
    """
    def get_conf_folder(self) -> Path:
        return Path(__file__).parent.parent.parent / "conf"

    def get_conf_tasks_folder(self) -> Path:
        return Path(__file__).parent.parent.parent / "conf/tasks"

    def read_config(self, conf_file_name) -> Dict[str, Any]:
        try:
            conf_folder = self.get_conf_tasks_folder()
            conf_file_path = conf_folder / conf_file_name
            print(conf_file_path)
            return DevUtils._read_config(conf_file=conf_file_path)
        except Exception as ex:
            print(f"read_config() - Error - {ex}")
            return {}

    @staticmethod
    def _read_config(conf_file) -> Dict[str, Any]:
        config = yaml.safe_load(Path(conf_file).read_text())
        return config

    def read_dev_config(self) -> Dict[str, Any]:
        return self.read_config(conf_file_name="app_config_dev.yml")

    def read_staging_config(self) -> Dict[str, Any]:
        return self.read_config(conf_file_name="app_config_staging.yml")

    def read_prod_config(self) -> Dict[str, Any]:
        return self.read_config(conf_file_name="app_config_prod.yml")

