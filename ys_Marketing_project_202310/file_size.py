import os
import pandas as pd
import csv


l = []
f = []
#遍历文件夹下所有文件
def traverse_folder(path) :
    for file_name in os.listdir(path):#获取当前目录下所有文件和文件夹的名称
        file_path=os.path.join(path,file_name)#将文件名和路径连接起来
        if os.path.isdir(file_path):#判断该路径是否为文件夹
            traverse_folder(file_path)#如果是文件夹,则递归调用该函数
        else:
            l.append(file_path)
    return l
#修改此处文件路径，读取文件夹下的文件
file_path = "E:\\易识\\固件测试文件"


#收集所有低于500M大小的固件
def firmware_collect():
    for firm_path in traverse_folder(file_path):
        with open(firm_path, 'rb') as file:
            content = file.read()
            file_size = len(content)/1024/1024
            if file_size >500:  #过滤500M以上的固件
                continue
            else:   #将500M以内的固件路径写入CSV文件中
                a = firm_path[-3:]
                if a == 'pdf' or a=='tml':
                    continue
                else:
                    f.append(firm_path)
    # 创建CSV文件
    for row in f:
        with open("C:\\Users\\anban\\Desktop\\marketing\\firmware_path.csv", 'a', encoding='utf8') as name:
            name.write(row + '\n')

if __name__ == '__main__':
    firmware_collect()

