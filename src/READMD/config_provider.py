import json
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, Dict, Union


class ConfigProvider(ABC):
    _config: Dict[str, Any]

    def __init__(self) -> None:
        self.get_config()

    @abstractmethod
    def get_config(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def get(self, key: str) -> Any:
        raise NotImplementedError


class JsonConfigProvider(ConfigProvider):
    def __init__(self, config_file: Union[str, Path]) -> None:
        if isinstance(config_file, Path):
            self._config_file = config_file.absolute()
        else:
            self._config_file = config_file
        super().__init__()

    def get_config(self) -> None:
        with open(self._config_file, "r") as file:
            self._config = json.load(file)

    def get(self, key: str) -> Any:
        return self._config.get(key)
