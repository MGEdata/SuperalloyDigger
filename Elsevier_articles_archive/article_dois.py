# -*- coding: utf-8 -*-
"""
Created on Wed Jun 10 12:04:34 2020

@author: wwr
"""

import requests
import xlrd
import xlwt


class ArticleArchiveDoi:
    def __init__(self, header, filename, url_publisher, apikey, arformat, path, text_outpath):
        self.filename = filename
        self.url_publisher = url_publisher
        self.apikey = apikey
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
        list_values = []
        for x in range(1, len(table.col_values(1))):
            values = []
            row = table.row_values(x)
            values.append(row[1])
            list_values.append(values)
        dois = list_values
        print(dois)
        count = len(dois)
        for i in range(0, count):
            url = self.url_publisher + dois[i][0] + "?" + self.apikey + "&httpAccept=" + self.arformat
            r = requests.get(url, headers=self.header)
            content = r.content.decode()
            print(self.path)
            path = self.path + '/' + str(i) + '.txt'
            print(path)
            self.data_totxt(content, path)
            sheet.write(i, 0, dois[i][0])
            sheet.write(i, 1, path)
        xls.save(self.out_path)
