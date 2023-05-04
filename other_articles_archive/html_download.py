# -*- coding: utf-8 -*-
"""
Created on Fri Dec 11 17:27:22 2020

@author: wwr
"""

import ssl
ssl._create_default_https_context = ssl._create_unverified_context

def get_all_url(url):
    '''
    return all url on the page
    :param url:url of one page
    :return: all url as list
    '''
    import urllib.request
    from bs4 import BeautifulSoup
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0)\
                Gecko/20100101 Firefox/23.0'}
    req = urllib.request.Request(url=url, headers=headers)
    html = urllib.request.urlopen(req).read().decode("utf-8")
    soup = BeautifulSoup(html, features='html.parser')
    tags = soup.find_all('a')
    all_url = []
    for tag in tags:
        all_url.append(str(tag.get('href')).strip())
    return all_url

def doi_info(doi_str):
    '''
    get url and database of doi
    :param doi_str: doi as str
    :return: doi_info=[doi_url,doi_database]
    '''
    global doi_url
    doi_info = []
    if doi_str[:7] == "10.1016":
        doi_url = "https://doi.org/" + doi_str
        doi_database = "Elsevier"
    elif doi_str[0:7] in ["10.1007","10.1361","10.1023"]:
        doi_url = "https://link.springer.com/article/" + doi_str
        doi_database = "Springer"
    elif doi_str[0:7] == "10.1080":
        doi_url = "https://www.tandfonline.com/doi/" + doi_str
        doi_database = "Taylor & Francis Online"
    elif doi_str[0:7] == "10.1088":
        doi_url = "https://iopscience.iop.org/article/" + doi_str + "/meta"
        doi_database = "IOP Publishing"
    elif doi_str[0:7] in ["10.1002","10.1111"]:
        doi_url = "https://onlinelibrary.wiley.com/doi/" + doi_str
        doi_database = "Wiley Blackwell"
    elif doi_str[0:7] == "10.1115":
        doi_url = "https://doi.org/" + doi_str
        doi_database = "ASME International"
    elif doi_str[0:7] == "10.3390":
        #解决MDPI页面跳转
        all_url = get_all_url("https://doi.org/"+ doi_str)
        for url_str in all_url:
            if "htm" in url_str:
                doi_url = "https://www.mdpi.com/" + url_str
                break
        doi_database = "MDPI"
    elif doi_str[0:7] == "10.1038":
        doi_url = "https://doi.org/" + doi_str
        doi_database = "Nature Publishing Group"
    else:
        doi_url = "other URL"
        doi_database = "other database"
    doi_info.append(doi_url)
    doi_info.append(doi_database)
    return doi_info


import xlrd
import urllib.request
import os

def getHtml(url,User_Agent):
    html = None
    # Add 'Cookie' information as required by the journal
    headers = {'User-Agent':User_Agent}
    try:
        req = urllib.request.Request(url=url[0], headers=headers)
        html = urllib.request.urlopen(req).read()
    except Exception as e:
        print(e)
        print(f"{e} happen in {url}")
    
    return html

def saveHtml(file_name, file_content):
    with open(file_name + ".html", "wb+") as f:
        f.write(file_content)

