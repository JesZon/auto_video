import json
import os
import sys

from openai import OpenAI


#  ====================================================================
def resource_path(relative_path):
    """获取资源文件的路径"""
    if hasattr(sys, '_MEIPASS'):
        # 打包后的环境
        return os.path.join(sys._MEIPASS, relative_path)
    # 开发环境
    return os.path.join(os.path.abspath("."), relative_path)
#  ====================================================================

# 使用 resource_path 函数获取基础路径
package_dir_os = resource_path("").replace("auto_operate", "")

# ai文章生成的保存路径
__ai_article_path__ = resource_path(os.path.join(package_dir_os, "is_ai_article_data"))

__comfyui_path__ = resource_path(os.path.join(package_dir_os, "is_comfyui_data"))

__Jianying_path__ = resource_path(os.path.join(package_dir_os, "is_jianying_data"))

# comfyui的本地服务地址
__comfyui_localhost__ = '127.0.0.1:8188'

# 每个镜头comfyui的图片生成次数
__lens_batch__ = 1

# 定义全局变量
client = None
__draft_path__ = None


def get_config():
    config_path = resource_path("public/config.json")
    with open(config_path, "r", encoding="utf-8") as f:
        config = json.load(f)
        return config


def load_config():
    global client, __draft_path__
    config = get_config()
    client = OpenAI(
        api_key=config["api_key"],
        base_url=config["base_url"],
    )
    __draft_path__ = config["jianying_draft"] + "/"


# 初始化配置
load_config()


def set_config(config):
    global client, __draft_path__
    config_path = resource_path("public/config.json")
    with open(config_path, 'w', encoding='utf-8') as f:
        json.dump(config, f, ensure_ascii=False, indent=4)
    # 重新加载配置
    load_config()


from .ai_article import AIArticle
from .comfyui import ComfyUI
from .jianying_draft import JianYingDraft