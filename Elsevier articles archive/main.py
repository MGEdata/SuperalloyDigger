# -*- coding: utf-8 -*-
"""
Created on Tue Jun 16 11:01:12 2020

@author: 35732
"""
import os
from article_dois import ArticleArchiveDoi


def mkdir(file_name):
    pathd = os.getcwd()+'\\'+file_name
    if os.path.exists(pathd):
        for root, dirs, files in os.walk(pathd, topdown=False):
            for name in files:
                os.remove(os.path.join(root, name)) 
            for name in dirs:
                os.rmdir(os.path.join(root, name))
        os.rmdir(pathd) 
    os.mkdir(pathd)


if __name__ == '__main__':
    folder1 = 'text_path'
    mkdir(folder1)
    folder2 = 'all_origin_txt'
    mkdir(folder2)
    filename = 'alloyDOI.xlsx'
    path_txt = r'all_origin_txt'
    file_excel = r'text_path\text_path.xls'
    header = {'Accept': 'text/plain', 'CR-TDM-Rate-Limit': '4000', 'CR-TDM-Rate-Limit-Remaining': '76', 
              'CR-TDM-Rate-Limit-Reset': '1378072800'}
    url_publisher = "https://api.elsevier.com/content/article/doi/"  # 如果获取全文的话，将abstract替换成article
    APIKey = "APIKey=36697d0dea0745f5f236356d7f5cd38f"   # developer Elsevier 申请的
    arformat = "text/plain"   # text/xml,text/plain
    Article_archive_doi = ArticleArchiveDoi(header, filename, url_publisher, APIKey, arformat, path_txt, file_excel)
    Article_archive_doi.httprequest()
