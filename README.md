拉起服务器 python server.py 直接通过 http://0.0.0.0:8888 访问
只写了个接口 http://0.0.0.0:8888/v1/portrait/query/server
凑活着试试看, 记得修改app/config/app_config.py文件中部分配置域名信息
POST 请求内容
```json
{
    "endpoint": "endpoint.a",
    "group": "mysql"
}
```
HEADER
```json
{"X-Token": "随便加一个token就行"}
```

API: GET /v1/portrait/ 实验是否可以正常访问