import os
import openpyxl

file_path = ['H:\\易识\\路由器固件\\output\\asus',
            'H:\\易识\\路由器固件\\output\\AVM',
            'H:\\易识\\路由器固件\\output\\buffalo',
            'H:\\易识\\路由器固件\\output\\dlink',
            'H:\\易识\\路由器固件\\output\\hikvision',
            'H:\\易识\\路由器固件\\output\\linksys',
            'H:\\易识\\路由器固件\\output\\mercury',
            'H:\\易识\\路由器固件\\output\\mikrotik',
            'H:\\易识\\路由器固件\\output\\netcore',
            'H:\\易识\\路由器固件\\output\\openwrt',
            'H:\\易识\\路由器固件\\output\\qnap',
            'H:\\易识\\路由器固件\\output\\tenda',
            'H:\\易识\\路由器固件\\output\\tenvis',
            'H:\\易识\\路由器固件\\output\\tomato-shibby',
            'H:\\易识\\路由器固件\\output\\tp-link',
            'H:\\易识\\路由器固件\\output\\trendnet',
            'H:\\易识\\路由器固件\\output\\ubiquiti'
             ]

#file_path = ['H:\\易识\\路由器固件\\output\\asus','H:\\易识\\路由器固件\\output\\buffalo']
#excel_file = 'C:\\Users\\anban\\Desktop\\易识\\爬虫固件文件\\linux组件\\含linux组件固件数据记录20240311-155436.xlsx'

excel = openpyxl.load_workbook('C:\\Users\\anban\\Desktop\\易识\\爬虫固件文件\\linux组件\\含linux组件固件数据记录20240311-155436.xlsx')
sheet = excel.worksheets[0]
rows_list = []
for row in sheet.values:
    rows_list.append(row[0])


def count_filenames():
    for i in range(0,len(file_path)):
        directory = file_path[i]
        count = 0
        for root, dirs, files in os.walk(directory):
            count = 0
            for filename in rows_list:
                if filename in files:
                        count += 1
                else:
                    continue
        print(directory,count)


'''
适配器:Adapter
存储器:storage、iSCSI
网关:Gateway
路由器:UniFi、wifi、router、wireless、Unified
照相机:camera、video
交换机:switch、Web Smart、xStack Managed 24-Port 10/100 Stackable
集线器： Connect Hub
网关：UTM
收音机：Radio
中继器：Repeater
其他：4G LTE M2M Modem、Tri-Mode 802 11a/g Access Point、2x10GbE +2x 1GbE Secondary iSCSI SAN Controller for DSN-6510、
'''

'''#适配器
SELECT count(*) FROM "scraper_firmware" where device_class like '%Adapter%';

#存储器
SELECT count(*) FROM "scraper_firmware" where device_class like '%storage%';

#网关
SELECT count(*) FROM "scraper_firmware" where device_class like '%Gateway%';

#路由器
SELECT count(*) FROM "scraper_firmware" where device_class like '%UniFi%' or device_class like '%wifi%' or device_class like '%router%' or device_class like '%wireless%';

#收音机
SELECT count(*) FROM "scraper_firmware" where device_class like '%Radio%';

#中继器
SELECT count(*) FROM "scraper_firmware" where device_class like '%Repeater%';


#摄像机
SELECT count(*) FROM "scraper_firmware" where device_class like '%camera%' or device_class like '%video%';

#交换机
SELECT count(*) FROM "scraper_firmware" where device_class like '%switch%' or device_class like '%Web Smart%' or device_class like '%xStack Managed 24-Port 10/100 Stackable%';

#集线器
SELECT count(*) FROM "scraper_firmware" where device_class like '%Connect Hub%';

#网关
SELECT count(*) FROM "scraper_firmware" where device_class like '%UTM%';'''




if __name__ == '__main__':
    count_filenames()
    # count_filenames()


