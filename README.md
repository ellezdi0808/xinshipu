文件用途：爬去新食谱网站的菜谱，菜谱页面点击数，收藏数。

操作实现：

分析新食谱页面，获取菜谱链接，爬取菜谱页面需要的数据。

定义爬虫类，类里面设置爬虫启动start方法。

实现根据传入的页面url，及所要导出的文件类型，将获取的数据导出到需要的文件格式。

目前支持三种导出文件，txt，csv，excel。






