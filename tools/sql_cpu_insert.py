#向爬虫固件的db文件中插入cpu架构信息
import sqlite3
import csv


conn = sqlite3.connect('H:\\vmshare\\firmwarescrawler\\db.sqlite3')
cursor = conn.cursor()

#爬虫固件插入cve数据
def cve_datas_insert():
    with open('C:\\Users\\anban\\Desktop\\cve.csv','r') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            cve = row[1]
            critical = row[2]
            high = row[3]
            middle = row[4]
            low = row[5]
            unknown = row[6]
            hash = row[0]
            try:
                update_query = f"UPDATE scraper_firmware SET cve=? ,critical=?, high=? , middle=?, low=?, unknown=? WHERE url_hash=?"
                values = (cve,critical,high,middle,low,unknown,hash)   #放两个问号代表的值

                cursor.execute(update_query,values)
                conn.commit()
            except Exception as e:
                print("Error updating database:", str(e))


#插入cpu数据
def cpu_datas_insert():
    with open('C:\\Users\\anban\\Desktop\\cpu_datas.csv','r') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            cpu = row[1]
            hash = row[0]
            try:
                update_query = f"UPDATE scraper_firmware SET cpu_type=?  WHERE url_hash=?"
                values = (cpu,hash)   #放两个问号代表的值

                cursor.execute(update_query,values)
                conn.commit()
            except Exception as e:
                print("Error updating database:", str(e))


#插入文件成分数据
def soft_datas_insert():
    with open('C:\\Users\\anban\\Desktop\\linux_datas.csv','r') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            soft = row[1]
            hash = row[0]
            try:
                update_query = f"UPDATE scraper_firmware SET software_components=?  WHERE url_hash=?"
                values = (soft,hash)   #放两个问号代表的值

                cursor.execute(update_query,values)
                conn.commit()
            except Exception as e:
                print("Error updating database:", str(e))


if __name__=='__main__':
    cve_datas_insert()