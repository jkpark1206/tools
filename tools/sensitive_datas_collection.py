from openpyxl import Workbook
import time
import psycopg2
import os
import json


#数据库信息
database = ['ys_yishi','192.168.1.186',25432,'postgres',123456]

plugin = '''["sensitive", "pwd"]'''


#新建表的title
datas = [['测试固件','文件类型','文件数量','CPU架构','敏感信息']]
l = []

filepath = 'H:\\易识\\test_cases\\Vxworks_test_cases'

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


def traverse_folder(path) :
    for file_name in os.listdir(path):#获取当前目录下所有文件和文件夹的名称
        file_path=os.path.join(path,file_name)#将文件名和路径连接起来
        if os.path.isdir(file_path):#判断该路径是否为文件夹
            traverse_folder(file_path)#如果是文件夹,则递归调用该函数
        else:
            l.append(file_path)
    return l


def get_plugin_sql(filename ,plugin):  # 查找ys_firmware_scan_result表中的plugin字段，返回所有基本信息数据
    fw_name = str(filename).strip().replace("'", "''")  # 用replace是为了解决数据中存在单引号的问题
    plugin_sql = f"SELECT r.plugin FROM ys_firmware_scan_result r , ys_firmware_scan_task t where r.task_id=t.id and t.is_delete='f' and t.task_name='{fw_name}' and t.plugin='{plugin}'  ORDER BY t.end_time desc limit 1"
    return plugin_sql

def get_base_data_sql(filename,plugin):
    fw_name = str(filename).strip().replace("'", "''")  # 用replace是为了解决数据中存在单引号的问题
    base_data_sql = f"SELECT r.meta FROM ys_firmware_scan_result r , ys_firmware_scan_task t where r.task_id=t.id and t.is_delete='f' and t.task_name='{fw_name}' and t.plugin='{plugin}' ORDER BY t.end_time desc limit 1"
    return base_data_sql


class Base_Compare_Data:
    def __init__(self, database):
        try:
            self.conn = psycopg2.connect(
                database=database[0], host=database[1], port=database[2], user=database[3], password=database[4])
            self.cur =self.conn.cursor()
        except Exception as e:
            print('ERROR', '数据库连接出错，错误原因{}'.format(e))
            raise Exception('数据库连接出错！！')

    def get_file_type_datas(self):

        try:
            for i in traverse_folder(filepath):
                firmname = i.split('\\')[-1]

                self.cur.execute(get_plugin_sql(firmname, plugin))
                firmware = self.cur.fetchall()

                self.cur.execute(get_base_data_sql(firmname, plugin))
                base_datas = self.cur.fetchall()

                if bool(firmware) is True or bool(base_datas) is True:   #任务存在
                    #提取file_type
                    All_file_type = json.loads(firmware[0][0])['file_type']['summary']
                    file_type = str(All_file_type)[1:-1]

                    # 提取文件解包数量
                    file_type_count = json.loads(base_datas[0][0])['total_files_count']

                    #提取CPU信息
                    All_cpu = json.loads(firmware[0][0])['central']['summary']
                    cpu = str(All_cpu)[1:-1]

                    # 提取敏感信息数据（ip插件+user插件的数量总和）
                    # 获取ip插件中的敏感信息数据
                    ip_uri = json.loads(firmware[0][0])['sensitive']['summary']
                    ip_uri_len = len(list(ip_uri.values()))
                    ip_uri_datas = []
                    if ip_uri_len > 0:
                        for i in range(0, ip_uri_len):
                            ip_uri_s = list(ip_uri.values())[i]["plugin_res"]
                            ip_uri_datas.append(ip_uri_s)
                    else:
                        ip_uri_datas = [0]
                    All_ip_uri = sum(ip_uri_datas)

                    # 获取user插件中的敏感信息数据
                    user_passwd = json.loads(firmware[0][0])['pwd']['summary']
                    user_passwd_len = len(list(user_passwd.values()))
                    user_passwd_datas = []
                    if user_passwd_len > 0:
                        for i in range(0, user_passwd_len):
                            user_passwd_s = list(user_passwd.values())[i]["plugin_res"]
                            user_passwd_datas.append(user_passwd_s)
                    else:
                        user_passwd_datas = [0]
                    All_user_passwd = sum(user_passwd_datas)

                    # 敏感信息数据由ip和user插件的数据相加
                    All_sensetive = All_ip_uri + All_user_passwd
                    #把所有数据放进一个列表中
                    ll = (firmname,file_type,file_type_count,cpu,All_sensetive)
                    data = list(ll)
                    datas.append(data)

                else:
                    ll = (firmname,'','','','')
                    data = list(ll)
                    datas.append(data)

            #把列表的数据加到excel表格中
            Excel_Create(datas)


        except Exception as e:
            print('固件提取数据失败,失败原因：{}'.format(e))


if __name__ == '__main__':
    Base_Compare_Data(database).get_file_type_datas()
