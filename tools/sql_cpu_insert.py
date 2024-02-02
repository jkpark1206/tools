#向爬虫固件的db文件中插入cpu架构信息
import csv
import sqlite3


conn = sqlite3.connect('db_test.sqlite3')
cursor = conn.cursor()
def read_firm_datas():
    with open('C:\\Users\\anban\\Desktop\\新建 文本文档.csv', 'r') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            hash = row[0]
            cpu = row[1]
            try:
                update_query = f"UPDATE scraper_firmware SET cpu_type=? WHERE url_hash=?"
                values = (cpu, hash)   #放两个问号代表的值
                cursor.execute(update_query,values)
                conn.commit()
            except Exception as e:
                print("Error updating database:", str(e))


if __name__=='__main__':
    read_firm_datas()
