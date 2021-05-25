# -*- coding: utf-8 -*-
"""
Created on Tue Nov 24 20:32:04 2020

@author: win
"""
import re
from chemdataextractor import Document
import os
from .log_wp import Log_wp

class Html_parser():
    def __init__(self,journal,html_path,out_path):
        self.journal = journal
        self.html_path = html_path
        self.out_path = out_path
        self.log_wp = Log_wp()

    def paragraph_extract(self):
        no_pargas = []
        if self.journal == "Springer" or self.journal == "NaturePublishingGroup":
            html_file = os.listdir(self.html_path)
            number_file = len(os.listdir(self.html_path))
            no_pargas = []
            success_extracted = []
            content_exist = []
            content_label = "Sec\d+\S*"
            for file_i in range(0, number_file):
                sole_file = html_file[file_i]
                file = open(self.html_path + '/' + sole_file, 'rb')
                doc = Document.from_file(file)
                paragraphs = doc.paragraphs
                all_parag = ''
                content_find = None
                for parag in paragraphs:
                    if "Abs" in str(parag.id):
                        text = parag.text
                        if text[0].isupper() and len(text) > 100:
                            all_parag += '\n'
                        refs = re.findall(r"\[\d+[^\[]*\]", text)
                        for ref in refs:
                            text = text.replace(ref, '')
                        text = text.replace("\n", '')
                        all_parag += text
                        all_parag += " "

                    re_d = re.findall(content_label, str(parag.id))
                    if re_d:
                        text = parag.text
                        if text[0].isupper() and len(text) > 100:
                            all_parag += '\n'
                        refs = re.findall(r"\[\d+[^\[]*\]", text)
                        for ref in refs:
                            text = text.replace(ref, '')
                        text = text.replace("\n", '')
                        all_parag += text
                        all_parag += " "
                        content_find = True
                if content_find:
                    content_exist.append(sole_file)
                    # 若全文找不到段落标签
                if not all_parag:
                    self.log_wp.print_log("No paragraph label:%s",sole_file)
                    no_pargas.append(sole_file)
                    for parag in paragraphs:
                        text = parag.text
                        if text[0].isupper() and len(text) > 100:
                            all_parag += '\n'
                        refs = re.findall(r"\[\d+[^\[]*\]", text)
                        for ref in refs:
                            text = text.replace(ref, '')
                        text = text.replace("\n", '')
                        all_parag += text
                        all_parag += " "

                else:
                    success_extracted.append(sole_file)
                txt_name = str(sole_file).replace(".html", ".txt")
                path = self.out_path + '/' + txt_name
                self.log_wp.write_totxt_log(path, str(all_parag))

        if self.journal == "Tandfonline":
            html_file = os.listdir(self.html_path)
            number_file = len(os.listdir(self.html_path))
            no_pargas = []
            success_extracted = []
            content_exist = []
            content_label = "[Ss]\d{3}\S*"

            for file_i in range(0, number_file):
                sole_file = html_file[file_i]
                file = open(self.html_path + '/' + sole_file, 'rb')
                doc = Document.from_file(file)
                elements = doc.elements
                parags = doc.paragraphs
                all_parag = ''
                abs_search = None
                content_find = None
                for ele in elements:
                    if str(ele.id) == 'abstract':
                        abs_search = 1
                    if abs_search == 1:
                        abstract = ele.text
                        if abstract[0].isupper() and len(abstract) > 100:
                            all_parag += '\n'
                        refs = re.findall(r"\[\d+[^\[]*\]", abstract)
                        for ref in refs:
                            abstract = abstract.replace(ref, '')
                        abstract = abstract.replace("\n", '')
                        all_parag += abstract
                        all_parag += " "
                        break
                for parag in parags:
                    re_d = re.findall(content_label, str(parag.id))
                    if re_d:
                        text = parag.text
                        if text[0].isupper() and len(text) > 100:
                            all_parag += '\n'
                        refs = re.findall(r"\[\d+[^\[]*\]", text)
                        for ref in refs:
                            text = text.replace(ref, '')
                        text = text.replace("\n", '')
                        all_parag += text
                        all_parag += " "
                        content_find = True
                if content_find:
                    content_exist.append(sole_file)

                # 若全文找不到段落标签
                if not all_parag:
                    self.log_wp.print_log("No paragraph label:%s",sole_file)
                    no_pargas.append(sole_file)
                    for parag in parags:
                        text = parag.text
                        if text[0].isupper() and len(text) > 100:
                            all_parag += '\n'
                        text = text.replace("\n", '')
                        refs = re.findall(r"\[\d+[^\[]*\]", text)
                        for ref in refs:
                            text = text.replace(ref, '')
                        all_parag += text
                        all_parag += " "
                else:
                    success_extracted.append(sole_file)

                txt_name = str(sole_file).replace(".html", ".txt")
                path = self.out_path + '/' + txt_name
                self.log_wp.write_totxt_log(path, str(all_parag))

        if self.journal == "WileyBlackwell":
            html_file = os.listdir(self.html_path)
            number_file = len(os.listdir(self.html_path))
            no_pargas = []
            success_extracted = []
            content_exist = []
            content_label = "sec"

            for file_i in range(0, number_file):
                sole_file = html_file[file_i]
                file = open(self.html_path + '/' + sole_file, 'rb')
                doc = Document.from_file(file)
                parags = doc.paragraphs
                all_parag = ''
                content_find = None
                for parag in parags:
                    if content_label in str(parag.id) and "reference" not in str(parag.id):  # 避免参考文件信息加入到结果中
                        text = parag.text
                        if text[0].isupper() and len(text) > 100:
                            all_parag += '\n'
                        refs = re.findall(r"\[\d+[^\[]*\]", text)
                        for ref in refs:
                            text = text.replace(ref, '')
                        text = text.replace("\n", '')
                        all_parag += text
                        all_parag += " "
                        content_find = True
                if content_find:
                    content_exist.append(sole_file)

                # 若全文找不到段落标签
                if not all_parag:
                    self.log_wp.print_log("No paragraph label:%s",sole_file)
                    no_pargas.append(sole_file)
                    for parag in parags:
                        text = parag.text
                        if text[0].isupper() and len(text) > 100:
                            all_parag += '\n'
                        text = text.replace("\n", '')
                        refs = re.findall(r"\[\d+[^\[]*\]", text)
                        for ref in refs:
                            text = text.replace(ref, '')
                        all_parag += text
                        all_parag += " "

                else:
                    success_extracted.append(sole_file)

                txt_name = str(sole_file).replace(".html", ".txt")
                path = self.out_path + '/' + txt_name
                self.log_wp.write_totxt_log(path, str(all_parag))

        if self.journal == "ASME":
            html_file = os.listdir(self.html_path)
            number_file = len(os.listdir(self.html_path))
            no_pargas = []
            success_extracted = []
            content_exist = []
            content_label = "ContentTab"

            for file_i in range(0, number_file):
                sole_file = html_file[file_i]
                file = open(self.html_path + '/' + sole_file, 'rb')
                doc = Document.from_file(file)
                parags = doc.paragraphs
                all_parag = ''
                content_find = None
                for parag in parags:
                    if content_label == str(parag.id):
                        text = parag.text
                        if text == "References":
                            break
                        if text[0].isupper() and len(text) > 100:
                            all_parag += '\n'
                        refs = re.findall(r"\[\d+[^\[]*\]", text)
                        for ref in refs:
                            text = text.replace(ref, '')
                        text = text.replace("\n", '')
                        all_parag += text
                        all_parag += " "
                        content_find = True
                if content_find:
                    content_exist.append(sole_file)

                # 若全文找不到段落标签
                if not all_parag:
                    self.log_wp.print_log("No paragraph label:%s",sole_file)
                    no_pargas.append(sole_file)
                    for parag in parags:
                        text = parag.text
                        if text[0].isupper() and len(text) > 100:
                            all_parag += '\n'
                        text = text.replace("\n", '')
                        refs = re.findall(r"\[\d+[^\[]*\]", text)
                        for ref in refs:
                            text = text.replace(ref, '')
                        all_parag += text
                        all_parag += " "
                else:
                    success_extracted.append(sole_file)

                txt_name = str(sole_file).replace(".html", ".txt")
                path = self.out_path + '/' + txt_name
                self.log_wp.write_totxt_log(path, str(all_parag))

        if self.journal == "MDPI":
            html_file = os.listdir(self.html_path)
            number_file = len(os.listdir(self.html_path))
            no_pargas = []
            success_extracted = []
            content_exist = []
            content_label = "sec\d+\S*"
            content_label_2 = "^\d+[A-Z]\S*"
            for file_i in range(0, number_file):
                sole_file = html_file[file_i]
                file = open(self.html_path + '/' + sole_file, 'rb')
                doc = Document.from_file(file)
                paragraphs = doc.paragraphs
                all_parag = ''
                content_find = None
                for parag in paragraphs:
                    if "Abs" in str(parag.id) or "abs" in str(parag.id):
                        text = parag.text
                        if text[0].isupper() and len(text) > 100:
                            all_parag += '\n'
                        refs = re.findall(r"\[\d+[^\[]*\]", text)
                        for ref in refs:
                            text = text.replace(ref, '')
                        text = text.replace("\n", '')
                        all_parag += text
                        all_parag += " "

                    re_d = re.findall(content_label, str(parag.id))
                    re_d_2 = re.findall(content_label_2, str(parag.id))
                    if re_d or re_d_2:
                        text = parag.text
                        if text[0].isupper() and len(text) > 100:
                            all_parag += '\n'
                        refs = re.findall(r"\[\d+[^\[]*\]", text)
                        for ref in refs:
                            text = text.replace(ref, '')
                        text = text.replace("\n", '')
                        all_parag += text
                        all_parag += " "
                        content_find = True
                if content_find:
                    content_exist.append(sole_file)
                    # 若全文找不到段落标签
                if not all_parag:
                    self.log_wp.print_log("No paragraph label:%s",sole_file)
                    no_pargas.append(sole_file)
                    for parag in paragraphs:
                        text = parag.text
                        if text[0].isupper() and len(text) > 100:
                            all_parag += '\n'
                        refs = re.findall(r"\[\d+[^\[]*\]", text)
                        for ref in refs:
                            text = text.replace(ref, '')
                        text = text.replace("\n", '')
                        all_parag += text
                        all_parag += " "

                else:
                    success_extracted.append(sole_file)
                txt_name = str(sole_file).replace(".html", ".txt")
                path = self.out_path + '/' + txt_name
                self.log_wp.write_totxt_log(path, str(all_parag))

        return no_pargas, success_extracted, content_exist

