import time,uuid
from django.shortcuts import render,HttpResponse
from rest_framework.response import Response
from rest_framework.views import APIView
from user.models import UserInfo
import jwt, datetime
from jwt import exceptions
from django.conf import settings

SALT = settings.SECRET_KEY

class LoginView(APIView):
    def post(self,request,*args,**kwargs):
        user = request.data.get('username')
        pwd = request.data.get('password')
        print(user,pwd)
        user_object = UserInfo.objects.filter(username=user,password=pwd).first()
        print(user_object,type(user_object))

        if not user_object:
            return Response({'code':1000,'error':'用户名密码错误'})
        random_string = str(uuid.uuid4())
        user_object.token = random_string
        user_object.save()
        return Response({'code':1001,'data':random_string})

class OrderView(APIView):
    def get(self,request,*args,**kwargs):
        token = request.query_params.get('token')
        if not token:
            return Response({'code': 2000, 'data': '登录成功后才能访问'})
        user_object = UserInfo.objects.filter(token=token).first()
        if not user_object:
            return Response({'code': 2000, 'data': 'token无效'})
        return Response('订单列表')

class JwtLoginView(APIView):
    def post(self,request,*args,**kwargs):
        user = request.data.get('username')
        pwd = request.data.get('password')
        user_object = UserInfo.objects.filter(username=user,password=pwd).first()

        if not user_object:
            return Response({'code':1000,'error':'用户名密码错误'})
        # 通过jwt生成token

        # 构造header，不写表示使用默认
        headers = {
            'typ': 'JWT',
            'alg': 'HS256'
        }
        # 构造payload
        payload = {
            'user_id': user_object.id,  # 自定义用户ID
            'username': user_object.username,  # 自定义用户名
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=1)  # 超时时间
        }
        token = jwt.encode(payload=payload, key=SALT, algorithm="HS256", headers=headers).decode('utf-8')
        return Response({'code':1001,'data':token})


class JwtOrderView(APIView):
    def get(self, request, *args, **kwargs):
        # 获取token
        token = request.query_params.get('token')
        # 1.切割
        # 2.解密第二段，判断是否国企
        # 3.验证第三段合法性
        payload=None
        msg = None
        try:
            payload = jwt.decode(token, SALT, True)  # True 使用集成的时间等字段校验
        except exceptions.ExpiredSignatureError:
            msg = 'token已失效'
        except jwt.DecodeError:
            msg = 'token认证失败'
        except jwt.InvalidTokenError:
            msg = '非法的token'
        if not payload:
            return Response({'code': 2001, 'error': msg})
        # print('payload: ',payload)
        return Response('订单列表')

from user.extensions.auth import JwtQueryParamsAuthentication
from user.utils.jwt_auth import create_token
class ProLoginView(APIView):
    authentication_classes = [] # 为空表示不应用认证
    def post(self,request,*args,**kwargs):
        user = request.data.get('username')
        pwd = request.data.get('password')
        user_object = UserInfo.objects.filter(username=user,password=pwd).first()

        if not user_object:
            return Response({'code':1000,'error':'用户名密码错误'})
        payload = {
            "id":user_object.id,
            "username":user_object.username
        }
        token = create_token(payload)
        return Response({'code':1001,'data':token})



class ProOrderView(APIView):
    # authentication_classes = [JwtQueryParamsAuthentication,] # 加入 settings 全局配置
    def get(self, request, *args, **kwargs):
        print(request.user)  #  拿到payload的所有信息
        return Response('订单列表')