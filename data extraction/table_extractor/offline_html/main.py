# -*- coding: utf-8 -*-
"""
Created on Wed Jan 20 14:49:42 2021

@author: win
"""
from table_info_get import GetTableInfoFromHtml

if __name__ == '__main__':

    html_path = r'...\html_folder'

    output_path = r'...\output_folder'

    get_table = GetTableInfoFromHtml(html_path, output_path)
    get_table.run()
