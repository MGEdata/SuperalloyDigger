# -*- coding: utf-8 -*-
"""
Created on Mon May 18 09:13:02 2020

@author: 35732
"""

from text_with_table import Acquire_all_target_info

if __name__ == '__main__':
    # get table content and full text, and dependency parsing

    # the path of configuration file
    c_path = r'dictionary.ini'

    # the path of folder contains txt files
    origin_text_path = r'...\all_txt_folder'

    # target property
    prop_list = ['solvus']

    # the path of folder contains excel files
    excels_path = r'...\all_table_folder'

    # the path of folder to store excels files that have been output
    out_path = r'...\output_folder'

    acquire_all_target_info = Acquire_all_target_info(c_path, origin_text_path, prop_list, excels_path, out_path)
    acquire_all_target_info.run()
