from rest_framework.authentication import BaseAuthentication
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from jwt import exceptions
import jwt

from django.conf import settings



class JwtQueryParamsAuthentication(BaseAuthentication):
    def authenticate(self, request):
        # 获取token
        # 1.切割
        # 2.解密第二段，判断是否国企
        # 3.验证第三段合法性
        token = request.query_params.get('token') #
        SALT = settings.SECRET_KEY
        try:
            payload = jwt.decode(token, SALT, True)  # True 使用集成的时间等字段校验
        except exceptions.ExpiredSignatureError:
            msg = 'token已失效'
            raise AuthenticationFailed({'code':400,'error':msg})
        except jwt.DecodeError:
            msg = 'token认证失败'
            raise AuthenticationFailed({'code': 400, 'error': msg})
        except jwt.InvalidTokenError:
            msg = '非法的token'
            raise AuthenticationFailed({'code': 400, 'error': msg})
        # 3种返回值
        # 1.抛出异常后，后面的代码都不会执行了
        # 2.return 元组（1,2） 认证通过， 在views中调用 request.user = 第一个元素， request.auth = 第二个值
        # 3.None, 等待下一次认证，不用管
        # if not payload:
        #     return Response({'code': 2001, 'error': msg})
        print('payload: ', payload)
        return (payload,token) # 1=request.user