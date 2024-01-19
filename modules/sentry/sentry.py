import sentry_sdk

from modules.config_manager.config_manager import get_configs


def run_sentry():
    configs = get_configs()
    dsn_key = configs['common']['sentry_key']

    if isinstance(dsn_key, str) and 'http' in dsn_key:
        sentry_sdk.init(
            dsn=dsn_key,
            traces_sample_rate=1.0,
        )
