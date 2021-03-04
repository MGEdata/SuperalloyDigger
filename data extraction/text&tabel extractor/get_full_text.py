# -*- coding: utf-8 -*-
"""
Created on Tue Oct 22 22:02:21 2019

@author: 35732
"""

import os
import nltk
import re
from log_wp import Log_wp

def get_elsevier_doi(full_text_path):
    target_doi = ''
    doi_pattern = 'doi:10.1016\S+'
    file = open(full_text_path, encoding="UTF-8")
    line_data = file.readlines()
    file.close()
    for line in line_data:
        line_c = line.strip()
        doi_search = re.findall(doi_pattern, line_c)
        if doi_search:
            target_doi = doi_search[0]
            break
    return target_doi

class Filter_text:
    def __init__(self,in_path,out_path):
        self.in_path = in_path
        self.out_path = out_path
        self.log_wp = Log_wp()

    def data_totxt(self, sample,path):
        self.log_wp.write_totxt_log(path, sample)

    def process(self):
        txt_name = os.listdir(self.in_path)
        lengthen_0 = len(txt_name)
        doi_list = []
        for k in range(0,lengthen_0):
            new_data = []
            datas_outcome = []
            file =open(self.in_path +'/'+ txt_name[k],'r',encoding='utf-8')
            data_i = file.read()
            doi_info = get_elsevier_doi(self.in_path +'/'+ txt_name[k])
            data_i = data_i.replace('Key words','Keywords')
            data_i = data_i.replace('Keywords','Keyword')
            data_i = data_i.replace('INTRODUCTION','Introduction')
            token_data = nltk.word_tokenize(data_i)
            if "Keyword" in token_data:
                index_abstract = token_data.index('Keyword')
                token_data = token_data[index_abstract:]
                new_data = token_data
                if 'References' in new_data or 'Reference' in new_data:
                    if 'References' in new_data:
                        new_data = new_data[::-1]
                        index_References = new_data.index('References')
                        new_data = new_data[index_References:]
                        new_data = new_data[::-1]
                        datas_outcome = " ".join(new_data)
                        path = self.out_path +'\\'+ txt_name[k]
                        self.data_totxt(datas_outcome, path)
                    else:
                        if 'Reference' in new_data:
                            new_data = new_data[::-1]
                            index_Reference = new_data.index('Reference')
                            new_data = new_data[index_Reference:]
                            new_data = new_data[::-1]
                            datas_outcome = " ".join(new_data)
                            path = self.out_path +'/'+ txt_name[k]
                            self.data_totxt(datas_outcome,path)
                else:
                    datas_outcome = " ".join(new_data)
                    path = self.out_path + '/' + txt_name[k]
                    self.data_totxt(datas_outcome,path)
        
            elif "Introduction" in token_data:
                re_token_data = token_data[::-1]
                index_Introduction = re_token_data.index('Introduction')
                token_data = re_token_data[:index_Introduction]
                new_data = token_data[::-1]
                if 'References' in new_data or 'Reference' in new_data:
                    if 'References' in new_data:
                        new_data = new_data[::-1]
                        index_References = new_data.index('References')
                        new_data = new_data[index_References:]
                        new_data = new_data[::-1]
                        datas_outcome = " ".join(new_data)
                        path = self.out_path +'/' + txt_name[k]
                        self.data_totxt(datas_outcome,path)
                    else:
                        if 'Reference' in new_data:
                            new_data = new_data[::-1]
                            index_Reference = new_data.index('Reference')
                            new_data = new_data[index_Reference:]
                            new_data = new_data[::-1]
                            datas_outcome = " ".join(new_data)
                            path = self.out_path +'/'+txt_name[k]
                            self.data_totxt(datas_outcome,path)
                else:
                    datas_outcome = " ".join(new_data)
                    path = self.out_path+'/'+txt_name[k]
                    self.data_totxt(datas_outcome,path)
            else:
                datas_outcome = data_i
                path = self.out_path+'/'+txt_name[k]
                self.data_totxt(datas_outcome,path)
            doi_list.append(doi_info)
        return txt_name,doi_list


