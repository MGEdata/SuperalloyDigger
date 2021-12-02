# -*- coding: utf-8 -*-
"""
Created on Mon May 18 09:13:02 2020

@author: 35732
"""
import os

import xlwt

from Phrase_parse import PhraseParse
from Relation_extraciton_orig import RelationExtraciton
from T_pre_processor import TPreProcessor
from file_io import File_IO as FI
from get_all_attributes import AllAttributes
from get_full_text import FilterText
from log_wp import LogWp
from pre_processor import PreProcessor
from sentence_positioner import SentencePositioner


class OtherJ():
    def __init__(self):
        pass

    def mkdir(self, file_name):
        pathd = os.path.join(os.getcwd(), file_name)
        if os.path.exists(pathd):
            for root, dirs, files in os.walk(pathd, topdown=False):
                for name in files:
                    os.remove(os.path.join(root, name))
                for name in dirs:
                    os.rmdir(os.path.join(root, name))
            os.rmdir(pathd)
        os.mkdir(pathd)

    def relation_extraction(self, C_path, origin_text_path, prop_name, triple_path, out_path, m_path):
        log_wp = LogWp()
        # 经过全文定位之后的文本的储存文件夹路径
        text_path = os.path.join(m_path, "full_text")
        # 定位得到的目标语料
        TS_path = os.path.join(m_path, "sent.xls")
        # 筛选获取全文内容
        FT = FilterText(origin_text_path, text_path)
        txt_name,dois = FT.process()
        # 获取目标语料
        all_x = []
        txt_name2 = []
        length = len(os.listdir(text_path))
        for i in range(0, length):
            n_path = text_path + '/' + str(os.listdir(text_path)[i])
            with open(n_path, 'r', encoding='utf-8') as file:
                data = file.read()
            pre_processor = PreProcessor(data, C_path)
            filter_data = pre_processor.pre_processor()

            # pre_processor = PreProcessor(data, C_path)
            # filter_txt = pre_processor.pre_processor()
            # positioner = SentencePositioner(filter_txt, prop_name, C_path)
            # target_sents = positioner.target_sent()

            processor = TPreProcessor(filter_data, prop_name, C_path)
            filter_data = processor.processor()
            positioner = SentencePositioner(filter_data, prop_name, C_path)
            target_sents = positioner.target_sent()

            # print(target_sents)
            all_x.append(str(target_sents))
            txt_name2.append(n_path)
        FI_out = FI(all_x, TS_path, txt_name2)
        FI_out.out_to_excel()

        # 进行三元组的抽取
        data = FI_out.data_from_excel()
        # print(data)
        xls = xlwt.Workbook()
        sht2 = xls.add_sheet("triple_extracion")
        triple_lines = 0  # 代表triple的行数
        file_index = 0  # 代表文件索引
        num_of_lines = 0  # 代表句子的行数g
        for item in data:
            doi = dois[file_index].replace("doi:","")
            sht2.write(triple_lines, 0, doi)
            if item != []:
                out_unit = []
                sent_out = {}
                l_sent = []
                for sent in item:
                    # print(sent)
                    processor = TPreProcessor(sent, prop_name, C_path)
                    filter_data = processor.processor()
                    # print(filter_data)
                    parse = PhraseParse(filter_data, prop_name, C_path)
                    sub_order, sub_id, object_list = parse.alloy_sub_search()
                    # print(sub_order, sub_id, object_list)
                    RE = RelationExtraciton(prop_name, filter_data, sub_order, sub_id, object_list, C_path)
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
                    #                sent_out[sent] = out_unit
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
        attributes = AllAttributes(prop_name, txt_name, text_path, triple_path, out_path, C_path, dois)
        attributes.get_toexcel()
