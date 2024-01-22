import json

import requests

from common.session_init import Session_init
from common.api_demo import ApiDefine
from common.firmware_files import Upload_files
from config.config import local_config
from common.Md5_data import Get_file_md5
import os
import unittest
from requests import *

import os
from requests_toolbelt import *

file_path = "D:\\mytest\\myfile.rar"
file_name = "myfile.rar"  # 这里为了简化就直接给出文件名了，也可以从文件路径中获取
file_stats = os.stat(file_path)
file_size = file_stats.st_size

# with open(file_path, mode='rb') as f:
#     file_rb = f.read()


# class Create_Task_Test1(Session_init):
#
#     def test_ota_firmware(self):
#         token = ApiDefine().Get_token(self.session)
#         task_name = '全选插件创建tsl6G固件任务'
#         file_md5 = Get_file_md5(os.path.join(local_config.ota_firmware))
#         item = {
#             "device_name" :'tsl6G固件任务',
#             "task_name" :task_name,
#             "vendor": 'all',
#             "version": 'all',
#             "plugin" :'''["software_components","cve_lookup","file_type","cpu_architecture","binwalk","cwe_checker","crypto_hints","file_hashes","elf_analysis","ip_and_uri_finder","users_and_passwords","elf_checksec"]''',
#             "file_md5": file_md5,
#             "task_lib_tag" :"false",
#             'firmware': open(local_config.ota_firmware, 'rb')
#         }
#         temp = MultipartEncoder(item)
#         data = MultipartEncoderMonitor(temp)
#
#         headers = {
#             "Content-Type": temp.content_type
#         }
#
#         response = requests.post(url=url, data=data, headers=headers)
#         return response




class Create_Task_Test(Session_init):

    def test_ota_firmware(self):
        self._testMethodName = '接口上传tsl6G固件'
        self._testMethodDoc = "全选插件上传tsl6G固件任务"
        token = ApiDefine().Get_token(self.session)
        # file_stats = os.stat(os.path.join(local_config.ota_firmware))
        # file_size = file_stats.st_size
        task_name = '全选插件创建tsl6G固件任务'
        file_md5 = Get_file_md5(os.path.join(local_config.ota_firmware))
        print(file_md5)
        h = {"Authorization": token}
        d = {"device_name" :'tsl6G固件任务',
             "task_name" :task_name,
             "vendor": 'all',
             "version": 'all',
             "plugin" :'''["software_components","cve_lookup","file_type","cpu_architecture","binwalk","cwe_checker","crypto_hints","file_hashes","elf_analysis","ip_and_uri_finder","users_and_passwords","elf_checksec"]''',
             "file_md5": file_md5,
             "task_lib_tag" :"false",
             'firmware': open(local_config.ota_firmware, 'rb')
             }
        # f = {'firmware' :open(local_config.ota_firmware ,'rb')}
        temp = MultipartEncoder(d)
        data = MultipartEncoderMonitor(temp)
        res = ApiDefine().Create_task(self.session, data, h)
        print(res)

