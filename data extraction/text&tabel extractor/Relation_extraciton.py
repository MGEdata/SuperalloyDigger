# -*- coding: utf-8 -*-
"""
Created on Mon May 18 09:15:57 2020

@author: 35732
"""
import nltk 
import re
import copy
from dictionary import Dictionary
class Relation_extraciton:
    def __init__(self, prop_name, data, sub_order, sub_id, object_list, C_path, abbre_pairs):
        self.C_path = C_path
        self.prop_name = prop_name
        self.data = data
        self.sub_order = sub_order
        self.sub_id = sub_id
        self.object_list = object_list
        self.dictionary = Dictionary(self.C_path)
        self.abbre_pairs = abbre_pairs

    def triple_extraction(self):
        object_list = self.object_list
        sub_order = self.sub_order
        txt = self.data
        abbre_pairs_keys = self.abbre_pairs.keys()
        id_word = {}
        outcome = {}
        word_list = nltk.word_tokenize(txt)
        new_word_list = []
        word_id = {}
        replace_sub =[]
        w = 0
        if all(word not in txt for word in self.dictionary.other_phase[self.prop_name]):
            for word in word_list:
                search = re.findall(r'\S*[Aa]lloy$',word)
                if search:
                    replace_sub.append(word)
                id_word[w] = word
                w = w + 1
                new_word_list.append(word)
            new_sent = (' ').join(new_word_list)
            for s in range(0,len(sub_order)):
                if sub_order[s] not in new_sent:
                    sub_order.remove(sub_order[s])
            word_id = {value:key for key,value in id_word.items()}
            other_quality = self.dictionary.other_quality[self.prop_name]
            length_subject = len(sub_order)
            length_object = len(object_list)
            if length_subject == 0 and length_object ==1 and replace_sub:
                if any(key in word_list for key in other_quality) and replace_sub:
                    all_quality = []
                    len_quality = []
                    other_quality.append(self.prop_name)
                    for kek in other_quality:
                       if kek in word_list:
                           all_quality.append(kek)
                    for quality in all_quality:
                        quality_id = word_id[quality]
                        word = object_list[0]
                        value_id = word_id[word]
                        len_1 = abs(quality_id - value_id)
                        len_quality.append(len_1)
                    id_min = len_quality.index(min(len_quality))
                    min_quality = all_quality[id_min]
                    outcome[1] = replace_sub[0],min_quality,object_list[0]
                    other_quality.remove(self.prop_name)
                if all(key not in word_list for key in other_quality) and replace_sub:
                    outcome[1] = replace_sub[0],self.prop_name,object_list[0]
            if length_subject == 0 and length_object > 1 and replace_sub:
                if all(key not in word_list for key in other_quality) :                  
                    quality_id = word_id[self.prop_name]
                    distance_os = []
                    for word_obj in object_list:
                        id_word_obj = word_id[word_obj]
                        length_os =  abs(id_word_obj - quality_id)
                        distance_os.append(length_os)
                    id_min = distance_os.index(min(distance_os))
                    id_min_2 = id_min + 1
                    if id_min_2 != len(distance_os):
                        if distance_os[id_min+1] == min(distance_os):
                            id_min = id_min_2
                            outcome[1] = replace_sub[0],self.prop_name,object_list[id_min]
                        else:
                            outcome[1] = replace_sub[0],self.prop_name,object_list[id_min]  
                    else:
                        outcome[1] = replace_sub[0],self.prop_name,object_list[id_min]
                if any(key in word_list for key in other_quality):
                    other_quality.append(self.prop_name)
                    all_quality =[]
                    for word in word_list:
                        if word in other_quality and word not in all_quality:
                            all_quality.append(word)
                    k = 1
                    if len(all_quality) == len(object_list):
                        
                        for i in range(len(all_quality)):
                            outcome[k] = replace_sub[0],all_quality[i],object_list[i]
                            k += 1
                    else:
                        for word_obj in object_list:
                            id_word_qual = word_id[word_obj]
                            distance_os = []
                            for quality in all_quality:
                                id_word_obj = word_id[quality]
                                length_os = abs(id_word_qual - id_word_obj)
                                distance_os.append(length_os)
                            id_min = distance_os.index(min(distance_os))
                            outcome[k] = replace_sub[0],all_quality[id_min],word_obj
                            k += 1
                    other_quality.remove(self.prop_name)
                
            if length_subject != 0 and length_object != 0:
                if length_subject == length_object and length_subject == 1:
                    if any(key in word_list for key in other_quality):
                        out_id = {}
                        solidus_id = word_id[self.prop_name]
                        word = object_list[0]
                        value_id = word_id[word]
                        len_1 = abs(solidus_id - value_id)
                        for kek in other_quality:
                            if kek in word_list:
                                kek_id = word_id[kek]
                                len_2 = abs(kek_id - value_id)
                                out_id[kek] = len_2
                        out_id = sorted(out_id.items(),key=lambda x:x[1],reverse=False)
                        kek = out_id[0][0]
                        out_values = out_id[0][1]
                        len_min = min(out_values,len_1)
                        if len_min == len_1 :
                            sub = sub_order[0].replace('~',' ')
                            if sub in abbre_pairs_keys:
                                sub_alloy = self.abbre_pairs[sub]
                                outcome[1] = sub, self.prop_name, object_list[0]
                                outcome[2] = sub_alloy, self.prop_name, object_list[0]
                            else:
                                outcome[1] = sub,self.prop_name,object_list[0]
                        if len_min == out_values:
                            sub = sub_order[0].replace('~',' ')
                            if sub in abbre_pairs_keys:
                                sub_alloy = self.abbre_pairs[sub]
                                outcome[1] = sub,kek,object_list[0]
                                outcome[2] = sub_alloy,kek,object_list[0]
                            else:
                                outcome[1] = sub,kek,object_list[0]
                    else:  
                        sub = sub_order[0].replace('~',' ')
                        if sub in abbre_pairs_keys:
                            sub_alloy = self.abbre_pairs[sub]
                            outcome[1] = sub,self.prop_name,object_list[0]
                            outcome[2] = sub_alloy,self.prop_name,object_list[0]
                        else:
                            outcome[1] = sub,self.prop_name,object_list[0]
                if length_subject == length_object and length_subject > 1:
                    if all(key not in new_word_list for key in other_quality):
                        index_alloy = 1
                        for q in range(0,length_subject):
                            subject = sub_order[q]
                            obj_all = object_list[q]
                            subject = subject.replace('~',' ')
                            if subject in abbre_pairs_keys:
                                subject_alloy = self.abbre_pairs[subject]
                                outcome[index_alloy] = subject,self.prop_name,obj_all
                                outcome[index_alloy+1] = subject_alloy,self.prop_name,obj_all
                                index_alloy += 2
                            else:
                                outcome[index_alloy] = subject,self.prop_name,obj_all
                                index_alloy += 1
                    if any(key in word_list for key in other_quality):
                        all_quality =[]
                        all_quality.append(self.prop_name)
                        k = 1
                        for word in word_list:
                            if word in other_quality and word not in all_quality:
                                all_quality.append(word)
                        for word_sub in sub_order:
                            id_word_sub = word_id[word_sub]
                            distance_os = []
                            for word_obj in object_list:
                                id_obj = word_id[word_obj]
                                length_os =  abs(id_word_sub - id_obj)
                                distance_os.append(length_os)
                            id_min = distance_os.index(min(distance_os))
                            out_obj = object_list[id_min]
                            id_out_obj = word_id[out_obj]
                            distance_oq = []
                            for quality in all_quality:
                                id_quality = word_id[quality]
                                length_oq = abs(id_quality - id_out_obj)
                                distance_oq.append(length_oq)
                            id_min = distance_oq.index(min(distance_oq))
                            out_quality = all_quality[id_min]
                            subject = word_sub.replace('~',' ')
                            if subject in abbre_pairs_keys:
                                subject_alloy = self.abbre_pairs[subject]
                                outcome[k] = subject,out_quality,out_obj
                                outcome[k+1] = subject_alloy,out_quality,out_obj
                                k += 2
                            else:
                                outcome[k] = subject,out_quality,out_obj
                                k += 1
                if length_subject > length_object:
                    if all(key not in word_list for key in other_quality):
                        k = 1
                        ol = copy.deepcopy(object_list)
                        for word_obj in object_list:
                            id_word_obj = word_id[word_obj]
                            distance_os = []
                            for word_sub in sub_order:
                                id_word_sub = word_id[word_sub]
                                length_os =  abs(id_word_obj - id_word_sub)
                                distance_os.append(length_os)
                            id_min = distance_os.index(min(distance_os))
                            subject = sub_order[id_min]
                            word_obj = word_obj 
                            subject = subject.replace('~',' ')
                            if subject in abbre_pairs_keys:
                                subject_alloy = self.abbre_pairs[subject]
                                outcome[k] = subject,self.prop_name,word_obj
                                outcome[k+1] = subject_alloy,self.prop_name,word_obj
                                k += 2
                            else:
                                outcome[k] = subject,self.prop_name,word_obj
                                k += 1
                    if any(key in word_list for key in other_quality):
                        all_quality =[]
                        all_quality.append(self.prop_name)
                        k = 1
                        for word in word_list:
                            if word in other_quality and word not in all_quality:
                                all_quality.append(word)
                        for word_obj in object_list:
                            id_word_obj = word_id[word_obj]
                            distance_oq = []
                            for quality in all_quality:
                                id_quality = word_id[quality]
                                length_oq =  abs(id_word_obj - id_quality)
                                distance_oq.append(length_oq)
                            id_min = distance_oq.index(min(distance_oq))
                            out_quality = all_quality[id_min]
                            id_out_qual = word_id[out_quality]
                            distance_sq = []
                            for word_sub in sub_order:
                                id_word_sub = word_id[word_sub]
                                length_sq =  abs(id_out_qual - id_word_sub)
                                distance_sq.append(length_sq)
                            id_min = distance_sq.index(min(distance_sq))
                            out_sub = sub_order[id_min]
                            subject = out_sub.replace('~',' ')
                            if subject in abbre_pairs_keys:
                                subject_alloy = self.abbre_pairs[subject]
                                outcome[k] = subject,out_quality,word_obj
                                outcome[k+1] = subject_alloy,out_quality,word_obj
                                k += 2
                            else:
                                outcome[k] = subject,out_quality,word_obj
                                k += 1
                if length_subject < length_object and length_subject == 1:
                    if all(key not in word_list for key in other_quality):
                        id_word_quality = word_id[sub_order[0]]
                        distance_os = []
                        for word_obj in object_list:
                            id_word_obj = word_id[word_obj]
                            length_os = abs(id_word_quality - id_word_obj)
                            distance_os.append(length_os)
                        id_min = distance_os.index(min(distance_os))
                        id_min_0 = id_min + 1
                        if id_min_0 != len(distance_os):
                            if distance_os[id_min + 1] == min(distance_os):
                                id_min = id_min + 1
                        object_0 = object_list[id_min]
                        subject = sub_order[0].replace('~',' ')
                        if subject in abbre_pairs_keys:
                            subject_alloy = self.abbre_pairs[subject]
                            outcome[1] = subject, self.prop_name,object_0
                            outcome[2] = subject_alloy, self.prop_name,object_0
                        else:
                            outcome[1] = subject, self.prop_name,object_0
                    if any(key in word_list for key in other_quality):
                        all_quality =[]
                        other_quality.append(self.prop_name)
                        k = 1
                        for word in word_list:
                            if word in other_quality and word not in all_quality:
                                all_quality.append(word)
                        if len(all_quality) == len(object_list):
                            for i in range(len(all_quality)):
                                subject = sub_order[0].replace('~',' ')
                                if subject in abbre_pairs_keys:
                                    subject_alloy = self.abbre_pairs[subject]
                                    outcome[k] = subject, all_quality[i],object_list[i]
                                    outcome[k + 1] = subject_alloy, all_quality[i],object_list[i]
                                    k += 2
                                else:
                                    outcome[k] = subject, all_quality[i],object_list[i]
                                    k += 1
                        else:
                            for word_obj in object_list:
                                id_word_qual = word_id[word_obj]
                                distance_os = []
                                for quality in all_quality:
                                    id_word_obj = word_id[quality]
                                    length_os = abs(id_word_qual - id_word_obj)
                                    distance_os.append(length_os)
                                id_min = distance_os.index(min(distance_os))
                                subject = sub_order[0].replace('~',' ')
                                if subject in abbre_pairs_keys:
                                    subject_alloy = self.abbre_pairs[subject]
                                    outcome[k] = subject, all_quality[id_min],word_obj
                                    outcome[k + 1] = subject_alloy, all_quality[id_min],word_obj
                                    k += 2
                                else:
                                    outcome[k] = subject, all_quality[id_min],word_obj
                                    k += 1
                        other_quality.remove(self.prop_name)
                if length_subject < length_object and length_subject > 1:
                    if all(key not in word_list for key in other_quality):
                        k = 1
                        for sub in sub_order:
                            id_sub = self.sub_id[sub]
                            distance_os = []
                            for word_obj in object_list:
                                id_word_obj = word_id[word_obj]
                                length_os = abs(id_sub - id_word_obj)
                                distance_os.append(length_os)
                            id_min = distance_os.index(min(distance_os))
                            id_min_0 = id_min + 1
                            if id_min_0 != len(distance_os):
                                if distance_os[id_min + 1] == min(distance_os):
                                    id_min = id_min + 1
                            object_0 = object_list[id_min]
                            subject = sub.replace('~',' ')
                            if subject in abbre_pairs_keys:
                                subject_alloy = self.abbre_pairs[subject]
                                outcome[k] = subject, self.prop_name,object_0
                                outcome[k + 1] = subject_alloy, self.prop_name,object_0
                                k += 2
                            else:
                                outcome[k] = subject, self.prop_name,object_0
                                k += 1
                    if any(key in word_list for key in other_quality):
                        all_quality =[]
                        all_quality.append(self.prop_name)
                        k = 1
                        for word in word_list:
                            if word in other_quality and word not in all_quality:
                                all_quality.append(word)
                        for word_sub in sub_order:
                            id_word_sub = word_id[word_sub]
                            distance_so = []
                            for word_obj in object_list:
                                id_word_obj = word_id[word_obj]
                                length_so =  abs(id_word_sub - id_word_obj)
                                distance_so.append(length_so)
                            id_min = distance_so.index(min(distance_so))
                            out_obj = object_list[id_min]
                            id_out_obj = word_id[out_obj]
                            distance_oq = []    
                            for quality in all_quality:
                                id_quality = word_id[quality]
                                length_oq =  abs(id_out_obj - id_quality)
                                distance_oq.append(length_oq)
                            id_min = distance_oq.index(min(distance_oq))
                            out_quality = all_quality[id_min]
                            subject = word_sub.replace('~',' ')
                            if subject in abbre_pairs_keys:
                                subject_alloy = self.abbre_pairs[subject]
                                outcome[k] = subject, out_quality,out_obj
                                outcome[k+1] = subject_alloy, out_quality,out_obj
                                k += 2
                            else:
                                outcome[k] = subject, out_quality,out_obj
                                k += 1
        return outcome