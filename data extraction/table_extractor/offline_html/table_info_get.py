# -*- coding: utf-8 -*-
"""
Created on Wed Jan 20 14:49:42 2021

@author: wwr
"""
import os
import time
import urllib.request
import pandas as pd
import requests
from bs4 import BeautifulSoup
from log_wp import LogWp
from lxml import etree
import urllib.request
from bs4 import BeautifulSoup

'''
用于测试通过本地HTML文档表格抽取效果
taylor(table)    10.1080-02670836.1987.11782270
ASME(table) 10.1115-1.1447238   10.1115-1.3225007
wiley(table) 10.1002-adem.201200055  10.1002-1527-2648(200
MDPI(table) 10.3390-ma8095299   10.3390-met4010001
需要进行HTML文档合并
NPG(table) 10.1038-s41529-018-0046-1.mhtml  10.1038-s41467-020-14820-0
springer(table)10.1007-s11837-014-1181-y
'''
doi_url = ""


class GetTableInfoFromHtml:
    def __init__(self, html_path, output_path):
        self.html_path = html_path
        self.output_path = output_path
        self.log_wp = LogWp()

    def get_all_url(self, url):
        """
        return all url on the page
        :param url:url of one page
        :return: all url as list
        """
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0)\
                    Gecko/20100101 Firefox/23.0'}
        req = urllib.request.Request(url=url, headers=headers)
        html = urllib.request.urlopen(req).read().decode("utf-8")
        soup = BeautifulSoup(html, features='html.parser')
        tags = soup.find_all('a')
        all_url = []
        for tag in tags:
            all_url.append(str(tag.get('href')).strip())
        return all_url

    def get_table_url(self, doi_info):
        """
        return table url on the page for Springer and Nature Publishing Group
        param url:doi_info of article
        return: table url as list
        """
        all_url = self.get_all_url(doi_info[0])
        table_url = []
        for i in all_url:
            if "table" in i:
                if 'article' in i:
                    self.log_wp.print_log(str(i))
                    if doi_info[1] in "Springer":
                        table_url.append('https://link.springer.com' + i)
                    else:
                        table_url.append('https://www.nature.com' + i)
        if len(table_url) == 0:
            self.log_wp.print_log("There is no table url in this article!")
        self.log_wp.print_log(str(table_url))
        return table_url

    def doi_info(self, doi_str):
        """
        get url and database of doi
        param doi_str: doi as str
        return: doi_info=[doi_url,doi_database]
        doi_url: str
        """
        global doi_url
        doi_info = []
        if doi_str[0:7] in "10.1016":
            doi_url = "https://doi.org/" + doi_str
            doi_database = "Elsevier"
        elif doi_str[0:7] in ["10.1007", "10.1361", "10.1023"]:
            doi_url = "https://link.springer.com/article/" + doi_str
            doi_database = "Springer"
        elif doi_str[0:7] in "10.1080":
            doi_url = "https://doi.org/" + doi_str
            doi_database = "Taylor & Francis Online"
        elif doi_str[0:7] in ["10.1002", "10.1111"]:
            doi_url = "https://onlinelibrary.wiley.com/doi/" + doi_str
            doi_database = "Wiley Blackwell"
        elif doi_str[0:7] in "10.1115":
            doi_url = "https://doi.org/" + doi_str
            doi_database = "ASME International"
        elif doi_str[0:7] in "10.3390":
            all_url = self.get_all_url("https://doi.org/" + doi_str)
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
        doi_info.append(doi_str)
        return doi_info

    def filename(self, name):
        st = '\|/:?*<>;'
        for s in st:
            if s in name:
                name = name.replace(s, '-')
        return name

    def get_table(self, doi_info, path=r'table.xlsx'):
        """
        get all table name from the page,
        param doi_info: [doi_url,1doi_info_name]str
        param path: r""str
        return
        """
        table_name = []
        if doi_info[1] in ['Springer', 'Nature Publishing Group']:
            table_url = self.get_table_url(doi_info)
            if len(table_url) != 0:
                with pd.ExcelWriter(path) as writer:
                    for p in range(len(table_url)):
                        time.sleep(1)
                        self.log_wp.print_log("Start crawling the page")
                        r = requests.get(table_url[p])
                        rt = r.text
                        try:
                            df = pd.read_html(rt)
                            self.log_wp.print_log("complete!")
                        except Exception as e:
                            print(e)
                            self.log_wp.print_log('format of table ' + str(p) + ' is PDF')
                            continue
                        start = rt.find("<h1")
                        end = rt.rfind("</h1>")
                        title_str = ''
                        for i in range(start, end + 5):
                            title_str += rt[i]
                        title_start = title_str.find("Table")
                        title_end = title_str.find("</h1>")
                        title = ''
                        for j in range(title_start, title_end):
                            self.log_wp.print_log(str(title_str[j]))
                            title += title_str[j]
                        table_name.append(title)
                        table_te = []
                        row_doi = [doi_info[2]]
                        for j in range(len(df[0].columns) - 1):
                            row_doi.append('')
                        table_te.append(row_doi)
                        row_title = list()
                        row_title.append(title)
                        for j in range(len(df[0].columns) - 1):
                            row_title.append('')
                        table_te.append(row_title)
                        table_te.append(list(df[0].columns))
                        for i in range(len(df[0])):
                            table_te.append(list(df[0].iloc[i]))
                        df[0] = pd.DataFrame(data=table_te)
                        sheet_name = 'table' + str(p + 1)
                        df[0].to_excel(writer, sheet_name=sheet_name, header=None, index=False)
            else:
                self.log_wp.print_log(" Cannot find table in this page: " + self.filename(doi_info[0]))
        elif doi_info[1] in 'Taylor & Francis Online':
            rt = self.get_rt(doi_info[0])
            page = BeautifulSoup(rt, 'lxml')
            table_name = []
            for page1 in page.find_all('b'):
                name = page1.text
                if 'Table' in name:
                    table_name.append(name)
            del table_name[int(len(table_name) / 2):len(table_name)]
            count = 0
            for t in table_name:
                if 'Table 1' in t:
                    count += 1
            if count > 1:
                del table_name[1:(len(table_name)):2]
            if len(table_name) != 0:
                with pd.ExcelWriter(path) as writer:
                    for p in range(len(table_name)):
                        df = pd.read_html(rt)
                        table_te = []
                        row_doi = [doi_info[2]]
                        for j in range(len(df[p].columns) - 1):
                            row_doi.append('')
                        table_te.append(row_doi)
                        row_title = list()
                        row_title.append(table_name[p])
                        for j in range(len(df[p].columns) - 1):
                            row_title.append('')
                        table_te.append(row_title)
                        table_te.append(list(df[p].columns))
                        for i in range(len(df[p])):
                            table_te.append(list(df[p].iloc[i]))
                        df = pd.DataFrame(data=table_te)
                        sheet_name = 'table' + str(p + 1)
                        df.to_excel(writer, sheet_name=sheet_name, header=None, index=False)
            else:
                self.log_wp.print_log(" Cannot find table in this page: " + self.filename(doi_info[0]))
        elif doi_info[1] in 'MDPI':
            rt = self.get_rt(doi_info[0])
            page = BeautifulSoup(rt, 'lxml')
            table_name = []
            for page1 in page.find_all('caption'):
                name = page1.text
                name = name.replace('\n', '')
                table_name.append(name)
            self.log_wp.print_log(str(table_name))
            if len(table_name) != 0:
                with pd.ExcelWriter(path) as writer:
                    time.sleep(1)
                    self.log_wp.print_log("Start crawling the page")
                    r = requests.get(doi_info[0])
                    rt = r.text
                    df = pd.read_html(rt)
                    self.log_wp.print_log("complete!")
                    for p in range(len(table_name)):
                        table_te = []
                        row_doi = [doi_info[2]]
                        for j in range(len(df[p].columns) - 1):
                            row_doi.append('')
                        table_te.append(row_doi)
                        row_title = list()
                        row_title.append(table_name[p])
                        for j in range(len(df[p].columns) - 1):
                            row_title.append('')
                        table_te.append(row_title)
                        table_te.append(list(df[p].columns))
                        for i in range(len(df[p])):
                            table_te.append(list(df[p].iloc[i]))
                        fa = pd.DataFrame(data=table_te)
                        sheet_name = 'table' + str(p + 1)
                        fa.to_excel(writer, sheet_name=sheet_name, header=None, index=False)
            else:
                self.log_wp.print_log(" Cannot find table in this page: " + self.filename(doi_info[0]))
        elif doi_info[1] in "ASME International":
            import re
            rt = self.get_rt(doi_info[0])
            page = BeautifulSoup(rt, 'lxml')
            table_name = []
            for page1 in page.find_all('div'):
                name = page1.text
                if 'Table' in name[0:5]:
                    if ' ' in name[-1]:
                        table_name.append(name)
            if len(table_name) != 0:
                df = pd.read_html(rt)
                self.log_wp.print_log("complete!")
                del df[0:len(df):2]
                with pd.ExcelWriter(path) as writer:
                    for p in range(len(df)):
                        table_te = []
                        row_doi = [doi_info[2]]
                        for j in range(len(df[p].columns) - 1):
                            row_doi.append('')
                        table_te.append(row_doi)
                        row_title = list()
                        row_title.append(table_name[p])
                        for j in range(len(df[p].columns) - 1):
                            row_title.append('')
                        table_te.append(row_title)
                        table_te.append(list(df[p].columns))
                        for i in range(len(df[p])):
                            table_te.append(list(df[p].iloc[i]))
                        fa = pd.DataFrame(data=table_te)
                        sheet_name = 'table' + str(p + 1)
                        fa.to_excel(writer, sheet_name=sheet_name, header=None, index=False)
            else:
                self.log_wp.print_log(" Cannot find table in this page: " + doi_info[0])
        elif doi_info[1] in "Wiley Blackwell":
            rt = self.get_rt(doi_info[0])
            page = BeautifulSoup(rt, 'lxml')
            table_name = []
            for page1 in page.find_all('header'):
                name = page1.text
                if 'Table' in name:
                    name = ' '.join(name.split())
                    table_name.append(name.replace('\n', ''))
            try:
                if len(table_name) != 0:
                    df = pd.read_html(rt)
                    with pd.ExcelWriter(path) as writer:
                        for p in range(len(df)):
                            table_te = []
                            row_doi = [doi_info[2]]
                            for j in range(len(df[p].columns) - 1):
                                row_doi.append('')
                            table_te.append(row_doi)
                            row_title = list()
                            row_title.append(table_name[p])
                            for j in range(len(df[p].columns) - 1):
                                row_title.append('')
                            table_te.append(row_title)
                            table_te.append(list(df[p].columns))
                            for i in range(len(df[p])):
                                table_te.append(list(df[p].iloc[i]))
                            fa = pd.DataFrame(data=table_te)
                            sheet_name = 'table' + str(p + 1)
                            fa.to_excel(writer, sheet_name=sheet_name, header=None, index=False)
                else:
                    self.log_wp.print_log(" Cannot find table in this page: " + doi_info[0])
            except Exception as e:
                print(e)
                pself.log_wp.print_log(" Cannot find table in this page: " + doi_info[0])
        else:
            self.log_wp.print_log("Please try other function!")
        return table_name

    def get_rt(self, url):
        """
        param url:str
        return
        """
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}
        time.sleep(1)
        self.log_wp.print_log("Start crawling the page")
        r = requests.get(url, headers=headers)
        r.encoding = 'utf-8'
        rt = r.text
        self.log_wp.print_log("complete!")
        return rt

    def load_doi(self, path):
        import xlrd
        data = xlrd.open_workbook(path)
        table = data.sheet_by_index(0)
        doi_li = []
        for row in range(table.nrows):
            table_doi = table.row_values(row, start_colx=0, end_colx=None)[0]
            doi_li.append(table_doi)
        return doi_li

    def get_html(self, url):
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}
        req = urllib.request.Request(url=url, headers=headers)
        html = urllib.request.urlopen(req).read()
        return html

    def save_html(self, file_name, file_content):
        with open(file_name + ".html", "wb") as f:
            f.write(file_content)

    def down_html(self, doi_li, path=''):
        for s in range(len(doi_li)):
            name = self.filename(doi_li[s])
            url_te = self.doi_info(doi_li[s])[0]
            html = self.get_html(url_te)
            self.save_html(path + name, html)
            self.log_wp.print_log('html_' + str(s + 1) + " download completed!")

    def doi_renamed(self, html_name):
        name = html_name[0:-5]
        if len(html_name) > 7:
            name = self.str_sub(name, 7, '/')
        else:
            self.log_wp.print_log('Your file name is wrong!')
        return name

    def str_sub(self, string, p, c):
        new = []
        for s in string:
            new.append(s)
        new[p] = c
        return ''.join(new)

    def load_html(self, html_input_path):
        html_name = self.doi_renamed(os.path.basename(html_input_path))
        f = open(html_input_path, "r", encoding="utf-8")
        ft = f.read()
        return ft, html_name

    def get_table_html(self, doi_info, rt, path=r'table.xlsx'):
        """
        get all table name from the page,
        param doi_info: [doi_url,1doi_info_name]str
        param rt: requests.get(url).text
        param path: str
        return
        """
        if doi_info[1] in 'Taylor & Francis Online':
            page = BeautifulSoup(rt, 'lxml')
            table_name = []
            for page1 in page.find_all('b'):
                name = page1.text
                if 'Table' in name:
                    table_name.append(name)
            del table_name[int(len(table_name) / 2):len(table_name)]
            count = 0
            for t in table_name:
                if 'Table 1' in t:
                    count += 1
            if count > 1:
                del table_name[1:(len(table_name)):2]
            if len(table_name) != 0:
                with pd.ExcelWriter(path) as writer:
                    for p in range(len(table_name)):
                        df = pd.read_html(rt)
                        table_te = []
                        row_doi = [doi_info[2]]
                        for j in range(len(df[p].columns) - 1):
                            row_doi.append('')
                        table_te.append(row_doi)
                        row_title = list()
                        row_title.append(table_name[p])
                        for j in range(len(df[p].columns) - 1):
                            row_title.append('')
                        table_te.append(row_title)
                        table_te.append(list(df[p].columns))
                        for i in range(len(df[p])):
                            table_te.append(list(df[p].iloc[i]))
                        df = pd.DataFrame(data=table_te)
                        sheet_name = 'table' + str(p + 1)
                        df.to_excel(writer, sheet_name=sheet_name, header=None, index=False)
            else:
                self.log_wp.print_log(" Cannot find table in this file: " + self.filename(doi_info[2]) + '.html')
        elif doi_info[1] in 'MDPI':
            page = BeautifulSoup(rt, 'lxml')
            table_name = []
            for page1 in page.find_all('caption'):
                name = page1.text
                name = name.replace('\n', '')
                table_name.append(name)
            self.log_wp.print_log(str(table_name))
            if len(table_name) != 0:
                with pd.ExcelWriter(path) as writer:
                    df = pd.read_html(rt)
                    for p in range(len(table_name)):
                        table_te = []
                        row_doi = [doi_info[2]]
                        for j in range(len(df[p].columns) - 1):
                            row_doi.append('')
                        table_te.append(row_doi)
                        row_title = list()
                        row_title.append(table_name[p])
                        for j in range(len(df[p].columns) - 1):
                            row_title.append('')
                        table_te.append(row_title)
                        table_te.append(list(df[p].columns))
                        for i in range(len(df[p])):
                            table_te.append(list(df[p].iloc[i]))
                        fa = pd.DataFrame(data=table_te)
                        sheet_name = 'table' + str(p + 1)
                        fa.to_excel(writer, sheet_name=sheet_name, header=None, index=False)
            else:
                self.log_wp.print_log(" Cannot find table in this file: " + self.filename(doi_info[2]) + '.html')
        elif doi_info[1] in "ASME International":
            page = BeautifulSoup(rt, 'lxml')
            table_name = []
            for page1 in page.find_all('div'):
                name = page1.text
                if 'Table' in name[0:5]:
                    if ' ' in name[-1]:
                        table_name.append(name)
            if len(table_name) != 0:
                df = pd.read_html(rt)
                self.log_wp.print_log("complete!")
                del df[0:len(df):2]
                with pd.ExcelWriter(path) as writer:
                    for p in range(len(df)):
                        table_te = []
                        row_doi = [doi_info[2]]
                        for j in range(len(df[p].columns) - 1):
                            row_doi.append('')
                        table_te.append(row_doi)
                        row_title = list()
                        row_title.append(table_name[p])
                        for j in range(len(df[p].columns) - 1):
                            row_title.append('')
                        table_te.append(row_title)
                        table_te.append(list(df[p].columns))
                        for i in range(len(df[p])):
                            table_te.append(list(df[p].iloc[i]))
                        fa = pd.DataFrame(data=table_te)
                        sheet_name = 'table' + str(p + 1)
                        fa.to_excel(writer, sheet_name=sheet_name, header=None, index=False)
            else:
                self.log_wp.print_log(" Cannot find table in this file: " + self.filename(doi_info[2]) + '.html')
        elif doi_info[1] in ["Springer", "Nature Publishing Group", "Wiley Blackwell"]:
            page = BeautifulSoup(rt, 'lxml')
            table_name = []
            for page1 in page.find_all('header'):
                name = page1.text
                if 'Table' in name:
                    name = ' '.join(name.split())
                    table_name.append(name.replace('\n', ''))
            try:
                if len(table_name) != 0:
                    df = pd.read_html(rt)
                    with pd.ExcelWriter(path) as writer:
                        for p in range(len(df)):
                            table_te = []
                            row_doi = [doi_info[2]]
                            for j in range(len(df[p].columns) - 1):
                                row_doi.append('')
                            table_te.append(row_doi)
                            row_title = list()
                            row_title.append(table_name[p])
                            for j in range(len(df[p].columns) - 1):
                                row_title.append('')
                            table_te.append(row_title)
                            table_te.append(list(df[p].columns))
                            for i in range(len(df[p])):
                                table_te.append(list(df[p].iloc[i]))
                            fa = pd.DataFrame(data=table_te)
                            sheet_name = 'table' + str(p + 1)
                            fa.to_excel(writer, sheet_name=sheet_name, header=None, index=False)
                else:
                    self.log_wp.print_log(" Cannot find table in this file: " + self.filename(doi_info[2]) + '.html')
            except Exception as e:
                print(e)
                self.log_wp.print_log(" Cannot find table in this file: " + self.filename(doi_info[2]) + '.html')
        else:
            table_name = []
            self.log_wp.print_log("This doi belongs to other databases!")
        return table_name

    def run(self):
        html_list = os.listdir(self.html_path)
        for html_file in html_list:
            path = os.path.join(self.html_path, html_file)
            rt, html_name = self.load_html(path)
            excel_name = self.filename(html_name)
            output_path = self.output_path + '/' + '%s.xlsx'
            table_name = self.get_table_html(self.doi_info(html_name), rt, output_path % excel_name)
