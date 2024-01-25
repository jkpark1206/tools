print('{"code":3001,"data":{},"message":"\u7b56\u7565\u4e0d\u5b58\u5728"}'.encode().decode())


# import hashlib
#
# def Get_file_md5(file_path):
#     try:
#         with open(file_path,'rb') as f:
#             md5obj = hashlib.md5()
#             md5obj.update(f.read())
#             hash_value = md5obj.hexdigest()
#             return hash_value
#     except Exception as e:
#         print('ERROR', f'获取文件{file_path}md5值出错,原因{e}')
#         return False
#
#
# print(Get_file_md5('C:\\Users\\anban\\Desktop\\gujianhuizong\\配额边界值测试固件\\lighttpd-mod-alias(2.92KB).ipk'))


