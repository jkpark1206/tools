#查找文件中的文件，与数据库中已有任务的md5进行匹配，如果数据库中没有该md5,则返回该文件的路径，以便查找上传失败的任务
#需要传入任务的创建时间和文件的路径（通过该文件的md5值去数据库中进行匹配）

import os
import hashlib
import psycopg2
from openpyxl import Workbook
import time



def traverse_folder(path) :
    for file_name in os.listdir(path):#获取当前目录下所有文件和文件夹的名称
        file_path=os.path.join(path,file_name)#将文件名和路径连接起来
        if os.path.isdir(file_path):#判断该路径是否为文件夹
            traverse_folder(file_path)#如果是文件夹,则递归调用该函数
        else:
            l.append(file_path)
    return l


def Excel_Create(data):
    # 创建一个叫wk的excel表格
    wk = Workbook()
    # 选择第一个工作表
    sheet = wk.active
    date = time.strftime("%Y%m%d-%H%M%S",time.localtime())
    for row in data:
        sheet.append(row)
        wk.save('C:\\Users\\anban\\Desktop\\未上传固件{}.xlsx'.format(date))
        wk.close()


#获取文件的md5值
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


#从数据库中查找相同的md5任务
def get_task_md5_sql(md5,create_time):  # 查找ys_firmware_scan_result表中的plugin字段，返回所有基本信息数据
    md5_sql = f"SELECT file_md5 FROM ys_firmware_scan_task where file_md5 like '{md5}' and date(create_time) ='{create_time}'"
    return md5_sql


class Base_Compare_Data:
    def __init__(self, database):
        try:
            self.conn = psycopg2.connect(
                database=database[0], host=database[1], port=database[2], user=database[3], password=database[4])
            self.cur =self.conn.cursor()
        except Exception as e:
            print('ERROR', '数据库连接出错，错误原因{}'.format(e))
            raise Exception('数据库连接出错！！')

    def Not_upload_file(self):
        try:
            for filepath in l:
                file_md5 = Get_file_md5(filepath)
                self.cur.execute(get_task_md5_sql(file_md5, create_time))
                firmware = self.cur.fetchall()
                if len(firmware) == 0:
                    ll = (filepath,)
                    data = list(ll)
                    datas.append(data)
                else:
                    continue
            print(datas)
            Excel_Create(datas)
        except Exception as e:
            print('固件提取数据失败,失败原因：{}'.format(e))



if __name__ == '__main__':
    database = ['ys_yishi', '192.168.5.242', 25432, 'postgres', 123456]
    l = []
    create_time = '2024-04-30'
    datas = []
    traverse_folder('D:\\Downloads\\A_test_cases\\jizhunceshi')
    traverse_folder('H:\\vmshare\\download_firmware\\未知\\120xxXR')
    Base_Compare_Data(database).Not_upload_file()


