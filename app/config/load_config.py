
from app.config.app_config import AppConfigSetting
from functools import lru_cache

# 通过本地配置文件, TODO 加载到系统路径中去?
def get_env_file():
    return ""


## TODO yml配置文件?


@lru_cache
def getAppConfig():
    # 配置文件, TODO 是否需要覆盖?
    return AppConfigSetting()



globalAppConfigure = getAppConfig()