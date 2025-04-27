from pathlib import Path
from typing import Literal

from benedict import benedict
import voluptuous as vol

type Format = Literal['auto', 'yaml', 'json', 'dict', 'toml', 'ini']


class Configurator:
    def __init__(self, schema: vol.Schema):
        self.schema = schema
        self.config = None

    def load(self, config_source: Path | str | dict | benedict, format: Format = 'auto'):
        if format == 'auto':
            if isinstance(config_source, dict) or isinstance(config_source, benedict):
                raise ValueError('Cannot specify "auto" format for dict input')

            config_path = Path(config_source)

            match config_path.suffix:
                case '.yaml':
                    format = 'yaml'
                case '.json':
                    format = 'json'
                case '.toml':
                    format = 'toml'
                case '.ini':
                    format = 'ini'
                case _:
                    raise ValueError(f"Unsupported file extension: {config_path.suffix}")

        match format:
            case 'yaml':
                config = benedict.from_yaml(config_source)
            case 'json':
                config = benedict.from_json(config_source)
            case 'toml':
                config = benedict.from_toml(config_source)
            case 'dict':
                config = benedict(config_source)
            case 'ini':
                config = benedict.from_ini(config_source)
            case _:
                raise ValueError(f"Unsupported format specification: {format}")

        self.config = self.schema(config)

    def __getattr__(self, item: str):
        if self.config is None:
            raise AttributeError('Configuration is not loaded')

        return self.config[item]

    def __contains__(self, item: str):
        if self.config is None:
            raise AttributeError('Configuration is not loaded')

        return item in self.config
