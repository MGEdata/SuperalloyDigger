# -*- coding: utf-8 -*-
"""
Created on Mon May 18 08:55:54 2020

@author: wwr
"""
import re
import nltk
from .dictionary import Dictionary


class TPreProcessor:
    def __init__(self, all_text, prop_name, c_path):
        self.c_path = c_path
        self.all_text = all_text
        self.dict_info = Dictionary(self.c_path)
        self.prop_name = prop_name

    def processor(self):
        all_txt = self.all_text
        replace_word = self.dict_info.replace_word
        unit_replace = self.dict_info.unit_replace
        paras = self.dict_info.paras_to_replace
        alloy_replace = self.dict_info.alloy_to_replace
        writing_type = self.dict_info.prop_writing_type
        for element in writing_type[self.prop_name]:
            all_txt = all_txt.replace(element, self.prop_name)
        for old_word, new_word in replace_word.items():
            all_txt = all_txt.replace(old_word, new_word)
        for para_model, change_place in paras.items():
            paras_all = re.findall(para_model, all_txt)
            for para in paras_all:
                find_word = re.findall(change_place[0], para)
                para_out = para.replace(find_word[0], change_place[1])
                all_txt = all_txt.replace(para, para_out)
        for alloy_model, replace in alloy_replace.items():
            alloy_part = re.findall(alloy_model, all_txt)
            for alloy in alloy_part:
                find_part = re.findall(replace[0], alloy)
                alloy_out = alloy.replace(find_part[0], replace[1])
                all_txt = all_txt.replace(alloy, alloy_out)
        sent_list = nltk.sent_tokenize(all_txt)
        patterns = self.dict_info.no_unit_para
        alloy_blank_type = self.dict_info.alloy_blank_type
        outcome = list()
        for pattern in alloy_blank_type:
            outcome = re.findall(pattern, all_txt)
        para = patterns[self.prop_name]
        for sent in sent_list:
            word_list = nltk.word_tokenize(sent)
            list_order = list(set(word_list))
            for word in list_order:
                if word not in outcome:
                    for pattern in para:
                        number = re.findall(pattern, word)
                        if unit_replace[self.prop_name]:
                            if unit_replace[self.prop_name][0] in sent and number:
                                sent_c = sent.replace(word, word + unit_replace[self.prop_name][0])
                                all_txt = all_txt.replace(sent, sent_c)
                            if unit_replace[self.prop_name][0] not in sent and number and len(unit_replace[self.prop_name])==2:
                                sent_c = sent.replace(word, word + unit_replace[self.prop_name][-1])
                                all_txt = all_txt.replace(sent, sent_c)
        return all_txt
