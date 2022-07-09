# -*- coding: utf-8 -*-
"""
Created on Mon May 18 09:13:02 2020

@author: wwr
"""

import xlwt
import os
from get_full_text import FilterText
from pre_processor import PreProcessor
from sentence_positioner import SentencePositioner
from file_io import File_IO as FI
from T_pre_processor import TPreProcessor
from Phrase_parse import PhraseParse
from Relation_extraciton import RelationExtraciton
from get_all_attributes import AllAttributes
from log_wp import LogWp


def mkdir(file_name):
    pathd = os.getcwd() + '\\' + file_name
    if os.path.exists(pathd):
        for root, dirs, files in os.walk(pathd, topdown=False):
            for name in files:
                os.remove(os.path.join(root, name))
            for name in dirs:
                os.rmdir(os.path.join(root, name))
        os.rmdir(pathd)
    os.mkdir(pathd)


if __name__ == '__main__':
    log_wp = LogWp()
    # 配置文件的路径
    c_path = r'dictionary.ini'
    # 下载得到文本的储存文件夹路径
    origin_text_path = r'...\all_txt_folder'
    # 提取的目标性能名称
    prop_name = 'solvus'
    # 创建存放输出文件的文件夹
    mkdir('output')
    mkdir(r'output\full_text2')
    # 经过全文定位之后的文本的储存文件夹路径
    text_path = r"output\full_text2"
    # 定位得到的目标语料
    TS_path = r"output\sent.xls"
    # 识别所得三元体文件的路径
    triple_path = r"output\out-triple.xls"
    # 所有参数的综合输出路径
    out_path = r"output\all-attributes.xls"
    # 筛选获取全文内容
    FT = FilterText(origin_text_path, text_path)
    txt_name = FT.process()
    # 获取目标语料
    all_x = []
    txt_name2 = []
    length = len(os.listdir(text_path))       
    for i in range(0, length):
        n_path = text_path + '/' + str(os.listdir(text_path)[i])
        file = open(n_path, 'r', encoding='utf-8')
        data = file.read()
        processor = TPreProcessor(data, prop_name, c_path)
        filter_txt = processor.processor()
        positioner = SentencePositioner(filter_txt, prop_name, c_path)
        target_sents = positioner.target_sent()
        all_x.append(str(target_sents))
        txt_name2.append(n_path)
    FI = FI(all_x, TS_path, txt_name2)
    FI.out_to_excel()
    
    # 进行三元组的抽取
    data = FI.data_from_excel()
    xls = xlwt.Workbook()
    sht2 = xls.add_sheet("triple_extracion")
    # 代表triple的行数
    triple_lines = 0
    # 代表文件索引
    file_index = 0
    # 代表句子的行数
    num_of_lines = 0
    for item in data:
        sht2.write(triple_lines, 0, txt_name[0][file_index])
        if item:
            out_unit = []
            sent_out = {}
            l_sent = []
            for sent in item:
                processor = TPreProcessor(sent, prop_name, c_path)
                filter_data = processor.processor()
                parse = PhraseParse(filter_data, prop_name, c_path)
                sub_order, sub_id, object_list = parse.alloy_sub_search()
                RE = RelationExtraciton(prop_name, filter_data, sub_order, sub_id, object_list, c_path)
                all_outcome = RE.triple_extraction()
                if not all_outcome:
                    out = 'no target triples'
                    sht2.write(triple_lines, 2, out)
                    sht2.write(triple_lines, 3, 'None')
                    sht2.write(triple_lines, 4, 'None')
                    sht2.write(num_of_lines, 1, 'no target sentence')
                    num_of_lines += 1
                    triple_lines += 1
                n_triple = 0
                for index, v in all_outcome.items():
                    out_unit.append(v)
                    n_triple += 1
                for n in range(0, n_triple):
                    sht2.write(num_of_lines + n, 1, sent)
                num_of_lines = num_of_lines + n_triple

            for s in range(0, len(out_unit)):
                sht2.write(triple_lines + s, 2, out_unit[s][0])
                sht2.write(triple_lines + s, 3, out_unit[s][1])
                sht2.write(triple_lines + s, 4, out_unit[s][2])
            if out_unit:
                triple_lines = triple_lines + len(out_unit)
            else:
                triple_lines += 1
            file_index += 1
        else:
            out = 'no target triples'
            sht2.write(triple_lines, 2, out)
            sht2.write(triple_lines, 3, 'None')
            sht2.write(triple_lines, 4, 'None')
            sht2.write(num_of_lines, 1, 'no target sentence')
            num_of_lines += 1
            triple_lines += 1
            file_index += 1
    log_wp.excel_save(xls, triple_path)
    attributes = AllAttributes(prop_name, txt_name, text_path, triple_path, out_path, c_path)
    attributes.get_toexcel()
