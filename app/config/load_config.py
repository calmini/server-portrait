
from app.config.app_config import AppConfigSetting
from functools import lru_cache

# 通过本地配置文件, 加载到系统路径中去?
def get_env_file():
    return ""


@lru_cache
def getAppConfig():
    # 配置文件
    return AppConfigSetting()



globalAppConfigure = getAppConfig()