# -*- coding: utf-8 -*-
"""
Created on Fri Dec 11 17:27:22 2020

@author: wwr
"""

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
        doi_url = "https://doi.org/" + doi_str
        doi_database = "Taylor & Francis Online"
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

def getHtml(url):

    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}
    req = urllib.request.Request(url=url, headers=headers)
    html = urllib.request.urlopen(req).read()

    return html

def saveHtml(file_name, file_content):
    with open(file_name + ".html", "wb+") as f:
        # 写文件用bytes而不是str，所以要转码
        f.write(file_content)

# 包含DOI信息的表格
data = xlrd.open_workbook(r'.../DOI_MDPI.xlsx')
table = data.sheet_by_index(0)
start = 1 #开始的行
end = 178 #结束的行
rows=end-start
list_values=[]
for x in range(start,end):
  values=[]
  row =table.row_values(x)
  values.append(row[1])
  list_values.append(values)

download = list()

# 输出html文件的路径
path = r'.../MDPI/html/'

for i in range(len(list_values)):
    url_te = doi_info(str(list_values[i][0]))[0]
    download.append(url_te[0])

    html = getHtml(url_te)
    file_name = str(list_values[i][0])
    saveHtml(path + str(file_name), html)
