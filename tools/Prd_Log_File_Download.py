import requests
from jsonpath import jsonpath
import datetime
from zipfile import ZipFile
from io import BytesIO
import os
import logging



base_url = 'http://jump.cosec.tech:58012/'
login_datas = {"username": 'wwh',
                "password": '126cfbcd4d16ae6d25c9bfcae76d8ee4',
                "anban_password": '6b5c557da96612408d2844af0d9f5e5d'}
time = datetime.date.today() - datetime.timedelta(days=1)

def Get_prd_log(user_data):
    session = requests.session()
    headers = {"Content-Type": "application/json"}
    res = session.post('{}api/user/login'.format(base_url), json=user_data, headers=headers)
    token = 'Token ' + jsonpath(res.json(), '$.data.AuthToken')[0]
    h = {'Authorization': token,
         "Content-Type": "application/json"}
    file_path = f'D:\\演示环境日志文件\\{time}'
    isExists = os.path.exists(file_path)
    if not isExists:
        os.makedirs(file_path)
    try:
        sys_datas ={"log_tag":1,
                    "start_time":f"{time} 00:00:00",
                    "end_time":f"{time} 23:59:59"}
        res = session.post(f'{base_url}api/log/exportfile', json=sys_datas, headers=h)
        file = res.content  # 二进制流内的数据
        zipped_data = ZipFile(BytesIO(file))  # 使用ZipFile将二进制流写入zipped_data中
        zipped_data.extractall(f'{file_path}\\{time}syslog')
        user_datas = {
            "log_tag": 2,  # 此字段是系统日志
            "start_time": f"{time} 00:00:00",
            "end_time": f"{time} 23:59:59"
        }
        res = session.post('{}api/log/exportfile'.format(base_url), json=user_datas, headers=h)
        file = res.content  # 二进制流内的数据
        zipped_data = ZipFile(BytesIO(file))  # 使用ZipFile将二进制流写入zipped_data中
        zipped_data.extractall(f'{file_path}\\{time}userlog')
    except Exception as e:
        with open(f'{time}log_download.log', 'a') as file:
            file.write(f"{time}:日志下载失败,失败原因{e}")



if __name__ == '__main__':
    Get_prd_log(login_datas)
