'''
@Author         :   Ailitonia
@Date           :   2023/08/23 23:42:26
@FileName       :   __init__.py
@Description    :   封装 ForwardDriver 实现 HttpClient 功能
@GitHub         :   https://github.com/Ailitonia
@Software       :   PyCharm
'''

from nonebot.plugin import PluginMetadata

from .config import plugin_config


__plugin_meta__ = PluginMetadata(
    name='Nonebot Requests',
    description='封装 ForwardDriver 实现 HttpClient 功能',
    usage='声明依赖: `require("nonebot_plugin_requests")\n'
          '导入: `from nonebot_plugin_requests import NonebotRequests`\n'
          '使用: `NonebotRequests().get(...)`\n',
    type='library',
    homepage='https://github.com/Ailitonia/nonebot-plugin-requests',
    config=plugin_config.__class__,
    supported_adapters=None,
    extra={'author': 'Ailitonia'},
)


from .requests import NonebotRequests as NonebotRequests


__all__ = ['NonebotRequests']
