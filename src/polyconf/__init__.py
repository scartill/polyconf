from pathlib import Path
from typing import Literal
from argparse import ArgumentParser

from benedict import benedict
import voluptuous as vol
import voluptuous.schema_builder as vsc

type Format = Literal['auto', 'yaml', 'json', 'dict', 'toml', 'ini']


class Configurator:
    def __init__(self, schema: vol.Schema):
        self.schema = schema
        self.config = None
        self.params = []
        self._collect_params([], self.params, self.schema.schema)

    def load(
        self, config_source: Path | str | dict | benedict,
        *,
        format: Format = 'auto',
        bypass_validation: bool = False,
        use_cli_args: bool = True
    ):
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

        if not bypass_validation:
            self.config = self.schema(config)

        if use_cli_args:
            self.process_args()

    def __getattr__(self, item: str):
        if self.config is None:
            raise AttributeError('Configuration is not loaded')

        return self.config[item]

    def __contains__(self, item: str):
        if self.config is None:
            raise AttributeError('Configuration is not loaded')

        return item in self.config

    def _collect_params(self, prefix: list[str], params: list[tuple[list[str], type]], schema):
        for item_name, item in schema.items():
            if isinstance(item, vsc.Required):
                self._collect_params(prefix, params, item.schema)
            elif isinstance(item, vsc.Schema):
                self._collect_params(prefix + [item_name], params, item.schema)
            elif item is int:
                params.append((prefix + [item_name], int))
            elif item is str:
                params.append((prefix + [item_name], str))
            elif item is bool:
                params.append((prefix + [item_name], bool))
            elif item is float:
                params.append((prefix + [item_name], float))
            else:
                raise ValueError(f'[{prefix}] Unknown schema item {item} type {type(item)}')

    def parser(self):
        parser = ArgumentParser()

        for prefix, param_type in self.params:
            param_name = '-'.join(map(str, prefix))
            parser.add_argument(f'--{param_name}', type=param_type)

        return parser

    def process_args(self):
        if self.config is None:
            raise AttributeError('Configuration is not loaded')

        parser = self.parser()
        args = parser.parse_args()

        for prefix, _ in self.params:
            arg_param_name = '_'.join(map(str, prefix))
            config_param_name = '.'.join(map(str, prefix))

            if args_value := getattr(args, arg_param_name):
                self.config[config_param_name] = args_value
