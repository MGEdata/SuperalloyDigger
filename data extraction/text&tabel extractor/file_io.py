# -*- coding: utf-8 -*-
"""
Created on Thu May 21 20:09:04 2020

@author: 35732
"""
import xlrd
import xlwt
from log_wp import Log_wp

class File_IO:
    def __init__(self,target_sents,out_path,txt_name):
        self.target_sents = target_sents
        self.out_path = out_path
        self.txt_name = txt_name
        self.log_wp = Log_wp()

    def out_to_excel(self):
        length_sent = len(self.target_sents)
        xls = xlwt.Workbook()
        sht1 = xls.add_sheet("Sheet1")
        for w in range(0,length_sent):
            sht1.write(w,0,str(w)+'.txt')
            if self.target_sents[w] == '{}':
                out = 'no target sentence'
                sht1.write(w,1,out)
            else:
                sht1.write(w,1,self.target_sents[w])
        self.log_wp.excel_save(xls,self.out_path)

    def data_from_excel(self):
        all_data = []
        file = xlrd.open_workbook(self.out_path)
        sheet = file.sheet_by_index(0)
        col_value = sheet.col_values(1)
        k = len(col_value)
        for k in range(0,k):
            unit_data = []
            str_sent = col_value[k]
            if str_sent == 'no target sentence':
                all_data.append([])
            else:
                dict_sent = eval(str_sent)
                for i,sent in dict_sent.items():
                    unit_data.append(sent)
                all_data.append(unit_data)
        return all_data