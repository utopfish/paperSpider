# -*- coding=utf-8 -*-
#@author:liuAmon
#@contact:utopfish@163.com
#@file:pdfScrapy.py
#@time: 2019/6/20 9:19
import scrapy
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from exceptions_robot_SEO import NOTUSABLEEXCEPTION
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from multiprocessing import Pool
from scrapy import Request
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import WebDriverException
from exceptions_robot_SEO import NOTUSABLEEXCEPTION, INITDRIVEREXCEPTION, GETPAGEERROR, ROBOTSEOEXCEPTION
import requests
import multiprocessing
import time
from bs4 import BeautifulSoup
# import selenium
from pdfSearch.items import PdfsearchItem
class pdfScrapy(scrapy.Spider):
    name = 'pdfScrapy'
    # allowed_domains = ['xs.glgoo.top']

    #百度学术爬虫参数部分
    word="morphological"#关键字
    pn="0"#分页请求号，0为第一页，10为第二页
    tn="duxueshu_c1gjeupa"#未知参数
    ie="utf-8"#编码格式
    sc_f_para="sc_tasktype%3D%7BfirstSimpleSearch%7D"#搜索类型简单搜索
    sc_hit="1"#未知参数
    sort="sc_time"#搜索结果排序方式
    start_urls = ['http://xueshu.baidu.com/s?wd={}&pn={}&tn=SE_baiduxueshu_c1gjeupa&sc_f_para={}&sc_hit=1&ie=utf-8&sort=sc_time']
    def start_requests(self):
        for i in range(10):
            yield Request(url=self.start_urls[0].format(self.word,i*10,self.sc_f_para))

    def parse(self, response):
        node_list = response.css("div#bdxs_result_lists div.result")
        for node in node_list:
            pdfName="".join(node.css("h3.t a *::text").extract())

            saveList=node.css("p.saveurl::text").extract()
            print("论文名为"+pdfName)
            for url in saveList:
                print(url)
            item = PdfsearchItem()

class researchgate(scrapy.Spider):
    name="researchgate"
    word="morphological"

    def start_requests(self):
        for i in range(10):
            yield Request(url="https://www.researchgate.net/search/publications?q={}&page={}".format(self.word, i))


    def parse(self, response):
        info=response.css("div.indent-left div.nova-c-card__body div.nova-e-text a.nova-e-link")
        for i in info:
            print(i.extract())
        print(response.text)

class DownloadRobot:


    def __init__(self, host,  proxy_ip=None):
        """
        初始化机器人参数
        :param host:搜索下载的网址(网站下载页面)
        :param proxy_ip:设置的代理IP(无代理IP传入None)
        """
        self.driver = None
        self.host = host
        self.proxy_ip = proxy_ip
        self.init_chrome()  # 初始化浏览器参数

    def init_chrome(self):
        """
            初始化driver
        """
        try:
            chromeOptions = Options()
            # chromeOptions.add_argument('--headless')
            # chromeOptions.add_argument('--disable-gpu')
            # chromeOptions.add_argument("window-size=1024,768")
            # chromeOptions.add_argument("--no-sandbox")

        except WebDriverException:
            raise INITDRIVEREXCEPTION()
        # 设置代理IP
        if self.proxy_ip:
            chromeOptions.add_argument("--proxy-server=http://{}".format(self.proxy_ip))  # 设置代理

        # 设置不加载图片
        prefs = {"profile.managed_default_content_settings.images": 2}
        chromeOptions.add_experimental_option('prefs', prefs)

        # 启动driver
        self.driver = webdriver.Chrome(chrome_options=chromeOptions)
        # self.driver.maximize_window()


    def get_result_page(self):
        """
            进入下载界面
        """
        # 获取搜索引擎首页页面
        self.driver.set_page_load_timeout(100)
        try:
            self.driver.get(self.host)
        except GETPAGEERROR as e:
            e.msg = '获取下载节面失败'
            self.driver.execute_script("window.stop()")
            raise e
    def download(self):
        time.sleep(5)
        try:
            te=self.driver.find_elements_by_css_selector("button.nova-c-button span.nova-c-button__label")
            for i in te:
                if i.text=="Download full-text PDF":
                    i.click()
                    break
            self.driver.find_elements_by_css_selector("button.nova-c-button").click()
            time.sleep(2)
        except:
            print("点击下载出错")
        finally:
            self.driver.close()
    def get_download_url(self):
        time.sleep(5)
        content = self.driver.page_source.encode('utf-8')
        soup = BeautifulSoup(content, 'lxml')
        for i in soup.select("a.nova-e-link "):
            if "publication" in i.attrs['href']:
                print("https://www.researchgate.net/"+i.attrs['href'])
                robot=DownloadRobot("https://www.researchgate.net/"+i.attrs['href'])
                robot.get_result_page()
                robot.download()
def main(numer):
    print(numer)
    for i in range(30):
        url="https://www.researchgate.net/search/publications?q=morphological&page={}".format(i*5+int(numer))
        try:
            robot=DownloadRobot(url,None)
            robot.get_result_page()
            robot.get_download_url()
        except:
            print("信息读取出错")
from multiprocessing import Process
if __name__=="__main__":
    p = Pool(5)
    process_list = []
    for i in range(5):
        p = Process(target=main,args=("{}".format(i),))
        p.start()
        process_list.append(p)
    print('Waiting for all subprocesses done...')
    for p in process_list:
        p.join()
    print('All subprocesses done.')
