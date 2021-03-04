# -*- coding: utf-8 -*-
"""
Created on Mon Apr 27 23:15:37 2020

@author: 35732
"""
import configparser
class Dictionary:
    def __init__(self,path):#表示配置文件的路径
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
        self.table_unit_pattern = eval(cp.get("DICTIONARY",'table_unit_pattern'))
        self.table_e_pattern = eval(cp.get("DICTIONARY",'table_e_pattern'))
        self.table_ratio_pattern = eval(cp.get("DICTIONARY",'table_ratio_pattern'))
        self.table_units = eval(cp.get("DICTIONARY",'table_units'))

        
        
        
        
        
        
#        self.replace_word = {'Fig .': 'fig ', 'Fig.': 'fig', 'fig.': 'fig', 'et al.': 'et al', '℃': '°C', '˚C': '°C', 'g cm−3': 'g/cm3', 'gm/cc': 'g/cm3', 'g cm3': 'g/cm3', '–': '-', 'L12': 'γ′', 'incipient melting': 'incipient-melting', "γ'": 'γ′', 'gamma prime': 'γ′', '™': 'TM', '<': '＜', '>': '＞', '＞ ': '＞', ' ＜': '＜', 'solution heat': 'solution-heat'}
#        self.alloy_to_replace = {r'\s([A-Z]+[a-z]*\s+[0-9]+)\s':["\s+","~"]}#会与很多仪器名称重叠
#        
#        self.paras_to_replace = {"\s[0-9]+\s+C":["\s+C","°C"],"[0-9]+\s+°C":["\s+",""],"[0-9]+\s+K":["\s+K","K"],'\s+±\s+':['\s+',''],'\s+–\s+':['\s+',''],'[0-9]+\s+g/cm3':['\s+g/cm3','g/cm3'],'\d\s+%':['\s+%','/%/']}
#        
#        self.alloy_writing_type = [r'^[0-9]+\.?[0-9]{0,2}[A-JL-Z]',r'[0-9]{0,2}\.?[0-9]{0,2}[A-Z][a-z]?\-[0-9]{0,2}\.?[0-9]{0,2}[A-Z][a-z]?',r'^[A-Z]+[a-z]*\-\S*[0-9]+$',r'^[A-Z]\S+[0-9]$',r'^[A-Z]+\S*\-[0-9A-Z]\S*',r'^[A-Z]+[0-9]+[A-z]+',r'^[A-Z]+[a-z]*\~[A-Z0-9]+$']
#        
#        self.alloy_blank_type = ['\s([0-9A-Z]+\w*)\s+\S*[Aa]lloy\s','\s+\S*[Aa]lloy\s+([0-9A-Z]+\w*)\s']
#        #用\w而不用\s是为了避免匹配Co-base等名称
#        #density中+s?
#        
#        self.prop_writing_type = {'solidus':['Tsolidus','Solidus','solidus'],'solvus':['γ′-solvus','γ′Solvus','solvus','γ′-transus','Tγ′','solvus-temperature','dissolution'],'density':['density','densities','densityρ','pO-'],'hardness':['microhardness', 'micro-hardness', 'nanohardness','hardnesses','nano-hardness','microhardnesses','Hardness','Micro-hardness','Microhardness','harness','macrohardness'],'liquidus':['liquidus','Liquidus','Tlq','liquidous','liquidusus']}
#        
#        self.value_wt = {'solidus':[r'^\W{0,1}[7-9][0-9]{2}(\.[0-9]{1,2})?\S*°C$','^\W{0,1}[7-9][0-9]{2}(\.[0-9]{1,2})?\S*K$','^\W{0,1}1[0-9][0-9]{2}\S*°C$','^\W{0,1}1[0-9][0-9]{2}\S*K$'],'solvus':[r'^\W{0,1}[7-9][0-9]{2}(\.[0-9]{1,2})?\S*°C$','^\W{0,1}[7-9][0-9]{2}(\.[0-9]{1,2})?\S*K$','^\W{0,1}1[0-9][0-9]{2}\S*°C$','^\W{0,1}1[0-9][0-9]{2}\S*K$'],'density':[r"^\W?[4-9](\.[0-9]{1,2})?\S*g/cm3|^\W?1[0,1](\.[0-9]{1,2})?\S*g/cm3"],'liquidus':[r'^\W{0,1}[7-9][0-9]{2}(\.[0-9]{1,2})?\S*°C$','^\W{0,1}[7-9][0-9]{2}(\.[0-9]{1,2})?\S*K$','^\W{0,1}1[0-9][0-9]{2}\S*°C$','^\W{0,1}1[0-9][0-9]{2}\S*K$']}
#        
##        self.triple_e_replace = {'Fig .':'fig ','Fig.':'fig','fig.':'fig','et al.':'et al',"℃":"°C","˚C":"°C",'g cm−3':'g/cm3','gm/cc':'g/cm3','L12':'γ′','incipient melting':'incipient-melting',"γ'":'γ′','gamma prime':'γ′','™':'TM','<':'＜','>':'＞','DSC':'dsc'}#各个性能分开
#        
##        self.triple_para_replace = {}
#        self.other_phase = {'solvus':['γ″','δ','η','TCP',' μ ',' P ',' R ','D019','M23 C6'],'solidus':[],'liquidus':[],'density':[]}#当这些字符出现时性能参数匹配会失败，参数改变了原来的归属,加空格是为了避免匹配到其它字符
#        self.unit_replace = {'solidus':['°C','K'],'solvus':['°C','K'],'density':['g/cm3'],'yield':['MPa'],'liquidus':['°C','K']}#是否某个性能存在两个有数量关系且通用的单位
#        self.no_unit_para = {'solvus':[r'^\W{0,1}[7-9][0-9]\S*\d$',r'^\W{0,1}1[0-9][0-9]\S*\d$'],'solidus':[r'^\W{0,1}[7-9][0-9]\S*\d$',r'^\W{0,1}1[0-9][0-9]\S*\d$'],'density':[r"^\W?[4-9]\.[0-9]{1,2}(\S\d\.\d{2})?$|^\W?1[0,1]\.[0-9]{1,2}(\S\d\.\d{2})?$"],'yield':[r'^\S?[1]?[2-9]\d{2}\.[0-9]{1,2}\S*'],'liquidus':[r'^\W{0,1}[7-9][0-9]\S*\d$',r'^\W{0,1}1[0-9][0-9]\S*\d$']}
#        self.other_quality = {'solvus':['γ′-solution','solution','solutioning','solidus','Tsolidus','Solidus','liquidus','Liquidus','Tlq','liquidous','liquidusus','incipient','age','aged','aging','heat','solution-heat','ageing','heated','heating','homogenized','homogenization','heat-treated','super-solvus','sub-solvus','γ″','solidification','eutectic','solubility','annealing','annealed','anneal','deformed','melting','incipient-melting'],'solidus':['γ′-solution','solution','solutioning','solvus','γ′-transus','liquidus','Liquidus','Tlq','liquidous','liquidusus','incipient','age','aged','aging','heat','solution-heat','ageing','heated','heating','homogenized','homogenization','heat-treated','super-solvus','sub-solvus','γ″','solidification','eutectic','solubility','annealing','annealed','anneal','deformed','melting','incipient-melting'],'density':[],'liquidus':['Tsolidus','Solidus','γ′-solution','solution','solutioning','solidus','incipient','γ′-solvus','γ′Solvus','solvus','γ′-transus','Tγ′','solvus-temperature','dissolution','age','aged','aging','heat','solution-heat','ageing','heated','heating','homogenized','homogenization','heat-treated','super-solvus','sub-solvus','γ″','solidification','eutectic','solubility','annealing','annealed','anneal','deformed','melting','incipient-melting']}#该范围的数值可能是其它的性能
        
        
        
         
        


    
    

