# -*- coding: utf-8 -*-
"""
Created on Mon May 18 09:13:02 2020

@author: 35732
"""

import xlwt
import os

from get_full_text import Filter_text
from pre_processor import Pre_processor
from sentence_positioner import Sentence_Positioner
from file_io import File_IO as FI
from T_pre_processor import T_pre_processor
from Phrase_parse import Phrase_parse
from Relation_extraciton import Relation_extraciton
from get_all_attributes import All_attributes

def mkdir(file_name):
    #file_name为要创建的文件夹路径
    pathd=os.getcwd()+'\\'+file_name
    if os.path.exists(pathd): #判断mydata文件夹是否存在
        for root, dirs, files in os.walk(pathd, topdown=False):
            for name in files:
                os.remove(os.path.join(root, name)) #删除文件
            for name in dirs:
                os.rmdir(os.path.join(root, name)) #删除文件夹
        os.rmdir(pathd) #删除mydata文件夹
    os.mkdir(pathd) #创建mydata文件夹

if __name__ == '__main__':
    
    #配置文件的路径
    C_path = r'dictionary.ini'
    #下载得到文本的储存文件夹路径
    origin_text_path = r'text-out-5000'
    #提取的目标性能名称
    prop_name = 'solidus'
    #创建存放输出文件的文件夹
    mkdir('output')
    mkdir(r'output\full_text')
    
    #经过全文定位之后的文本的储存文件夹路径
    text_path = r"output\full_text"
    
    #定位得到的目标语料
    TS_path = r"output\sent.xls"
    #识别所得三元体文件的路径
    triple_path = r"output\out-triple.xls"
    #所有参数的综合输出路径
    out_path = r"output\all-attributes.xls"
    #筛选获取全文内容
    FT = Filter_text(origin_text_path,text_path)
    txt_name = FT.process()
    #获取目标语料
    all_x = []
    txt_name2 = []
    length = len(os.listdir(text_path))       
    for i in range(0,length):
        n_path = text_path +'/'+str(i)+'.txt'
        file = open(n_path ,'r',encoding='utf-8')
        data = file.read()
        pre_processor = Pre_processor(data,C_path)
        filter_txt = pre_processor.pre_processor()
        positioner = Sentence_Positioner(filter_txt,prop_name,C_path)
        target_sents = positioner.target_sent()
        all_x.append(str(target_sents))
        txt_name2.append(n_path)
    FI = FI(all_x,TS_path,txt_name2)
    FI.out_to_excel()
    
#    进行三元组的抽取
    data = FI.data_from_excel()
    xls = xlwt.Workbook()
    sht2 = xls.add_sheet("triple_extracion")
    triple_lines = 0 #代表triple的行数
    file_index = 0 #代表文件索引
    num_of_lines = 0 #代表句子的行数
    for item in data:
        sht2.write(triple_lines,0,str(file_index)+'.txt')
        if item != []:
            out_unit = []
            sent_out = {}
            l_sent = []
            
            for sent in item:
                processor = T_pre_processor(sent,prop_name,C_path)
                filter_data = processor.processor()
                parse = Phrase_parse(filter_data,prop_name,C_path)
                sub_order,sub_id,object_list = parse.alloy_sub_search()
                RE = Relation_extraciton(prop_name,filter_data,sub_order,sub_id,object_list,C_path)
                all_outcome = RE.triple_extraction()
                n_triple = 0
                for index,v in all_outcome.items():
                    out_unit.append(v)
                    n_triple += 1

#                sent_out[sent] = out_unit

                for n in range(0,n_triple):
                    sht2.write(num_of_lines+n,1,sent)
                num_of_lines = num_of_lines + n_triple

            
            for s in range(0,len(out_unit)):
                
                sht2.write(triple_lines+s,2,out_unit[s][0])
                sht2.write(triple_lines+s,3,out_unit[s][1])
                sht2.write(triple_lines+s,4,out_unit[s][2])
            triple_lines = triple_lines + len(out_unit)
            file_index += 1
        else:
            out = 'no target triples'
            sht2.write(triple_lines,2,out)
            sht2.write(triple_lines,3,'None')
            sht2.write(triple_lines,4,'None')
            sht2.write(num_of_lines,1,'no target sentence')
            
            num_of_lines += 1 
            triple_lines += 1
            file_index += 1
    xls.save(triple_path)
#获取流程中所有关键的变量信息
    attributes = All_attributes(prop_name,txt_name,text_path,triple_path,out_path,C_path)
    attributes.get_toexcel()
    
    
    
    