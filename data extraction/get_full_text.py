# -*- coding: utf-8 -*-
"""
Created on Tue Oct 22 22:02:21 2019

@author: 35732
"""

import os
import nltk

class Filter_text:
    #in_path为输入的文件夹路径，out_path为输出的文件夹路径

    def __init__(self,in_path,out_path):
        self.in_path = in_path
        self.out_path = out_path

    def data_totxt(sample,path):
        f = open(path,'w',encoding='utf-8')
        f.write(sample)
        f.close()
        
    def process(self):
        txt_name = os.listdir(self.in_path)
        print(txt_name)
        lengthen_0 = len(txt_name)  #计算单个文件夹下子文件的数目
        p = 0
        for k in range(0,lengthen_0):
            new_data = []
            datas_outcome = []
            file =open(self.in_path +'/'+ txt_name[k],'r',encoding='utf-8')
            data_i = file.read()
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
                        path = self.out_path +'\\'+ str(p) + '.txt'
                        #path = str(i)+".xml"
                        Filter_text.data_totxt(datas_outcome,path)
                        p = p+1

                    else:
                        if 'Reference' in new_data:
                            new_data = new_data[::-1]
                            index_Reference = new_data.index('Reference')
                            new_data = new_data[index_Reference:]
                            new_data = new_data[::-1]
                            datas_outcome = " ".join(new_data)
                            path = self.out_path +'/'+ str(p) + '.txt'
                            #path = str(i)+".xml"
                            Filter_text.data_totxt(datas_outcome,path)
                            p = p+1
                else:
                    datas_outcome = " ".join(new_data)
                    path = self.out_path +'/'+str(p) +'.txt'
                    #path = str(i)+".xml"
                    Filter_text.data_totxt(datas_outcome,path)
                    p = p+1
        
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
                        path = self.out_path +'/'+str(p)+'.txt'
                        #path = str(i)+".xml"
                        Filter_text.data_totxt(datas_outcome,path)
                        p = p+1

                    else:
                        if 'Reference' in new_data:
                            new_data = new_data[::-1]
                            index_Reference = new_data.index('Reference')
                            new_data = new_data[index_Reference:]
                            new_data = new_data[::-1]
                            datas_outcome = " ".join(new_data)
                            path = self.out_path +'/'+str(p)+'.txt'
                            #path = str(i)+".xml"
                            Filter_text.data_totxt(datas_outcome,path)
                            p = p+1

                else:
                    datas_outcome = " ".join(new_data)
                    path = self.out_path+'/'+str(p)+'.txt'
                    #path = str(i)+".xml"
                    Filter_text.data_totxt(datas_outcome,path)
                    p = p+1

            else:
                datas_outcome = data_i
                path = self.out_path+'/'+str(p)+'.txt'
                #path = str(i)+".xml"
                Filter_text.data_totxt(datas_outcome,path)
                p = p+1
        return txt_name


