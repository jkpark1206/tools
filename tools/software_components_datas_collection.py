import psycopg2
import os
import hashlib
import json
from openpyxl import Workbook
import time


database = ['ys_yishi','192.168.1.186',25432,'postgres',123456]
plugin = '''["soft", "cve", "cwe", "security", "baseline", "compliance", "sensitive", "pwd"]'''
filepath = 'C:\\Users\\anban\\Desktop\\gujianhuizong'
l = []
soft_versions = []
datas = []
file_hash_list = []


def get_plugin_sql(plugin, hash):  # 查找ys_firmware_scan_result表中的plugin字段，返回所有基本信息数据
    plugin_sql = f"SELECT r.plugin FROM ys_firmware_scan_result r , ys_firmware_scan_task t where r.task_id=t.id and t.is_delete='f' and t.file_md5='{hash}' and t.plugin='{plugin}'  ORDER BY t.end_time desc limit 1"
    return plugin_sql


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


def Excel_Create(data):
    # 创建一个叫wk的excel表格
    wk = Workbook()
    # 选择第一个工作表
    sheet = wk.active
    date = time.strftime("%Y%m%d-%H%M%S",time.localtime())
    for row in data:
        sheet.append(row)
    wk.save('C:\\Users\\anban\\Desktop\\含linux组件固件数据记录{}.xlsx'.format(date))
    wk.close()


def find_elements_with_field(data_list, field):
    return [item for item in data_list if field in item]


def get_soft_datas():
    try:
        for i in traverse_folder(filepath):
            firmname = i.split('\\')[-1]
            file_hash = Get_file_md5(i)


            conn = psycopg2.connect(
                database=database[0], host=database[1], port=database[2], user=database[3], password=database[4])
            cur = conn.cursor()
            cur.execute(get_plugin_sql(plugin, file_hash))
            firmware = cur.fetchall()
            if bool(firmware) is True:
                software_components = json.loads(firmware[0][0])['soft']['summary']  #查找所有文件成分
                if len(software_components) != 0:   #如果存在文件成分
                    soft_version = []
                    for soft in software_components:
                        if soft[0] == 'Linux Kernel':    #判断文件成分是否为'Linux Kernel'
                            soft_datas = soft[0] + soft[1]
                            soft_version.append(soft_datas)
                            soft_versions.append(soft_datas)    #将所有linux组件添加到soft_versions列表中
                    if len(soft_version) != 0 :
                        ll = (firmname, file_hash, str(soft_version)[1:-1])
                        data = list(ll)
                        datas.append(data)
                    else:
                        continue

        # Excel_Create(datas)

    except Exception as e:
        print('固件提取数据失败,失败原因：{}'.format(e))


def soft_version_count(soft_list):
    linux_count = dict()
    print(linux_count)
    for i in soft_list:
        if i in linux_count:
            linux_count[i] += 1
        else:
            linux_count[i] = 1
    print(linux_count)


if __name__ == '__main__':
    # get_soft_datas()
    # soft_version_count(data)
    print(Get_file_md5('C:\\Users\\anban\\Downloads\\ADMIN10_0_0_2_0_10.exe'))
    print(Get_file_md5('H:\\vmshare\\firmware_scraper_wwh\\Avaya\\ADMIN10_0_0_2_0_10.exe'))



