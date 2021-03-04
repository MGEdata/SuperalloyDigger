# -*- coding: utf-8 -*-
"""
Created on Wed Jan 20 14:49:42 2021

@author: win
"""

class Log_wp():
    def __init__(self):
        pass
    
    def print_log(self, sentence, *args):
        print(sentence %args)
    
    def write_totxt_log(self, path, content):
        file = open(path, mode='w', encoding="UTF-8")
        file.write(str(content))
        file.close()

    def write_tohtml_log(self, path, content):
        file = open(path, mode='wb', encoding="UTF-8")
        file.write(str(content))

    def excel_writer(self,data, writer, sheet_name):
        data.to_excel(writer, sheet_name = sheet_name, header=None, index=False)

    def excel_save(self, xls, out_path):
        xls.save(out_path)
