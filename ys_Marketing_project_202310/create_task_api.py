# -- coding: utf-8 --**

import requests
import os
import json
from faker import Faker

# v2.10敏感信息合并插件
plugin = '''["software_components","cve_lookup","cwe_checker","crypto_hints","elf_analysis","elf_checksec","sensitive_msg"]'''
# plugin = '''["elf_analysis"]'''


URL = 'http://192.168.5.242:9051/'
l = []
# 'C:\\Users\\anban\\Desktop\\gujianhuizong\\jizhunceshi\\P3A_FW_V01.11.0020.bin.zip'
SBOM_path = 'C:\\yishi_2\\自动化测试\\ys_Marketing_project_202310\\app.bin_2023-10-07111.spdx'


# 3、读取文件夹下所有文件，查到是目录则继续遍历，直到读取完该目录下所有的文件，返回所有文件路径
def traverse_folder(path):
    for file_name in os.listdir(path):  # 获取当前目录下所有文件和文件夹的名称
        file_path = os.path.join(path, file_name)  # 将文件名和路径连接起来
        if os.path.isdir(file_path):  # 判断该路径是否为文件夹
            traverse_folder(file_path)  # 如果是文件夹,则递归调用该函数
        else:
            l.append(file_path)
    return l


traverse_folder('E:\\易识\\固件测试文件')


# E:\易识\固件测试文件\\4-24下载固件
# E:\易识\固件测试文件\2022_1_19新固件
# E:\易识\固件测试文件\2022_1_20工业SCADA系统固件
# E:\易识\固件测试文件\2022_1_20机顶盒固件
#E:\易识\固件测试文件\2022_1_20汽车固件
#E:\易识\固件测试文件\2022_2_10新固件
#E:\易识\固件测试文件\2022_2_14新固件
#E:\易识\固件测试文件\2022_2_15新固件
#E:\易识\固件测试文件\2022_2_16新固件
# E:\易识\固件测试文件\2022_2_17新固件     1
# E:\易识\固件测试文件\2022_2_21新固件      1
# E:\易识\固件测试文件\2022_2_28新固件      1
# E:\易识\固件测试文件\2022_03_08新固件      1
# E:\易识\固件测试文件\2022_07测试固件      1
# E:\易识\固件测试文件\2022_08固件报告      1
# E:\易识\固件测试文件\2022_09新固件     1
# E:\易识\固件测试文件\2022_10新固件     1
# E:\易识\固件测试文件\3022_03_02新固件   1
# E:\易识\固件测试文件\基准测试\测试固件      1
# E:\易识\固件测试文件\客户固件
# E:\易识\固件测试文件\老固件文件\bin
# E:\易识\固件测试文件\老固件文件\fact 固件备份
# E:\易识\固件测试文件\老固件文件\fw_tv-ip110wn_v2(1.2.2.68)
# E:\易识\固件测试文件\老固件文件\Netgear\WNAP320_V3.0.5.0
# E:\易识\固件测试文件\老周提供
# E:\易识\固件测试文件\清华苏研院
# E:\易识\固件测试文件\摄像机_无人机_录像机相关固件     1
# E:\易识\明确存在CVE的固件   1

# email = 'jackiepark1206@gmail.com'
class Upload_firmware:
    def __init__(self):
        self.session = requests.session()
        self.headers = {"Content-Type": "multipart/form-data"}

    def Create_firmtask(self):
        try:
            for firm_path in l:
                fake = Faker()
                email = fake.email()
                d = {"email": email}
                file_size = os.path.getsize(firm_path) / 1024 / 1024
                if file_size > 500:  # 过滤超过500M的固件，需要上传500M以上的固件，反之即可
                    continue
                else:
                    with open(firm_path, 'rb') as file:
                        files = {
                            "sbom": open(SBOM_path, 'rb'),
                            "firmware": file,
                        }
                        res = self.session.post('{}api/task/web_activity/create'.format(URL), data=d, files=files).text
                        print(email, firm_path, res)
        except Exception as e:
            print(e)


if __name__ == '__main__':
    Upload_firmware().Create_firmtask()
