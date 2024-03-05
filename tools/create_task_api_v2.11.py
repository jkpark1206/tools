# -- coding: utf-8 --**
import time

import requests
from jsonpath import jsonpath
import os
import hashlib
import json


#v2.11 分析策略
URL ='http://192.168.5.242:8011/'

l=[]
# strategy_id_list = [224,225,226,227,228,229,230,233,
#                     234,237,240,241,242,243,
#                     244,245,246,247,248,249,250,251,252,253,
#                     254,255,256,257,258,259,260,261,262,263,
#                     264,265,266,267,268,269,270,271,272,273,274,275]

strategy_id_list = [88]


# n1 = 8200
# n2 = 9076
#1、修改此处的文件路径,读取该路径下所有固件
# for filename in os.listdir(r'H:\\易识\\test_cases\\Vxworks_test_cases'):
#     l.append('H:\\易识\\test_cases\\Vxworks_test_cases\\'+filename)
# l =l[n1:n2]
# print(l)

# for filename in os.listdir(r'E:\\易识\\固件适配类型\\QNX'):
#     l.append('E:\\易识\\固件适配类型\\QNX\\'+filename)
    #E:\易识\固件适配类型\QNX

# for filename in os.listdir(r'C:\\Users\\anban\\Desktop\\gujianhuizong\\vbf_test_cases'):
#    l.append('C:\\Users\\anban\\Desktop\\gujianhuizong\\vbf_test_cases\\'+filename)

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


#3、读取文件夹下所有文件，查到是目录则继续遍历，直到读取完该目录下所有的文件，返回所有文件路径
def traverse_folder(path) :
    for file_name in os.listdir(path):#获取当前目录下所有文件和文件夹的名称
        file_path=os.path.join(path,file_name)#将文件名和路径连接起来
        if os.path.isdir(file_path):#判断该路径是否为文件夹
            traverse_folder(file_path)#如果是文件夹,则递归调用该函数
        else:
            l.append(file_path)
    return l


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
        data = {"username": 'wwh',
                "password": '126cfbcd4d16ae6d25c9bfcae76d8ee4',
                "anban_password": '6b5c557da96612408d2844af0d9f5e5d'}
        headers = {"Content-Type": "application/json"}
        res = self.session.post('{}api/user/login'.format(URL), json=data, headers=headers)
        self.token = 'Token ' + jsonpath(res.json(), '$.data.AuthToken')[0]

    def Create_firmtask(self):
        try:
            for firm_path in l:
                file_md5 = Get_file_md5(os.path.join(firm_path))
                h = {"Authorization": self.token}
                for strategy_id in strategy_id_list:
                    d = {
                        "file_md5":file_md5,
                        "strategy_id":strategy_id
                         }
                    # file_size = os.path.getsize(firm_path) / 1024 / 1024 /1024
                    # if file_size > 5:  # 过滤超过5GB的固件，需要上传5GB以下的固件，反之即可
                    #     continue
                    # else:
                    with open(firm_path, 'rb') as file:
                        f = {'firmware': file}
                        res2 = self.session.post('{}api/task/create'.format(URL),data= d,headers=h,files=f)
                        res_2_code = json.loads(res2.text)["code"]
                        if res_2_code != 200:
                            print(strategy_id,json.loads(res2.text))
                            continue
                        else:
                            task_id = json.loads(res2.text)["data"]["id"]
                            d2 = {"task_id": task_id}
                            res3 = self.session.put('{}api/task/start'.format(URL), json=d2, headers=h)
                            print(res3.text)

        except Exception as e:
                print(e)



if __name__ == '__main__':
#     path_list = ['H:\\download\\completed']
#     for path in path_list:
#         traverse_folder(path)
    traverse_folder('H:\\易识\\路由器固件\\output')
    Upload_firmware().Create_firmtask()


