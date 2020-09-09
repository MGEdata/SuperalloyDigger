# -*- coding: utf-8 -*-
"""
Created on Wed Jun 10 12:04:34 2020

@author: 35732
"""
# 下载纯文本和xml
import requests
import xlrd
import xlwt


class Article_archive_doi:
    def __init__(self, header, filename, url_publisher, APIKey, arformat, path, text_outpath):
        self.filename = filename
        self.url_publisher = url_publisher
        self.APIKey = APIKey
        self.arformat = arformat
        self.path = path
        self.header = header
        self.out_path = text_outpath

    def data_totxt(self, sample, path):
        f = open(path, 'w', encoding='utf-8')
        f.write(sample)
        f.close()

    def httprequest(self):
        xls = xlwt.Workbook()
        sheet = xls.add_sheet("doi-text_path")
        data = xlrd.open_workbook(self.filename)
        table = data.sheet_by_index(0)
        # 输出为数组的形式，好像只能指定某一行输出
        list_values = []
        #        end = table.nrows
        for x in range(1, len(table.col_values(1))):  # 默认从第2行第2列往下进行
            values = []
            row = table.row_values(x)
            values.append(row[1])
            list_values.append(values)
        dois = list_values
        print(dois)
        count = len(dois)
        for i in range(0, count):
            url = self.url_publisher + dois[i][0] + "?" + self.APIKey + "&httpAccept=" + self.arformat
            r = requests.get(url, headers=self.header)
            content = r.content.decode()
            print(self.path)
            path = self.path + '/' + str(i) + '.txt'
            print(path)
            self.data_totxt(content, path)
            # 将输出路径对应写在源文件doi后边
            sheet.write(i, 0, dois[i][0])
            sheet.write(i, 1, path)
        xls.save(self.out_path)
