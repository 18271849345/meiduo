from django.http import HttpResponse

import random

from rest_framework.response import Response
from rest_framework.views import APIView
from django_redis import get_redis_connection
from rest_framework.generics import GenericAPIView
from meiduo_mall.apps.verifications.serializers import ImageCodeCheckSerializer
from meiduo_mall.libs.captcha.captcha import captcha

from . import constants
import logging
from celery_tasks.sms.tasks import send_sms_code


logger=logging.getLogger('django')

# Create your views here.
class ImageCodeView(APIView):
    """图片验证码"""
    def get(self, request, image_code_id):
        # 生成验证码图片
        text, image = captcha.generate_captcha()
        # 保存真实值
        redis_conn = get_redis_connection('verify_codes')
        redis_conn.setex("img_%s" % image_code_id, constants.IMAGE_CODE_REDIS_EXPIRES, text)

        # 返回图片
        return HttpResponse(image, content_type='image/jpg')

class SMSCodeView(GenericAPIView):
    serializer_class = ImageCodeCheckSerializer
    def get(self,request,mobile):

        serializer = self.get_serializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)
        sms_code='%06d' % random.randint(0,9999999)

        redis_conn=get_redis_connection('verify_codes')
        pl=redis_conn.pipeline()
        pl.setex('sms_%s' % mobile,constants.SMS_CODE_REDIS_EXPIRES,sms_code)
        pl.setex('send_flag_%s' % mobile,constants.SEND_SMS_CODE_INTERVAL,1)
        pl.execute()

        #使用celery发送短信验证码
        expires=constants.SMS_CODE_REDIS_EXPIRES//60
        send_sms_code.delay(mobile,sms_code,expires)

        return Response({'message':'ok'})



