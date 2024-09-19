import os

def find_files(folder, extension,n1,n2):
    file_list = []
    for root, dirs, files in os.walk(folder):
        for file in files:
            if file.endswith(extension):
                file_list.append(os.path.join(root, file))
    return file_list[n1:n2]

floder = "E:\\易识\\网关、采集器固件（含内蒙古电力项目）"
ex = ".hex"
print(find_files(floder,ex,0,2))

# 导入os模块
import os

# path定义要获取的文件名称的目录
path = "C:/Users/anban/Desktop/固件适配类型/DD-WRT"

# os.listdir()方法获取文件夹名字，返回数组
file_name_list = os.listdir(path)

# 转为转为字符串
file_name = str(file_name_list)


# replace替换"["、"]"、" "、"'"
file_name = file_name.replace("[", "").replace("]", "").replace("'", "").replace(",", "\n").replace(" ", "")

# # 创建并打开文件list.txt
f = open("C:\\Tools\\UI_firmware_upload\\" + "文件list.csv", "a")


# # 将文件下名称写入到"文件list.txt"
firm_list=f.write(file_name)
#
print(file_name_list[0])