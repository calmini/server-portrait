
class AppConfigSetting:
    # 定义一些配置信息
    connector_limit: int = 50 # 限制连接池最大连接数
    max_asyncio_req_limit: int = 100 # 限制单次最大并发量为30, 仅限query

    # 启动
    host = '0.0.0.0'
    port = 8888

    # 查询域名
    baseHbaseURL: str = "xxx" # 填充hbase域名
    baseRedisNAME: str = "admin" # 填充redis用户
    baseRedisURL: str = "" # 填充redis域名
    baseRedisPORT: int = -1 # 填充redis端口
    baseRedisPWD: str = "xxx" # 填充redis密码

    # 查询配置
    futureQueryPeriod: int = 30 * 1440 * 60 # 30D
    lastQueryPeriod: int = 1 * 1440 * 60 # 1D
    



