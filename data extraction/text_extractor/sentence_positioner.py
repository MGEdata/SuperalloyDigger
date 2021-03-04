# -*- coding: utf-8 -*-
"""
Created on Mon Apr 27 23:15:37 2020

@author: 35732
"""
#Getting target sentences from a corpus
import re
import nltk
from dictionary import Dictionary
class Sentence_Positioner:
    def __init__(self,filter_txt,prop_name,C_path):
        self.C_path = C_path
        self.dict_info = Dictionary(C_path)
        self.prop_name = prop_name
        self.filter_txt = filter_txt

    def alloy_sub_search(self,txt):
        alloy_write_type = self.dict_info.alloy_writing_type
        alloy_blank_type = self.dict_info.alloy_blank_type
        outcome_filter = {}
        word_list = nltk.word_tokenize(txt)
        sub_order =[]
        for pattern in alloy_blank_type:
            outcome = re.findall(pattern,txt)
            if outcome:
                for name in outcome:
                    sub_order.append(name)
        len_type = len(alloy_write_type)
        for word in word_list:
            for i in range(0,len_type):
                outcome_filter[i] = re.findall(alloy_write_type[i],word)
            for k in range(0,len_type):
                if outcome_filter[k] :
                    sub_order.append(word)
                    break
        return sub_order

    def object_search(self,txt):
        value_writing_type = self.dict_info.value_wt[self.prop_name]
        
        len_type = len(value_writing_type)

        word_list = nltk.word_tokenize(txt)
        outcome_filter = {}
        object_list = []
        for word in word_list:
            for t in range(0,len_type):
                outcome_filter[t] = re.findall(value_writing_type[t],word)
            for q in range(0,len_type):
                if outcome_filter[q]:
                    object_list.append(word)
                    break
        return object_list

    def target_sent(self):
        target_sents = {}
        i = 1
        writing_type = self.dict_info.prop_writing_type
        sents_list = nltk.sent_tokenize(self.filter_txt)
        for sent in sents_list:
            sent_word_list = nltk.word_tokenize(sent)
            if len(sent) < 1000 and all(phase not in sent for phase in self.dict_info.other_phase[self.prop_name]):
                if any(element in sent_word_list for element in writing_type[self.prop_name]):
                    object_list = Sentence_Positioner.object_search(self,sent)
                    sub_order = Sentence_Positioner.alloy_sub_search(self,sent)
                    search = re.findall(r'\S*[Aa]lloy\s',sent)#
                    if object_list and sub_order:
                        target_sents[i] = sent
                        i += 1
                    elif search and object_list:
                        target_sents[i] = sent
                        i += 1
        return target_sents


    
    

