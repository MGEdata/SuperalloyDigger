# -*- coding: utf-8 -*-
"""
Created on Wed Jan 20 14:49:42 2021

@author: win
"""
from table_info_get import Get_tinfo_from_html

if __name__ == '__main__':

    html_path = r'E:\文本挖掘\工作二-工艺参数\合金领域所有语料汇总\superalloy_html_parse\原html文件\ASME_download'

    output_path = r'C:\Users\win\Desktop\springer_out_test'

    get_table = Get_tinfo_from_html(html_path, output_path)
    get_table.run()
