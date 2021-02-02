from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .WechatSendServer import *
import itchat


def wechat_send_controller(request):
    response = {}
    response['code'] = 0
    response['message'] = 'success'
    # POST
    if request.method == 'GET':
        wechat_sendfile_server()

    return JsonResponse(response)
