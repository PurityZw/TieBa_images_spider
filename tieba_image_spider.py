#!/usr/bin/env python
# -*- coding:utf-8 -*-

import requests
from lxml import etree

class TiebaSpider(object):
    def __init__(self):
        self.base_url = "http://tieba.baidu.com"
        self.headers = {"User-Agent" : "Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko"}
        self.tieba_name = raw_input("请输入贴吧名:")
        self.begin_page = int(raw_input("请输入爬取的起始页:"))
        self.end_page = int(raw_input("请输入爬取的结束页:"))

    def send_request(self, url, query = {}):
        """
            发送请求，返回响应
            url : 需要发送请求的url地址
            query: 查询字符串的数据
        """
        response = requests.get(url, params = query, headers = self.headers)
        return response

    def parse_page(self, response):
        """
            提取帖子列表页的每个帖子的链接，并返回链接
            response：每个帖子的响应
        """
        html = response.content
        #print len(html)
        html_obj = etree.HTML(html)
        link_list = html_obj.xpath("//a[@class='j_th_tit ']/@href")
        return link_list

    def parse_image(self, response):
        """
            提取每个帖子里每个图片的链接，并返回链接
        """
        html = response.content
        html_obj = etree.HTML(html)
        link_list = html_obj.xpath("//img[@class='BDE_Image']/@src")
        return link_list


    def write_image(self, response, filename):
        """
            将图片数据写入磁盘文件
        """
        print "[Info]: 正在保存图片" + filename
        with open('./images/' + filename, "wb") as f:
            f.write(response.content)

    def main(self):
        for page in range(self.begin_page, self.end_page + 1):
            pn = (page - 1) * 50
            query_data = {"kw" : self.tieba_name, "pn" : pn}
            url = self.base_url + "/f?"
            try:
                # 1. 每个帖子列表页的请求处理
                response = self.send_request(url, query_data)

                # 2. 每个帖子的请求处理
                page_link_list = self.parse_page(response)
                for link in page_link_list:
                    url = self.base_url + link

                    try:
                        response = self.send_request(url)
                        image_link_list = self.parse_image(response)

                        # 3. 每个图片的请求处理
                        for link in image_link_list:
                            response = self.send_request(link)

                            try:
                                self.write_image(response, link[-15:])
                            except:
                                print "[Error]：图片解析失败" + link
                    except:
                        print "[Error]: 帖子解析失败" + url
            except Exception as e:
                print "[Error]: 帖子列表页解析失败.."
                print e
        print "[Info]: 图片下载结束，谢谢使用!"

if __name__ == "__main__":
    spider = TiebaSpider()
    spider.main()
