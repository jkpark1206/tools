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