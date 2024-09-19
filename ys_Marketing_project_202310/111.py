#print('{"code":200,"data":["\u56fa\u4ef6\uff1a\u534e\u4e3a\u8def\u7531\u5668 .bin \u683c\u5f0f\u4e0d\u652f\u6301"],"message":"OK"}'.encode().decode())

import hashlib
import os


email1 = 'jackiepar.k.1206@gmail.com'
def Get_file_md5(email):
    try:
        md5obj = hashlib.md5()
        a = email.encode()
        md5obj.update(a)
        hash_value = md5obj.hexdigest()
        print(hash_value)
    except Exception as e:
        print('ERROR',e)

firm_path = 'C:\\Users\\anban\\Desktop\\gujianhuizong\\jizhunceshi\\Kylin_FT.zip'
file_size = os.path.getsize(firm_path)/ 1024 / 1024
if file_size < 500:  # 过滤超过500M的固件，需要上传500M以上的固件，反之即可
    print(file_size,'MB')
else:
    print('No')


# if __name__ == '__main__':
#     Get_file_md5(email1)