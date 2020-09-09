# -*- coding: utf-8 -*-
"""
Created on Wed May 13 18:46:14 2020

@author: 35732
"""
from gensim.models import word2vec
class Load_model:
    def __init__(self,path,prop_name,n,sim_path):
        self.path = path
        self.prop_name = prop_name
        self.n = n
        self.sim_path = sim_path
    def load(self):
        model = word2vec.Word2Vec.load(self.path)
        similarity_list = model.most_similar(self.prop_name, topn=self.n)
        return similarity_list