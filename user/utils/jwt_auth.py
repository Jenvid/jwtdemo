import jwt,datetime

from django.conf import settings

def create_token(payload,timeout=1):
    SALT = settings.SECRET_KEY
    # 通过jwt生成token
    # 构造header，不写表示使用默认
    headers = {
        'typ': 'JWT',
        'alg': 'HS256'
    }
    # 构造payload
    payload['exp'] = datetime.datetime.utcnow() + datetime.timedelta(minutes=timeout)  # 超时时间
    token = jwt.encode(payload=payload, key=SALT, algorithm="HS256", headers=headers).decode('utf-8')
    return token