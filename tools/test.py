# import hashlib
#
# file_path = 'H:\\vmshare\\v6.1.2c.tar.gz'
# with open(file_path, 'rb') as f:
#     md5obj = hashlib.md5()
#     md5obj.update(f.read())
#     hash_value = md5obj.hexdigest()
#     print(hash_value)


a = {'Linux Kernel3.18.71': 1, 'Linux Kernel4.4.198': 36, 'Linux Kernel4.1.52': 31, 'Linux Kernel3.18.20': 3, 'Linux Kernel4.19.183': 6, 'Linux Kernel5.4.182': 1, 'Linux Kernel4.4.60': 88, 'Linux Kernel4.9.325': 5, 'Linux Kernel4.1.38': 2, 'Linux Kernel4.9.198': 2, 'Linux Kernel2.6.32': 90, 'Linux Kernel4.4.271': 25, 'Linux Kernel3.10.107': 25, 'Linux Kernel3.4.11': 14, 'Linux Kernel3.10.73': 5, 'Linux Kernel2.6.28': 2, 'Linux Kernel4.9.279': 3, 'Linux Kernel2.6.39': 3, 'Linux Kernel3.14.26': 24, 'Linux Kernel4.14.206': 1, 'Linux Kernel4.9.276': 2, 'Linux Kernel3.10.49': 1, 'Linux Kernel2.6.36': 161, 'Linux Kernel3.10.102': 1, 'Linux Kernel4.4.25': 1, 'Linux Kernel3.10.90': 23, 'Linux Kernel2.6.30': 12, 'Linux Kernel2.6.34': 5, 'Linux Kernel3.6.5': 28, 'Linux Kernel2.4.27': 10, 'Linux Kernel2.6.21': 57, 'Linux Kernel2.4.20': 29, 'Linux Kernel3.10.20': 24, 'Linux Kernel2.6.31': 108, 'Linux Kernel2.6.14': 34, 'Linux Kernel3.10.70': 3, 'Linux Kernel2.6.22': 299, 'Linux Kernel2.6.19': 17, 'Linux Kernel2.6.18': 11, 'Linux Kernel3.4.35': 3, 'Linux Kernel2.6.16': 3, 'Linux Kernel3.14.43': 7, 'Linux Kernel2.6.15': 20, 'Linux Kernel3.10.14': 7, 'Linux Kernel5.6.3': 2, 'Linux Kernel3.3.5': 2, 'Linux Kernel4.9.129': 27, 'Linux Kernel4.14.90': 4, 'Linux Kernel4.9.206': 4, 'Linux Kernel3.0.8': 3, 'Linux Kernel4.9.37': 3, 'Linux Kernel4.4.52': 20, 'Linux Kernel3.10.12': 2, 'Linux Kernel2.4.37': 21, 'Linux Kernel4.4.4': 1, 'Linux Kernel1.1.0': 28, 'Linux Kernel4.19.151': 9, 'Linux Kernel5.4.164': 6, 'Linux Kernel4.9.84': 4, 'Linux Kernel4.19.91': 6, 'Linux Kernel5.4.203': 1, 'Linux Kernel2.4.19': 3, 'Linux Kernel3.3.8': 9, 'Linux Kernel3.10.108': 10, 'Linux Kernel3.4.0': 4, 'Linux Kernel3.10.104': 1, 'Linux Kernel4.1.51': 6, 'Linux Kernel5.4.124': 6, 'Linux Kernel3.14.77': 14, 'Linux Kernel4.14.117': 1, 'Linux Kernel5.15.137': 2560, 'Linux Kernel5.10.201': 2387, 'Linux Kernel3.10.0': 9, 'Linux Kernel3.10.39': 7, 'Linux Kernel3.2.40': 2, 'Linux Kernel4.1.27': 2, 'Linux Kernel3.4.103': 4, 'Linux Kernel4.4.146': 2, 'Linux Kernel2.6.35': 2, 'Linux Kernel1.3.1': 2, 'Linux Kernel4.1.25': 1, 'Linux Kernel3.4.6': 36, 'Linux Kernel4.2.8': 6, 'Linux Kernel4.4.153': 115, 'Linux Kernel3.18.24': 36, 'Linux Kernel4.9.241': 8, 'Linux Kernel3.14.65': 21, 'Linux Kernel5.4.213': 1, 'Linux Kernel4.14.4': 8, 'Linux Kernel4.19.68': 5, 'Linux Kernel4.14.0': 8, 'Linux Kernel4.9.79': 27, 'Linux Kernel4.14.115': 6, 'Linux Kernel4.9.58': 8, 'Linux Kernel4.9.65': 19, 'Linux Kernel4.14.54': 7, 'Linux Kernel4.19.152': 2, 'Linux Kernel4.4.241': 11, 'Linux Kernel4.1.37': 9, 'Linux Kernel4.9.182': 7, 'Linux Kernel4.1.16': 5, 'Linux Kernel2.6.33': 7, 'Linux Kernel4.4.169': 7, 'Linux Kernel3.18.44': 3, 'Linux Kernel2.6.38': 4, 'Linux Kernel4.4.302': 1, 'Linux Kernel4.4.115': 1, 'Linux Kernel3.18.21': 1}


