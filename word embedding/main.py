# -*- coding: utf-8 -*-
"""
Created on Tue Jun 16 12:01:21 2020

@author: 35732
"""
from load_word2vec import Load_model

if __name__ == '__main__':
    model_path = 'word2vec/all-text'
    prop_name = 'solvus'
    n = 100
    sim_path = 'sim.txt'
    model = Load_model(model_path,prop_name,n,sim_path)
    simlist = model.load()
    f = open(sim_path, 'w', encoding='utf-8')
    f.write(str(simlist))
    f.close()