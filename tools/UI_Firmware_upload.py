#此脚本用于读取CSV文件中的固件，将固件上传后，开始任务
#前提：该CSV文件已提前写好；
#思考：如何不提前写csv文件，直接将某文件夹下的固件上传，开始任务
    #1、固件过多怎么办
    #2、上传到一半，剩下的怎么传
#解决方法，先用脚本把该文件夹下的所有固件读取到一个文件中，分次手动截取一部分固件上传，下次再接着传剩下的
#任务：再写一个读取文件夹的脚本，写入CSV文件

import time
from selenium.webdriver.common.by import By
import csv
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

#步骤1：将固件上传到易识
#步骤2：将固件用CSV文件读取方式，循环上传所有文件

class upload():#步骤1：定义上传固件方法

    def __init__(self):
        self.driver=webdriver.Chrome()
        self.driver.maximize_window()
        self.driver.implicitly_wait(120)

    #先登录，点击上传任务，上传文件，填写信息
    def firmware_info_input(self, file: object, task_name: object, version: object, firm: object):
        self.driver.get("http://{}".format('192.168.5.253:8011/#/'))
        self.driver.find_element(By.XPATH, '//input[@placeholder="请输入您的账号"]').send_keys('root')
        self.driver.find_element(By.XPATH, '//input[@placeholder="请输入您的密码"]').send_keys('1234567')
        self.driver.find_element(By.CSS_SELECTOR,
                                 '#app > div > div > div.main > div > form > div:nth-child(4) > div > div').click()
        A=(By.XPATH,'//button/span/span')
        WebDriverWait(self.driver, 5).until(EC.text_to_be_present_in_element(A, '添加任务'))
        self.driver.find_element(By.CSS_SELECTOR,
                                 '#app > section > section > main > div > div > div > div:nth-child(1) > div.action-bar > div.ac-bar > div > button > span').click()
        # B = (By.XPATH,'//div[@class="v-modal"]')
        # WebDriverWait(self.driver, 5).until(EC.visibility_of_element_located(B))
        #上传文件
        self.driver.find_element(By.CSS_SELECTOR,
                                 '#app > section > section > main > div > div > div > div:nth-child(2) > div > div.el-dialog__body > form > div > div.el-form-item.require > div > div > div > input').send_keys(file)
        #输入任务名称、版本、厂商
        self.driver.find_element(By.XPATH, '//input[@placeholder="请输入任务名称"]').send_keys(task_name)
        self.driver.find_element(By.XPATH,'//input[@placeholder="请输入版本"]').send_keys(version)
        self.driver.find_element(By.XPATH, '//input[@placeholder="请输入厂商名称"]').send_keys(firm)
        #点击关联，勾选全插件
        self.driver.find_element(By.XPATH,'//*[@id="app"]/section/section/main/div/div/div/div[2]/div/div[2]/form/div/div[2]/div/span[2]/label/span[1]/span').click()
        #等待添加任务按钮 C可点击
        C = (By.XPATH, '//*[@id="app"]/section/section/main/div/div/div/div[2]/div/div[2]/div/div/div/button/span')
        #等待元素可见
        WebDriverWait(self.driver, 5).until(EC.visibility_of_element_located(C))
        #点击添加任务按钮
        self.driver.find_element(By.CSS_SELECTOR,'#app > section > section > main > div > div > div > div:nth-child(2) > div > div.el-dialog__body > div > div > div').click()
        #定位“任务添加成功”元素，等任务添加元素成功，再进行下一步
        task = (By.XPATH,'//*[@class="el-message el-message--success"]')
        #隐式等待20秒，直到添加任务成功元素出现，判断task元素存在，则不再等待
        WebDriverWait(self.driver,20).until(EC.visibility_of_element_located(task))
        #A 为开始按钮，定位到开始按钮，点击开始
        A = self.driver.find_element(By.XPATH,'//*[@id="app"]/section/section/main/div/div/div/div[1]/div[2]/div/div[1]/div[3]/table/tbody/tr[1]/td[8]/div/div')
        A.find_element(By.XPATH,'//*[@id="#icon-play"]').click()
        #等待1S
        time.sleep(1)
        self.driver.quit()

#步骤2：将固件上传（方法1上传解包固件；方法2上传基准测试固件）
def csv_file(): #读取firmware_list1.csv CSV文件，将固件全部上传，以firmware_list1.csv文件为例
    #方法1：每一行只有一个元素
    filename = 'C:/Users/anban/Desktop/gujianhuizong/firmware_list1.csv'
    fp = open(filename, 'r', encoding='utf-8')
    c_data = csv.reader(fp)
    data = []
    #输出每个固件元素为一个列表[['C:\\Users\\anban\\Desktop\\gujianhuizong\\jiebaoceshi\\Acti.lib'],[B],[C]...]
    for i in c_data:
        data.append(i)
    fp.close()
    for n in range(0, len(data)):
        A1 = data[n][0]
        print(A1)
        upload().firmware_info_input(r'{}'.format(A1), '', 'all', '关联固件库')


#上传基准测试固件、解包测试固件
    #方法2：每一行不止一个元素，先读取每一行，再读取每一行的第几列元素：以基准测试固件CSV文件为例
    # filename = 'C:/Users/anban/Desktop/gujianhuizong/jizhunceshi.csv'
    # # data = []
    # with open(filename, 'r', encoding='utf-8') as fp:
    #     reader =csv.reader(fp)
    #     data = [row[1] for row in reader]
    # #循环读取每一个固件，上传任务，调用方法，开始任务
    # for n in range(0, len(data)):
    #     A1 = data[n]
    #     print(A1)
    #     upload().firmware_info_input(r'{}'.format(A1), '', 'all', '关联固件库')

csv_file()

