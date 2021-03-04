# -*- coding: utf-8 -*-
"""
Created on Mon Apr 27 23:15:37 2020

@author: 35732
"""
# from configparser import ConfigParser
import configparser

class Dictionary:
    def __init__(self, path):
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