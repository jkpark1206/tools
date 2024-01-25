# -- coding: utf-8 --**

import requests
from jsonpath import jsonpath
import os
import hashlib
import json


#v2.10敏感信息合并插件
#plugin = '''["software_components","cwe_checker","cve_lookup","crypto_hints","elf_analysis","elf_checksec","sensitive_msg"]'''
#plugin = '''["software_components","cwe_checker"]'''
plugin = '''["soft","cve","encryption","func","security","sensitive_msg","cwe"]'''
#URL ='http://103.79.25.186:38011/'
URL ='http://192.168.1.186:8011/'

l=[]
#1、修改此处的文件路径,读取该路径下所有固件
# for filename in os.listdir(r'C:\\Users\\anban\\Desktop\\gujianhuizong\\xinjiebaoceshi\\fact_extractor_test'):
#     l.append('C:\\Users\\anban\\Desktop\\gujianhuizong\\xinjiebaoceshi\\fact_extractor_test\\'+filename)


# for filename in os.listdir(r'E:\\易识\\固件适配类型\\QNX'):
#     l.append('E:\\易识\\固件适配类型\\QNX\\'+filename)
    #E:\易识\固件适配类型\QNX

# for filename in os.listdir(r'E:\\易识\\网关、采集器固件（含内蒙古电力项目）\\内蒙古电科项目客户提供\\安全测试用固件汇总'):
#    l.append('E:\\易识\\网关、采集器固件（含内蒙古电力项目）\\内蒙古电科项目客户提供\\安全测试用固件汇总\\'+filename)

#2、查找目录下以特定后缀结尾的文件  修改floder和extension（后缀）即可  n限制取文件的个数（n1=0,n2=51,从第1个开始取到第50个文件）
# floder = "E:\\download\\completed"
# extension = ".hex"
# n1 = 61
# n2 = 81
#
# for root, dirs, files in os.walk(floder):
#     for file in files:
#         if file.endswith(extension):
#            l.append(os.path.join(root, file))
#     l = l[n1:n2]


n1 = 7488
n2 = 8200
# 1、修改此处的文件路径,读取该路径下所有固件
for filename in os.listdir(r'H:\\download\\completed'):
    l.append('H:\\download\\completed\\'+filename)
l =l[n1:n2]


#3、读取文件夹下所有文件，查到是目录则继续遍历，直到读取完该目录下所有的文件，返回所有文件路径
# def traverse_folder(path) :
#     for file_name in os.listdir(path):#获取当前目录下所有文件和文件夹的名称
#         file_path=os.path.join(path,file_name)#将文件名和路径连接起来
#         if os.path.isdir(file_path):#判断该路径是否为文件夹
#             traverse_folder(file_path)#如果是文件夹,则递归调用该函数
#         else:
#             l.append(file_path)
#     return l
# traverse_folder('C:\\Users\\anban\\Desktop\\gujianhuizong\\rtos-test-cases')


def Get_file_md5(file_path):
    try:
        with open(file_path,'rb') as f:
            md5obj = hashlib.md5()
            md5obj.update(f.read())
            hash_value = md5obj.hexdigest()
            return hash_value
    except Exception as e:
        print('ERROR', f'获取文件{file_path}md5值出错,原因{e}')
        return False


class Upload_firmware:
    def __init__(self):
        self.session = requests.session()
        data = {"username": 'root',
                "password": 'fcea920f7412b5da7be0cf42b8c93759',
                "anban_password": 'f169d2236b9ba09a2ceb8a5c03581d41'}
        headers = {"Content-Type": "application/json"}
        res = self.session.post('{}api/user/login'.format(URL), json=data, headers=headers)
        self.token = 'Token ' + jsonpath(res.json(), '$.data.AuthToken')[0]

    def Create_firmtask(self):
        try:
            for firm_path in l:
                file_md5 = Get_file_md5(os.path.join(firm_path))
                task_name = firm_path.split('\\')[-1]
                h = {"Authorization": self.token}
                d = {"device_name": task_name,
                     "task_name": task_name,
                     "vendor": 'test',
                     "version": 'test',
                     "plugin": plugin,
                     "file_md5": file_md5,
                     "task_lib_tag": "false"
                     }

                with open(firm_path, 'rb') as file:
                    f = {'firmware': file}
                    res2 = self.session.post('{}api/task/create'.format(URL),data= d,headers=h,files=f)
                    task_id = json.loads(res2.text)["data"]["id"]
                    d2 = {"task_id": task_id}
                    res3 = self.session.put('{}api/task/start'.format(URL), json=d2, headers=h)
                    print(res3.text)
        except Exception as e:
                print(e)



if __name__ == '__main__':
    # path_list = ['H:\\download\\completed']
    # for path in path_list:
    #     traverse_folder(path)
    # traverse_folder('F:\\易识\网关、采集器固件（含内蒙古电力项目）\\内蒙古电科项目客户提供\\上面文件解压后提取的固件汇总')
    Upload_firmware().Create_firmtask()


