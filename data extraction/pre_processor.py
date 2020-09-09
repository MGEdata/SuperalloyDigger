# -*- coding: utf-8 -*-
"""
Created on Mon Apr 27 23:15:37 2020

@author: 35732
"""
#Getting target sentences from a corpus
import re
from dictionary import Dictionary
class Pre_processor:
    def __init__(self,all_text,C_path):
        self.C_path = C_path
        self.all_text = all_text
        self.dict_info = Dictionary(self.C_path)
        
    def pre_processor(self):
        all_txt = self.all_text
        replace_word = self.dict_info.replace_word
        replace_alloy = self.dict_info.alloy_to_replace
        paras = self.dict_info.paras_to_replace
        for old_word,new_word in replace_word.items():
            all_txt = all_txt.replace(old_word,new_word)

        for para_model,change_place in paras.items():
            para_model = para_model.replace('%%','%')
            paras_all = re.findall(para_model,all_txt)
            if paras_all:
                for para in paras_all:
                    change_place[0] = change_place[0].replace('%%','%')
                    change_place[1] = change_place[1].replace('%%','%')
                    find_word = re.findall(change_place[0],para)
                    para_out = para.replace(find_word[0],change_place[1])
                    all_txt = all_txt.replace(para,para_out)

        for old_alloy,new_alloy in replace_alloy.items():#需要在param的后面
            alloy_all = re.findall(old_alloy,all_txt)
            if alloy_all:
                for alloy in alloy_all:
                    find_word = re.findall(new_alloy[0],alloy)
                    alloy_out = alloy.replace(find_word[0],new_alloy[1])
                    all_txt = all_txt.replace(alloy,alloy_out)
        return all_txt


    
    