def find_values_starting_with(dictionary, prefix):
    return [value for key, value in dictionary.items() if key.startswith(prefix)]

# values_starting_with_a = find_values_starting_with(a, 'Linux Kernel6')
# print(sum(values_starting_with_a))


# print(sum(a.values()))

linux1 = 30  #(0.45 GB)
linux2 = 898  #(22 GB)
linux3 = 333  #(93.1 GB)
linux4 = 552   #(216.4 GB)
linux5 = 4964   #(168.7 GB)
linux6 = 0   #(48.8 GB)

values_starting_with_a = find_values_starting_with(a, 'Linux Kernel2')
# print(values_starting_with_a)


#
import os
from openpyxl import Workbook
import time
l = [['文件路径'],]
path = 'H:\\download\\FW'

def Excel_Create(data):
    # 创建一个叫wk的excel表格
    wk = Workbook()
    # 选择第一个工作表
    sheet = wk.active
    date = time.strftime("%Y%m%d-%H%M%S",time.localtime())
    for row in data:
        sheet.append(row)
    wk.save('C:\\Users\\anban\\Desktop\\固件路径{}.xlsx'.format(date))
    wk.close()

def traverse_folder(path) :
    for file_name in os.listdir(path):#获取当前目录下所有文件和文件夹的名称
        file_path=os.path.join(path,file_name)#将文件名和路径连接起来
        if os.path.isdir(file_path):#判断该路径是否为文件夹
            traverse_folder(file_path)#如果是文件夹,则递归调用该函数
        else:
            ll = (file_path,)
            data = list(ll)
            l.append(data)
    return l


# Excel_Create(traverse_folder(path))

# import requests
#
# s = requests.Session()
# url = 'https://cios.dhitechnical.com/Brocade/HP%20Firmware/v5.1.0.zip'
# download_path = 'H:\\vmshare\\download_firmware\\Brocade\\HP Firmware'
# headers = {
#     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
#
#
# def download_firmware():
#     response = s.get(url, headers = headers, timeout=100)
#     print(response.status_code)
#     with open(download_path, 'wb') as f:
#         # 将响应内容写入文件
#         for chunk in response.iter_content(chunk_size=1024):
#             if chunk:
#                 f.write(chunk)
#     print('下载成功')
#
#
# download_firmware()


#2、查找目录下以特定后缀结尾的文件  修改floder和extension（后缀）即可  n限制取文件的个数（n1=0,n2=51,从第1个开始取到第50个文件）
floder = "H:\\vmshare\\download_firmware\\Brocade\\HP Firmware"
extension = ".zip"
n1 = 61
n2 = 81
ll = []


for root, dirs, files in os.walk(floder):
    for file in files:
        if file.endswith(extension):
           ll.append(os.path.join(root, file))
    # l = l[n1:n2]
    # print(ll)

import zipfile


def check_zip_file(zip_paths):
    corrupted_files = []
    for file in zip_paths:
        try:
            with zipfile.ZipFile(file, 'r') as z:
                z.testzip()  # 测试zip文件的完整性
        except Exception as e:
            corrupted_files.append((file, str(e)))
    return corrupted_files

# 使用函数检查zip文件
# print(len(check_zip_file(ll)))

import mimetypes

file_path = "C:\\Users\\anban\\Desktop\\补丁.zip"
mime_type = mimetypes.guess_type(file_path)
print(mime_type[0])

