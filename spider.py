#encoding : utf-8
import requests,re,csv,openpyxl
from bs4 import BeautifulSoup
from urllib.parse import urlparse


__author__ = "Alisa"
__copyright__ = "Copyright 2017"



class Spider:

    headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:52.0) Gecko/20100101 Firefox/52.0",
               "Referer": "http://www.xinshipu.com",
               "Host": "www.xinshipu.com"}

    def __init__(self,url,export_type="txt"):
        """初始化函数"""
        self.url = url
        self.links = set()  # 链接去重
        parse_url = urlparse(url)
        self.base_url = "{}://{}".format(parse_url[0],parse_url[1]) #构造基础url
        self.export_type = export_type
        self.export = {
            'txt':self._export_to_txt,
            'csv':self._export_to_csv,
            'excel':self._export_to_excel
        }

    def start(self):
        """启动爬虫"""
        self._extract_links()
        export_func = self.export.get(self.export_type)
        export_func()
        self._extract_links()

    def _extract_links(self):
        """提取链接
        加下划线意思是告诉其他人这两个方法是私有的
        执行方法链的一个部分
        不是给他人调用的，因为他人调用可能方法可能条件不具备
        """
        resp = requests.get(self.url,headers=Spider.headers)

        if resp.status_code == 200:
            html = resp.text
            soup = BeautifulSoup(html,"html.parser")

            container = soup.find(attrs={"class":"detail-cate-list clearfix mt20"})
            links = container.find_all('a')
            for link in links:
                pattern = re.compile('zuofa?')
                if re.findall('\/zuofa\/\d+','{}'.format(link)):

                    self.links.add("{}{}".format(self.base_url,link.attrs['href']))

        # print (self.links)   # 只想提取出来带做法的数据，什么做法大全的，菜谱的不想要

        # self.links.add('http://www.xinshipu.com/zuofa/92183')
        # self.links.add('http://www.xinshipu.com/zuofa/50755')
        # self.links.add('http://www.xinshipu.com/zuofa/83815')


    def _extract_data(self,url):
        """
        提取菜谱数据项
        :param url : 菜谱地址
        :return : 菜谱数据项
        """
        res = requests.get(url,headers=Spider.headers)
        if res.status_code == 200:
            soup = BeautifulSoup(res.text,'html.parser')
            title = soup.find('h1').get_text()  # 菜名
            hits = soup.find(attrs={"class":"cg2 mt12"}).find_all('span')[3].get_text() #阅读次数
            fav = soup.find(attrs={"class":"cg2 mt12"}).find_all('span')[5].get_text() #收藏数量
            return (title,hits,fav)

        return None

    def _export_to_txt(self):
        """
        导出数据到txt文件
        :return:
        """
        for url in self.links:
            with open('txtdata.txt','a+') as f:
                f.write('菜名：{}  阅读数：{}   收藏数：{}'.format(self._extract_data(url)[0],self._extract_data(url)[1],self._extract_data(url)[2]))
                f.write('\n')

    def _export_to_csv(self):
        """
        导出数据到 csv 文件
        :return:
        """
        header = ['菜名','阅读数','收藏数']
        with open('csvdata.csv', 'a+', newline='') as csvheader:
            headerwrite = csv.writer(csvheader)
            headerwrite.writerow(header)

        for url in self.links:
            with open('csvdata.csv','a+',newline='') as csvdata:

                csvwrite = csv.writer(csvdata)
                #创建一个写入器，往csvdata中写入，所以需要传递csvdata
                # 读取器是 reader（） 或者是DictReader（）

                csvwrite.writerow(self._extract_data(url))
                # print ("+"*2)
                # print (self._extract_data(url))

    def _export_to_excel(self):
        """
        导出数据到 excel 文件
        openpyxl围绕着打开Workbook，定位Sheet，操作Cell进行

        :return:
        """

        wb = openpyxl.Workbook()  # 声明工作薄实例
        ws = wb.active  # 激活工作表
        ws.title = "食谱数据"

        ws['A1'] = "菜名"
        ws['B1'] = "阅读数"
        ws['C1'] = "收藏数"


        for i,url in enumerate(self.links):
            ws.cell(row=i+2, column=1, value=self._extract_data(url)[0])
            ws.cell(row=i+2, column=2, value=self._extract_data(url)[1])
            ws.cell(row=i+2, column=3, value=self._extract_data(url)[2])


        wb.save("exceldata.xlsx")

if __name__ == '__main__':
    spider = Spider('http://www.xinshipu.com/%E5%AE%B6%E5%B8%B8%E8%8F%9C.html',export_type='excel')
    spider.start()

    # spider2 = Spider('http://www.xinshipu.com/question')
    # spider2.start()


