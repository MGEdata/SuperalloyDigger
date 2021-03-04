# -*- coding: utf-8 -*-
"""
Created on Mon Apr 27 23:15:37 2020

@author: 35732
"""
import configparser
class Dictionary:
    def __init__(self,path):
        cp = configparser.RawConfigParser()
        cp.read(path,'UTF-8')
        self.replace_word = eval(cp.get("DICTIONARY",'replace_word'))
        self.alloy_to_replace = eval(cp.get("DICTIONARY",'alloy_to_replace'))
        self.paras_to_replace = eval(cp.get("DICTIONARY",'paras_to_replace'))
        self.alloy_writing_type = eval(cp.get("DICTIONARY",'alloy_writing_type'))
        self.alloy_blank_type = eval(cp.get("DICTIONARY",'alloy_blank_type'))
        self.prop_writing_type = eval(cp.get("DICTIONARY",'prop_writing_type'))
        self.value_wt = eval(cp.get("DICTIONARY",'value_wt'))
        self.other_phase = eval(cp.get("DICTIONARY",'other_phase'))
        self.unit_replace = eval(cp.get("DICTIONARY",'unit_replace'))
        self.no_unit_para = eval(cp.get("DICTIONARY",'no_unit_para'))
        self.other_quality = eval(cp.get("DICTIONARY",'other_quality'))
        self.table_alloy_to_replace = eval(cp.get("DICTIONARY",'table_alloy_to_replace'))
        self.table_prop_pattern = eval(cp.get("DICTIONARY",'table_prop_pattern'))
        self.table_e_pattern = eval(cp.get("DICTIONARY",'table_e_pattern'))
        self.table_ratio_pattern = eval(cp.get("DICTIONARY",'table_ratio_pattern'))
        self.table_units = eval(cp.get("DICTIONARY",'table_units'))
        self.ele_list = eval(cp.get("DICTIONARY",'ele_list'))
        self.table_number_pattern = eval(cp.get("DICTIONARY",'table_number_pattern'))
        self.table_unit_pattern_text = eval(cp.get("DICTIONARY",'table_unit_pattern_text'))
        self.unit_pattern_table = eval(cp.get("DICTIONARY",'unit_pattern_table'))
        self.ele_to_abr = eval(cp.get("DICTIONARY",'ele_to_abr'))
        self.alloy_abbre_type = eval(cp.get("DICTIONARY",'alloy_abbre_type'))
        self.table_prop_pattern_words = eval(cp.get("DICTIONARY",'table_prop_pattern_words'))