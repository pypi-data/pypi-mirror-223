# encoding: utf-8
"""
@project: djangoModel->import_api
@author: 高栋天
@Email: 1499593644@qq.com
@synopsis: 导入execl
@created_time: 2023/06/25
"""
import datetime
import time

from django.core.cache import cache
from rest_framework.views import APIView
from rest_framework.response import Response

from ..services.execl_service import ExeclService
from ..utils.custom_response import doc_response, excel_response, util_response
from ..utils.custom_tool import request_params_wrapper
from ..utils.user_wrapper import user_authentication_wrapper


class importAPIView(APIView):

    @user_authentication_wrapper
    @request_params_wrapper
    def data_processing(self, *args, request_params=None, **kwargs):
        if request_params is None:
            request_params = {}
        print(request_params)
        execl_service = ExeclService()
        result = execl_service.bind_data_processing(request_params['execl_file'],
                                                    request_params['module'], request_params['group_id'])
        # result = execl_service.bind_data_processing.delay(request_params['execl_file'],
        #                                                   request_params['module'])
        # while not result.ready():
        #     print(result.status)
        #     progress = result.info or cache.get(result.task_id)
        #     print(progress)
        #     time.sleep(1)
        # final_result = result.get()
        # print(final_result)
        return util_response()

    def post(self, request):
        # ========== 二、检查：必填性 ==========
        # 对应postman的Body的key=file，value=上传文件的名称 watermelonhh.jpg
        execl_file = request.FILES.get("execl_file")
        module = request.POST.get("module")
        group_id = request.POST.get('group_id', None)
        execl_service = ExeclService()
        result, err = execl_service.bind_data_processing(execl_file, module, group_id)
        if err is None:
            return util_response(data=result)
        return util_response(err=47767, msg=err)
