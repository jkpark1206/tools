import requests
from common.session_init import Session_init
from common.api_demo import ApiDefine
from common.Md5_data import Get_file_md5
from config.config import local_config
import os
import csv
import json


import os
import csv
l=[]
#1、修改此处的文件路径即可
for filename in os.listdir(r'F:\\易识\\网关、采集器固件（含内蒙古电力项目）\\内蒙古电科项目客户提供\\安全测试用固件汇总'):
    l.append('F:\\易识\\网关、采集器固件（含内蒙古电力项目）\\内蒙古电科项目客户提供\\安全测试用固件汇总\\'+filename)

#基准测试固件路径
# for filename in os.listdir(r'C:\\Users\\Administrator\\Desktop\\gujianhuizong\\jizhunceshi'):
#     l.append('C:\\Users\\Administrator\\Desktop\\gujianhuizong\\jizhunceshi\\'+filename)

#
f=open("firmware.csv","w",encoding='utf-8')
for line in l:
    f.write(line+'\n')
f.close()

class Upload_all_firmware(Session_init):
    def test_csv_file(self):
        plugin = '''["cwe_checker","software_components","cve_lookup","crypto_hints","elf_analysis","ip_and_uri_finder","users_and_passwords","elf_checksec"]'''
        # plugin = '''["software_components","cve_lookup","file_type","cpu_architecture","binwalk","crypto_hints","file_hashes","elf_analysis","ip_and_uri_finder","users_and_passwords","elf_checksec","cwe_checker"]'''
        firmware_file = 'C:\\yishi_2\\自动化测试\\ys_api_wwh\\firmware.csv'   #2、修改此处固件csv文件路径
        fp = open(firmware_file, 'r', encoding='utf-8')
        c_data = csv.reader(fp)
        data = []
        for i in c_data:
            data.append(i)
        fp.close()
        try:
            for n in range(0, len(data)):
                firm_path = data[n][0]
                file_md5 = Get_file_md5(os.path.join(firm_path))
                token = ApiDefine().Get_token(self.session)
                task_name = firm_path.split('\\')[-1]
                h = {"Authorization": token}
                d = {"device_name" :task_name,
                    "task_name" :task_name,
                    "vendor": 'all',
                    "version": 'all',
                    "plugin" : plugin,
                    "file_md5": file_md5,
                    "task_lib_tag" :"false"
                        }
                file = open(firm_path ,'rb')
                f = {'firmware' :file}
                res = ApiDefine().Create_task(self.session, d, h, f)
                file.close()
                task_id = json.loads(res)["data"]["id"]
                d2 = {"task_id":task_id}
                res2 = ApiDefine().Start_task(self.session,d2,h)
                print(d2,res2)
        except Exception as e:
            print(e)

Upload_all_firmware().test_csv_file()

# def test_creat_task_01(self):
#     self._testMethodName = 'case_01'
#     self._testMethodDoc = "全选插件上传固件任务"

