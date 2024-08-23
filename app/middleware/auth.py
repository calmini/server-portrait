# 支持对于一些token的鉴权
from fastapi.requests import HTTPConnection
from starlette.authentication import AuthCredentials, AuthenticationBackend, BaseUser, SimpleUser
from starlette.middleware.authentication import AuthenticationMiddleware

# 参考: https://www.cnblogs.com/weiweivip666/p/18041433
class UserAuthenticationBackend(AuthenticationBackend):

    async def authenticate(self, conn: HTTPConnection) -> tuple[AuthCredentials, BaseUser] | None:
        
        # 定义鉴权的方式


        return AuthCredentials(["authenticated"]), SimpleUser(username="admin") # 从接口的token中获取


"""
完了注册鉴权的中间件
>>> from starlette.middleware.authentication import AuthenticationMiddleware
>>> authMiddleware = AuthenticationMiddleware(backend=UserAuthenticationBackend())
>>> # 注册中间件即可
"""
