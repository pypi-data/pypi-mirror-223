# -*- coding: utf-8 -*-
import os
import shutil
import sys
from pathlib import Path

from pydantic import BaseSettings

SELECTED_ENV_NAME = os.environ.get('APP_ENV_NAME')


class BaseSettingMixin(BaseSettings):
    class Config:
        case_sensitive = True
        validate_assignment = True

    @classmethod
    def get_selected_env(cls) -> str:
        if SELECTED_ENV_NAME in ('dev', 'stg', 'prod', 'local', 'redirect'):
            env_name = f'{SELECTED_ENV_NAME}.env'
        else:
            env_name = '.env'
        return env_name

    @classmethod
    def get_env_file_path(cls, env_name: str) -> str:
        env_file_path = os.path.join(os.getcwd(), 'envs', env_name)
        if not os.path.isfile(env_file_path):
            example_env_file_path = os.path.join(os.getcwd(), 'envs', 'example.env')
            if os.path.isfile(example_env_file_path):
                shutil.copy2(example_env_file_path, env_file_path)
            else:
                with open(env_file_path, 'w') as f:  # noqa
                    # create default env file,
                    # for now .env is empty
                    # os environments will be used
                    pass
        return env_file_path

    def setup(self, from_env: str, **kwargs):
        self.add_custom_proxy()
        self.notify_environment(from_env)
        # self.add_core_sys_path()

    def notify_environment(self, from_env: str):
        print(2 * '\n' + 50 * '-' + '\n')
        print('you select environment: ', from_env)
        print(f'http_proxy {os.environ.get("http_proxy")}')
        print(f'https_proxy {os.environ.get("https_proxy")}')
        print(f'no_proxy {os.environ.get("no_proxy")}')
        print('\n\n')

    def add_custom_proxy(self):
        if (
            not hasattr(self, 'SERVICE_USE_PROXY')
            or not hasattr(self, 'SERVICE_PROXY_ADDR')
            or not hasattr(self, 'SERVICE_NO_PROXY')
        ):
            print('Not found proxy configurations')
            return

        if not getattr(self, 'SERVICE_USE_PROXY'):
            return

        no_proxy = os.environ.get('no_proxy')

        if getattr(self, 'SERVICE_USE_PROXY'):
            os.environ['http_proxy'] = getattr(self, 'SERVICE_PROXY_ADDR')
            os.environ['https_proxy'] = getattr(self, 'SERVICE_PROXY_ADDR')
        if getattr(self, 'SERVICE_NO_PROXY'):
            if no_proxy:
                os.environ['no_proxy'] = no_proxy + ',' + getattr(self, 'SERVICE_NO_PROXY')
            else:
                os.environ['no_proxy'] = getattr(self, 'SERVICE_NO_PROXY')

    def add_core_sys_path(self):
        current_path = Path(os.getcwd())
        sys.path.append(str(current_path.parents[1]))
