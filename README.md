<div align="center">
  <a href="https://v2.nonebot.dev/store"><img src="https://github.com/A-kirami/nonebot-plugin-template/blob/resources/nbp_logo.png" width="180" height="180" alt="NoneBotPluginLogo"></a>
  <br>
  <p><img src="https://github.com/A-kirami/nonebot-plugin-template/blob/resources/NoneBotPlugin.svg" width="240" alt="NoneBotPluginText"></p>
</div>

<div align="center">

# nonebot_plugin_requests

_✨ 封装 ForwardDriver 实现 HttpClient 功能 ✨_

## 📖 介绍

本插件提供了 HttpClient 的封装, 简化了网络请求调用

## 💿 安装

<details>
<summary>使用 nb-cli 安装</summary>
在 nonebot2 项目的根目录下打开命令行, 输入以下指令即可安装

    nb plugin install nonebot-plugin-requests

</details>

<details>
<summary>使用包管理器安装</summary>
在 nonebot2 项目的插件目录下, 打开命令行, 根据你使用的包管理器, 输入相应的安装命令

<details>
<summary>pip</summary>

    pip install nonebot-plugin-requests
</details>
<details>
<summary>pdm</summary>

    pdm add nonebot-plugin-requests
</details>
<details>
<summary>poetry</summary>

    poetry add nonebot-plugin-requests
</details>
<details>
<summary>conda</summary>

    conda install nonebot-plugin-requests
</details>

打开 nonebot2 项目根目录下的 `pyproject.toml` 文件, 在 `[tool.nonebot]` 部分追加写入

    plugins = ["nonebot_plugin_example"]

</details>

## ⚙️ 配置

在 nonebot2 项目的`.env`文件中添加下表中的配置

| 配置项 | 必填 | 默认值 | 说明 |
|:-----:|:----:|:----:|:----:|
| nonebot_plugin_requests_enable_proxy | 否 | False | 是否使用代理 |
| nonebot_plugin_requests_proxy_type | 否 | http | 代理类型(仅限http) |
| nonebot_plugin_requests_proxy_address | 否 | 127.0.0.1 | 代理地址 |
| nonebot_plugin_requests_proxy_port | 否 | 1081 | 代理端口 |

## 🎉 使用

参考示例如下:

</div>

```python
import nonebot

nonebot.require("nonebot_plugin_requests")

from nonebot_plugin_requests import NonebotRequests


async def get_something():
    request = NonebotRequests()
    response = await request.get(...)

    json = NonebotRequests.parse_content_json(response)
    text = NonebotRequests.parse_content_text(response)
    ...

```
