# -*- coding: utf-8 -*-
"""
Created on Wed Jun 10 15:06:30 2020

@author: 35732
"""
import os
import xlrd
import xlwt
from log_wp import LogWp
from pre_processor import PreProcessor


class AllAttributes:
    def __init__(self, prop_name, txt_name, text_path, triple_path, out_path, c_path):
        self.txt_name = txt_name
        self.text_path = text_path
        self.triple_path = triple_path
        self.prop_name = prop_name
        self.out_path = out_path
        self.c_path = c_path
        self.log_wp = LogWp()

    def get_toexcel(self):
        xls = xlwt.Workbook()
        sheet = xls.add_sheet("all_attributes")
        sheet.write(0, 0, 'txt_name')
        sheet.write(0, 1, 'Full_text')
        sheet.write(0, 2, 'Target_sentences')
        sheet.write(0, 3, 'alloy')
        sheet.write(0, 4, 'property')
        sheet.write(0, 5, 'value')
        # triples_tuple
        data_triples = xlrd.open_workbook(self.triple_path)
        table_triples = data_triples.sheet_by_index(0)
        for x in range(0, len(table_triples.col_values(0))):
            sheet.write(x + 1, 1, str(table_triples.col_values(0)[x]))
            sheet.write(x + 1, 2, str(table_triples.col_values(1)[x]))
            sheet.write(x + 1, 3, str(table_triples.col_values(2)[x]))
            sheet.write(x + 1, 4, str(table_triples.col_values(3)[x]))
            sheet.write(x + 1, 5, str(table_triples.col_values(4)[x]))
        # txt_name+doi_list
        k = 0
        for i in range(0, len(table_triples.col_values(0))):
            if table_triples.col_values(0)[i]:
                sheet.write(i + 1, 0, str(self.txt_name[0][k]))
                k += 1
        # text + filtered_text_1 + Target sentences
        txt_name = os.listdir(self.text_path)
        process_text = []
        for i in range(0, len(txt_name)):
            file = open(self.text_path + '/' + str(txt_name[i]), 'r', encoding='utf-8')
            sole_text = file.read()
            pre_processor = PreProcessor(sole_text, self.c_path)
            filter_txt = pre_processor.pre_processor()
            path_2 = self.text_path + '/proprecess'
            is_exists = os.path.exists(path_2)
            if is_exists:
                text_path = path_2 + '/' + str(txt_name[i])
                file = open(text_path, 'w', encoding='utf-8')
                file.write(filter_txt)
                process_text.append(text_path)
            else:
                os.makedirs(path_2)
                text_path = path_2 + '/' + txt_name[i]
                file = open(text_path, 'w', encoding='utf-8')
                file.write(filter_txt)
                process_text.append(text_path)
        self.log_wp.excel_save(xls, self.out_path)
