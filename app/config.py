import os
from pathlib import Path
from typing import Type


def _read_secret(var_name: str, default: str | None = None) -> str | None:
    file_env = os.environ.get(f"{var_name}_FILE")
    if file_env:
        path = Path(file_env)
        if path.is_file():
            return path.read_text(encoding='utf-8').strip()
    secrets_path = Path('/run/secrets') / var_name.lower()
    if secrets_path.is_file():
        return secrets_path.read_text(encoding='utf-8').strip()
    value = os.environ.get(var_name)
    if value is not None:
        return value
    return default


class BaseConfig:
    SECRET_KEY = _read_secret('SECRET_KEY', 'dev-secret')
    MYSQL_HOST = os.environ.get('MYSQL_HOST', 'mysql')
    MYSQL_DATABASE = os.environ.get('MYSQL_DATABASE', 'petshop')
    MYSQL_USER = os.environ.get('MYSQL_USER', 'petshop')
    MYSQL_PASSWORD = _read_secret('MYSQL_PASSWORD', 'petshoppw')
    MYSQL_PORT = int(os.environ.get('MYSQL_PORT', 3306))
    MYSQL_CHARSET = 'utf8mb4'
    CACHE_DEFAULT_TTL = int(os.environ.get('CACHE_DEFAULT_TTL', 60))
    CACHE_NEWS_TTL = int(os.environ.get('CACHE_NEWS_TTL', 120))
    CACHE_SERVICES_TTL = int(os.environ.get('CACHE_SERVICES_TTL', 300))
    CACHE_ABOUT_TTL = int(os.environ.get('CACHE_ABOUT_TTL', 600))


class DevelopmentConfig(BaseConfig):
    DEBUG = True


class TestingConfig(BaseConfig):
    TESTING = True
    MYSQL_DATABASE = os.environ.get('MYSQL_DATABASE', 'petshop_test')


class ProductionConfig(BaseConfig):
    DEBUG = False


_CONFIG_MAP: dict[str, Type[BaseConfig]] = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
}


def get_config(env_name: str | None = None) -> Type[BaseConfig]:
    name = (env_name or os.environ.get('APP_ENV') or os.environ.get('FLASK_ENV') or 'development').lower()
    return _CONFIG_MAP.get(name, DevelopmentConfig)
