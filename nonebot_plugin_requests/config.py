'''
@Author         :   Ailitonia
@Date           :   2023/08/23 23:43:14
@FileName       :   config.py
@Description    :   nonebot-plugin-requests config
@GitHub         :   https://github.com/Ailitonia
@Software       :   PyCharm
'''


from nonebot import get_driver
from typing import Literal
from pydantic import BaseModel, IPvAnyAddress


class NonebotPluginRequestsConfig(BaseModel):
    """nonebot-plugin-requests 插件配置"""
    nonebot_plugin_requests_enable_proxy: bool = False
    nonebot_plugin_requests_proxy_type: Literal['http'] = 'http'
    nonebot_plugin_requests_proxy_address: IPvAnyAddress = '127.0.0.1' # type: ignore
    nonebot_plugin_requests_proxy_port: int = 1081

    class Config:
        extra = "ignore"

    @property
    def proxy_url(self) -> str | None:
        if self.nonebot_plugin_requests_enable_proxy:
            proxy = f'{self.nonebot_plugin_requests_proxy_type}://{self.nonebot_plugin_requests_proxy_address}:{self.nonebot_plugin_requests_proxy_port}'
        else:
            proxy = None
        return proxy


plugin_config = NonebotPluginRequestsConfig.parse_obj(get_driver().config)


__all__ = [
    'plugin_config'
]
