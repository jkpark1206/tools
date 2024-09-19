import os
import hashlib
import psycopg2
from openpyxl import Workbook
import time
from collections import Counter
import json
import requests
from jsonpath import jsonpath


database = ['ys_yishi','192.168.5.242',25432,'postgres',123456]
l = []
create_time = '2024-03-05'
datas = []
plugin = '''["soft", "cve"]'''
URL = 'http://192.168.5.242:8011/'
userdatas = {"username": 'cxh',
            "password": '126cfbcd4d16ae6d25c9bfcae76d8ee4',
            "anban_password": '6b5c557da96612408d2844af0d9f5e5d'}



#从数据库中查找CVE数量
def get_cve_sql(filename, plugin):  # 查找cve数量
    fw_name = str(filename).strip().replace("'", "''")  # 用replace是为了解决数据中存在单引号的问题
    cve_sql = f"SELECT r.cve_count FROM ys_firmware_scan_result r , ys_firmware_scan_task t where r.task_id=t.id and t.is_delete='f' and t.task_name='{fw_name}' and t.plugin='{plugin}' ORDER BY t.end_time desc limit 1"
    return cve_sql

def get_cve_plugin_sql(filename, plugin):  # 查找cve数量
    fw_name = str(filename).strip().replace("'", "''")  # 用replace是为了解决数据中存在单引号的问题
    cve_sql = f"SELECT r.plugin FROM ys_firmware_scan_result r , ys_firmware_scan_task t where r.task_id=t.id and t.is_delete='f' and t.task_name='{fw_name}' and t.plugin='{plugin}' ORDER BY t.end_time desc limit 1"
    return cve_sql

def get_task_id(filename, plugin):  # 查找cve数量
    fw_name = str(filename).strip().replace("'", "''")  # 用replace是为了解决数据中存在单引号的问题
    cve_sql = f"SELECT r.task_id FROM ys_firmware_scan_result r , ys_firmware_scan_task t where r.task_id=t.id and t.is_delete='f' and t.task_name='{fw_name}' and t.plugin='{plugin}' ORDER BY t.end_time desc limit 1"
    return cve_sql


def traverse_folder(path) :
    for file_name in os.listdir(path):#获取当前目录下所有文件和文件夹的名称
        file_path=os.path.join(path,file_name)#将文件名和路径连接起来
        if os.path.isdir(file_path):#判断该路径是否为文件夹
            traverse_folder(file_path)#如果是文件夹,则递归调用该函数
        else:
            l.append(file_path)
    return l


class Base_Compare_Data:
    def __init__(self, database):
        try:
            self.conn = psycopg2.connect(
                database=database[0], host=database[1], port=database[2], user=database[3], password=database[4])
            self.cur =self.conn.cursor()
        except Exception as e:
            print('ERROR', '数据库连接出错，错误原因{}'.format(e))
            raise Exception('数据库连接出错！！')

    def cve_file_count(self):
        cve_all_task = 0
        cve_count_all = 0
        cve_count_super = 0
        cve_count_high = 0
        for i in traverse_folder(filepath):
            firmname = i.split('\\')[-1]
            self.cur.execute(get_cve_sql(firmname, plugin))
            All_cve = self.cur.fetchall()
            if bool(json.loads(All_cve[0][0])) is True:
                cve_alls = json.loads(All_cve[0][0])['all']
                if cve_alls > 0:    #如果任务存在CVE
                    cve_all_task += 1       #那么CVE统计数量+1

                cve_alls = json.loads(All_cve[0][0])['all']    #获取CVE总数
                cve_count_all += cve_alls
                cve_super = json.loads(All_cve[0][0])['super']   #获取超危CVE的数量
                cve_count_super += cve_super
                cve_high = json.loads(All_cve[0][0])['high']  # 获取超危CVE的数量
                cve_count_high += cve_high
        print(f'该厂商中检测出CVE的固件数为：{cve_all_task}\n',
              f'共检测出CVE个数为：{cve_count_all}\n',
              f'其中超危CVE个数为：{cve_count_super}\n',
              f'高危CVE个数为：{cve_count_high}\n')

    def cve_top_20(self):
        self.session = requests.session()
        headers = {"Content-Type": "application/json"}
        res = self.session.post('{}api/user/login'.format(URL), json=userdatas, headers=headers)
        self.token = 'Token ' + jsonpath(res.json(), '$.data.AuthToken')[0]
        h = {"Authorization": self.token}
        cve_id_super_list = []
        cve_id_high_list = []
        for i in traverse_folder(filepath):
            firmname = i.split('\\')[-1]
        # firmname = 'FW_TUF_AX4200_300438832464.zip'
            self.cur.execute(get_task_id(firmname, plugin))
            Task = self.cur.fetchall()
            if len(Task) > 0:
                task_id = Task[0][0]
                d = {"task_id": task_id,
                     "part": "cve"}
                res = self.session.get('{}api/task/report/part'.format(URL), params=d, headers=h)
                cve_datas = list(json.loads(res.text)["data"].values())
                for cve_all in cve_datas:
                    cve_super = list(cve_all.values())[0]['super']   #获取超危CVE数据
                    for super_cve_ids in cve_super:
                        super_cve_id = super_cve_ids["cve_id"]
                        cve_id_super_list.append(super_cve_id)
                    cve_high = list(cve_all.values())[0]['high']  # 获取高危CVE数据
                    for high_cve_ids in cve_high:
                        high_cve_id = high_cve_ids["cve_id"]
                        cve_id_high_list.append(high_cve_id)
        counter = Counter(cve_id_super_list) # 使用max函数找到出现次数最多的元素
        top_elements_super = counter.most_common(20)   #输出出现次数前20的CVE及出现次数(超危CVE)
        print('超危')
        for super_cve_list in top_elements_super:
            super_cve = super_cve_list[0]
            print(super_cve)
        counter = Counter(cve_id_high_list)  # 使用max函数找到出现次数最多的元素
        top_elements_high = counter.most_common(20)  # 输出出现次数前20的CVE及出现次数(高危CVE)
        print('高危')
        for high_cve_list in top_elements_high:
            high_cve = high_cve_list[0]
            print(high_cve)


if __name__ == '__main__':
    filepath = 'H:\\易识\\路由器固件\\output\\ubiquiti'
    Base_Compare_Data(database).cve_top_20()



