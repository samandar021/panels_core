import json
import os
from copy import deepcopy
from functools import lru_cache


class ConfigManager:
    def __init__(self, config_dir='./configs'):  # По умолчанию папка с конфигами - ./configs
        self.config_dir = config_dir
        self.configs = {}
        self.load_configs()

    def load_configs(self):
        """Загрузка конфигов из папки с конфигами"""
        config_files = [f for f in os.listdir(self.config_dir) if f.endswith('.json')]
        for config_file in config_files:
            config_name = os.path.splitext(config_file)[0]
            with open(os.path.join(self.config_dir, config_file), 'r') as file:
                config_data = json.load(file)
                self.configs[config_name] = config_data

    def merge_configs(self):
        main_config = self.configs.get('config', {})  # Конфиг по умолчанию
        for config_name, config_data in self.configs.items():
            if config_name != 'config' and config_name != 'config-local':
                self.merge_config(main_config, config_data, config_name)
        return main_config

    def merge_config(self, target, source, section_name):
        parts = section_name.split('_')
        if len(parts) > 1:
            main_section, sub_section = parts[0], parts[1]
            if main_section not in target:
                target[main_section] = {}
            if sub_section not in target[main_section]:
                target[main_section][sub_section] = {}
            target[main_section][sub_section].update(source)
        else:
            target[section_name] = source

    def apply_local_overrides(self, config, local_config):
        """Переопределение конфигов локальными конфигами"""
        for key, value in local_config.items():
            if isinstance(value, dict) and key in config and isinstance(config[key], dict):
                self.apply_local_overrides(config[key], value)
            else:
                config[key] = value

    def get_configs(self):
        configs = self.merge_configs()

        local_config = self.configs.get('config-local', {})
        if local_config:
            local_configs = deepcopy(configs)
            self.apply_local_overrides(local_configs, local_config)
            configs.update(local_configs)

        return configs


@lru_cache()
def get_configs():
    """
    Возвращает словарь
    {
        "common": {
            "clickhouse_db": {
                "host": "127.0.0.1",
                ...
    """
    return ConfigManager().get_configs()
