# -*- coding: utf-8 -*-
"""
Created on Mon Apr 27 23:15:37 2020

@author: 35732
"""
#Getting target sentences from a corpus
import re
from .dictionary import Dictionary
class Pre_processor:
    def __init__(self,all_text,c_path):
        self.c_path = c_path
        self.all_text = all_text
        self.dict_info = Dictionary(self.c_path)
        
    def pre_processor(self):
        all_txt = self.all_text
        replace_word = self.dict_info.replace_word
        paras = self.dict_info.paras_to_replace
        for old_word,new_word in replace_word.items():
            all_txt = all_txt.replace(old_word,new_word)
        for para_model,change_place in paras.items():
            paras_all = re.findall(para_model,all_txt)
            if paras_all:
                for para in paras_all:
                    find_word = re.findall(change_place[0],para)
                    para_out = para.replace(find_word[0],change_place[1])
                    all_txt = all_txt.replace(para,para_out)

        return all_txt


    
    

