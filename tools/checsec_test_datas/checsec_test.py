import psycopg2
import json
import os
from openpyxl import Workbook
import time

plugin ='''["soft", "cve", "security", "sensitive", "pwd"]'''
l = []
filepath = 'C:\\Users\\anban\\Desktop\\gujianhuizong\\checksec_test_cases\\data'
datas = [['固件', 'RPATH', 'FORTIFY', 'RELRO', 'Stack','NX', 'PIE']]


def Excel_Create(data):
    # 创建一个叫wk的excel表格
    wk = Workbook()
    # 选择第一个工作表
    sheet = wk.active
    date = time.strftime("%Y%m%d-%H%M%S",time.localtime())
    for row in data:
        sheet.append(row)
        wk.save('C:\\Users\\anban\\Desktop\\测试数据记录{}.xlsx'.format(date))
        wk.close()


def get_plugin_sql(filename, plugin):  # 查找ys_firmware_scan_result表中的plugin字段，返回所有基本信息数据
    fw_name = str(filename).strip().replace("'", "''")  # 用replace是为了解决数据中存在单引号的问题
    plugin_sql = f"SELECT r.plugin FROM ys_firmware_scan_result r , ys_firmware_scan_task t where r.task_id=t.id and t.is_delete='f' and t.task_name='{fw_name}' and t.plugin='{plugin}'  ORDER BY t.end_time desc limit 1"
    return plugin_sql


def traverse_folder(path) :
    for file_name in os.listdir(path):#获取当前目录下所有文件和文件夹的名称
        file_path=os.path.join(path,file_name)#将文件名和路径连接起来
        if os.path.isdir(file_path):#判断该路径是否为文件夹
            traverse_folder(file_path)#如果是文件夹,则递归调用该函数
        else:
            l.append(file_path)
    return l

class OperationpostgresBase:
    def __init__(self,database):
        try:
            self.conn = psycopg2.connect(
                database=database[0],host=database[1],port=database[2],user=database[3],password=database[4])
        except Exception as e:
            print('ERROR','数据库连接出错，错误原因{}'.format(e))
            raise Exception('数据库连接出错！！')


class Base_Compare_Data:
    def __init__(self):
        database = ['ys_yishi','192.168.1.186',25432,'postgres',123456]
        self.cur = OperationpostgresBase(database).conn.cursor()  # 连接数据库


    def get_file_type_datas(self):
        try:
            for i in traverse_folder(filepath):
                firmname = i.split('\\')[-1]

                self.cur.execute(get_plugin_sql(firmname,plugin))
                firmware = self.cur.fetchall()
                if bool(firmware) is True:
                    # All_elf_checksec = json.loads(firmware[0][0])['security']['count']
                    a= json.loads(firmware[0][0])['security']['summary'].values()
                    checsec_list = list(a)[0]
                    if 'RPATH' in checsec_list.keys():
                        RPATH = checsec_list['RPATH']['value']
                    else:
                        RPATH = checsec_list['RUNPATH']['value']
                    FORTIFY = checsec_list['FORTIFY']['value']
                    RELRO = checsec_list['RELRO']['value']
                    Stack = checsec_list['Stack']['value']
                    NX = checsec_list['NX']['value']
                    PIE = checsec_list['PIE']['value']
                    ll = (firmname, RPATH, FORTIFY, RELRO, Stack, NX, PIE)
                    data = list(ll)
                    datas.append(data)

                else:
                    continue

                # 把列表的数据加到excel表格中
                Excel_Create(datas)
        except Exception as e:
            print('固件提取数据失败,失败原因：{}'.format(e))


if __name__ == '__main__':
    Base_Compare_Data().get_file_type_datas()
