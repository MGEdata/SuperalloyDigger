# -*- coding: utf-8 -*-
"""
Created on Mon May 18 09:13:02 2020

@author: 35732
"""

from text_with_table import Acquire_all_target_info

if __name__ == '__main__':
    # get table content and full text, and dependency parsing

    # the path of configuration file
    C_path = r'dictionary.ini'

    # the path of folder contains txt files
    origin_text_path = r'E:\文本挖掘\工作二-工艺参数\表格解析\self_try\all_text_outcome\text-out-5000'

    # target property
    prop_list = ['solvus']

    # the path of folder contains excel files
    excels_path = r'E:\文本挖掘\工作二-工艺参数\合金领域所有语料汇总\superalloy_table\table_all'

    # the path of folder to store excels files that have been output
    out_path = r'E:\文本挖掘\工作二-工艺参数\表格解析\self_try\dependency_outcome_1\改动后的数据基础上改原子和质量百分比\2'

    Acquire_all_target_info = Acquire_all_target_info(C_path, origin_text_path, prop_list, excels_path, out_path)
    Acquire_all_target_info.run()