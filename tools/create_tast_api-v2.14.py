# -- coding: utf-8 --**
import time
import requests
from jsonpath import jsonpath
import os
import hashlib
import json
import logging





##3、读取文件夹下所有文件，查到是目录则继续遍历，直到读取完该目录下所有的文件，返回所有文件路径
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
            hash_value = md5obj.hexdigest()   #hexdigest()返回十六进制字符串  digest()则返回的是二进制字符串
            return hash_value
    except Exception as e:
        print('ERROR', f'获取文件{file_path}md5值出错,原因{e}')
        return False


# 配置日志记录器
logging.basicConfig(filename='app.log', level=logging.INFO)
logger = logging.getLogger()

date = time.strftime("%Y%m%d-%H%M%S",time.localtime())

def save_logs(log):
    try:
        # 将日志写入文件中
        with open('upload{}.log'.format(date), 'a') as file:
            file.write(f"{log}\n")
    except Exception as e:
        logger.error(f"无法保存日志至文件：{e}")


class Upload_firmware:
    def __init__(self):
        self.session = requests.session()
        data = {"username": 'wwh',
                "password": '126cfbcd4d16ae6d25c9bfcae76d8ee4',
                "anban_password":'6b5c557da96612408d2844af0d9f5e5d' }
        headers = {"Content-Type": "application/json"}
        res = self.session.post('{}api/user/login'.format(URL), json=data, headers=headers)
        self.token = 'Token ' + jsonpath(res.json(), '$.data.AuthToken')[0]
        print(self.token)
    def Create_firmtask(self):
        try:
            for firm_path in l:
                file_md5 = Get_file_md5(os.path.join(firm_path))
                h = {"Authorization": self.token}
                for strategy_id in strategy_id_list:
                    d = {
                        "file_md5":file_md5,
                        "strategy_id":strategy_id,
                        "project_id":project_id,
                        "start":"false"
                        }
                    with open(firm_path, 'rb') as file:
                        f = {'firmware': file}
                        res2 = self.session.post('{}api/task/create'.format(URL),data= d,headers=h,files=f)
                        res_2_code = json.loads(res2.text)["code"]
                        if res_2_code != 200:
                            save_logs(firm_path)
                            save_logs(strategy_id)
                            print(res2.text)
                            save_logs(json.loads(res2.text))
                            continue
                        else:
                            task_id = json.loads(res2.text)["data"]["id"]
                            d2 = {"task_id": task_id}
                            res3 = self.session.put('{}api/task/start'.format(URL), json=d2, headers=h)
                            save_logs(firm_path)
                            print(res3.text)
                            save_logs(res3.text)
        except Exception as e:
            save_logs(e)


if __name__ == '__main__':
    URL ='http://192.168.1.186:8011/'
    strategy_id_list = [80]
    project_id = 38
    l = []
    traverse_folder('D:\\Downloads\\A_test_cases\\binary-samples')
    Upload_firmware().Create_firmtask()