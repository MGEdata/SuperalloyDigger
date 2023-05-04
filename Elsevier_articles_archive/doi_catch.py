# -*- coding: utf-8 -*-
"""
Created on Sat Jun 29 22:34:51 2019

@author: WWR
"""

from crossref_commons.iteration import iterate_publications_as_json
from data_archive import data_archive

def doi_catch():
    filter = {'prefix':'10.1016','type': 'journal-article'}#10.1016是Elsvier前缀
    queries = {'query.bibliographic': {'alloy'}}#'alloy'作为本次搜索的关键词，根据任务的不同去更改，需要用单引号
    doilist = []
    for p in iterate_publications_as_json(max_results=1000000, filter=filter, queries=queries):
        doilist.append(p['DOI'])
    return doilist

if __name__ == '__main__':
    doilist = doi_catch()
    data_archive(doilist,"alloyDOI.xlsx","alloyDOI")
