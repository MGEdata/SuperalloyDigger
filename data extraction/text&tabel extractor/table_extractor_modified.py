# -*- coding: utf-8 -*-
"""
Created on Sat Oct 10 11:55:01 2020

@author: win
"""
#from table_extractor import TableExtractor
import pickle
from bs4 import BeautifulSoup
import re
from gensim.models.deprecated import keyedvectors
import numpy as np
from unidecode import unidecode_expect_nonascii
import unidecode
from scipy import stats
from table import (Table, Entity, Attribute, Link)
from bson.objectid import (ObjectId)
from html.parser import HTMLParser
import traceback
import sys
import openpyxl
import os
from dictionary import Dictionary
from log_wp import Log_wp

class TableExtractor_modifiedtoalloy(object):
    def __init__(self,xml_path, save_path, config_path):
        self.xml_path = xml_path
        self.save_path = save_path
        self.dict_info = Dictionary(config_path)
        self.list_of_units = self.dict_info.table_units
        self.log_wp = Log_wp()
    def extract_and_save_all_tables(self, files=None, dois=None):
        with open('bin/word_classifier_python3.pkl', 'rb', encoding='utf-8') as f:
            clf = pickle.load(f)
        if files is None:
            self.log_wp.print_log("Need to provide list of files")
        if dois is None:
            self.log_wp.print_log("Need to provide list of dois for files")
        all_tables = []
        failures = 0
        for num, (doi, f) in enumerate(zip(dois, files)):
            tab = []
            doi = doi
            if 'html' in f:
                self.log_wp.print_log("Extracting Tables (HTML) from:%s", doi)
                problem = False
                tables, captions, footers, capt_refs, table_refs = get_tables(f)
                self.log_wp.print_log(len(tables))
                self.log_wp.print_log(len(captions))
                self.log_wp.print_log(len(footers))
                cols, rows, col_inds, row_inds = self.get_headers(tables)
                pred_cols, pred_rows = self.classify_table_headers(cols, rows)
                orients = []
                composition_flags = []
                for pred_col, pred_row, col, row in zip(pred_cols, pred_rows, cols, rows):
                    orient, composition_flag = self.determine_table_orientation(pred_col, pred_row, col, row)
                    orients.append(orient)
                    composition_flags.append(composition_flag)
                tab = []
                for table, row_ind, col_ind, orient, table_ref in zip(tables, row_inds, col_inds, orients, table_refs):
                    tab.append(self.construct_table_object(orient, table, row_ind, col_ind, table_ref))
                for i, (t, comp_flag, caption, footer, ref) in enumerate(
                        zip(tab, composition_flags, captions, footers, capt_refs)):
                    if t is not None:
                        t['order'] = i
                        t['_id'] = ObjectId()
                        t['paper_doi'] = doi
                        t['composition_table'] = comp_flag
                        t['caption'] = caption
                        if ref is not None:
                            t['caption_ref'] = ref
                        if footer is not None:
                            t['footer'] = footer
                        if comp_flag:
                            t = self.clean_composition_table(t, remaining = remaining)
                        all_tables.append(t)
                        self.log_wp.print_log('Success: Extracted Tables from %s', doi)

            elif 'xml' in f:
                self.log_wp.print_log('Extracting Tables (XML) from %s', doi)
                try:
                    tables, captions, footers, table_refs, capt_refs = self.get_xml_tables(doi, f)
                    cols, rows, col_inds, row_inds = self.get_headers(tables)
                    pred_cols, pred_rows = self.classify_table_headers(cols, rows)
                    orients = []
                    composition_flags = []
                    for pred_col, pred_row, col, row in zip(pred_cols, pred_rows, cols, rows):
                        orient, composition_flag = self.determine_table_orientation(pred_col, pred_row, col, row)
                        orients.append(orient)
                        composition_flags.append(composition_flag)
                    tab = []
                    for table, row_ind, col_ind, orient, ref in zip(tables, row_inds, col_inds, orients, table_refs):
                        try:
                            curr = (self.construct_table_object(doi, orient, table, row_ind, col_ind, ref))
                            tab.append(curr)
                        except IndexError as e:
                            self.log_wp.print_log('Failure: %s', doi)
                            failure += 1
                    for i, (t, comp_flag, caption, footer, capt_ref) in enumerate(
                            zip(tab, composition_flags, captions, footers, capt_refs)):
                        if t is not None:
                            t['order'] = i
                            t['_id'] = ObjectId()
                            t['caption'] = caption
                            t['paper_doi'] = doi
                            t['composition_table'] = comp_flag
                            if capt_ref is not None:
                                t['caption_ref'] = capt_ref
                            if footer is not None:
                                t['footer'] = footer
                            if comp_flag:
                                t = self.clean_composition_table(t, remaining=remaining)
                            all_tables.append(t)
                            self.log_wp.print_log('Success: Extracted Tables from %s', doi)
                except IndexError as e:
                    self.log_wp.print_log('FAILURE: XML index error : %s', doi)
                    failures += 1
            else:
                self.log_wp.print_log('Failure: File needs to be html or xml')
                failures += 1
        self.log_wp.print_log('Finished Extracting all Papers')
        self.log_wp.print_log('Number Attempted: %s', len(files))
        self.log_wp.print_log('Number Successful: %s', len(all_tables))
        self.log_wp.print_log('Number Failed: %s', failures)
        return all_tables


    def get_caption(self, doi, table, format):
        if format == 'html':
            if '10.1016' in doi:
                up = table.parent
                table_root = up.parent
                caption = table_root.find('div', 'caption')
                caption = caption.find('p')
                caption, ref = self._search_for_reference(caption, format)
                caption = unidecode.unidecode(HTMLParser().unescape(caption.text)).strip()
                return caption, ref

            elif '10.1039' in doi:
                check = table.parent
                check = check.parent
                if check.get('class') == ['rtable__wrapper']:
                    up = table.parent
                    up = up.parent
                    caption = up.previous_sibling
                    if caption is None:
                        return '', []
                    else:
                        caption = caption.previous_sibling
                        if caption is None:
                            return '', []
                        else:
                            caption = caption.find('span')
                            caption, ref = self._search_for_reference(caption, format)
                            caption = unidecode.unidecode(HTMLParser().unescape(caption.text)).strip()
                            return caption, ref
                else:
                    return '', []
            elif '10.1002' in doi:
                up = table.parent
                caption = up.previous_sibling
                caption = caption.previous_sibling
                if caption is not None:
                    caption.span.decompose()
                    caption, ref = self._search_for_reference(caption, format)
                    caption = unidecode.unidecode(HTMLParser().unescape(caption.text)).strip()
                    return caption, ref
                else:
                    self.log_wp.print_log('No caption')
                    return '', []
            elif '10.1021' in doi:
                up = table.parent
                if up.get('class') == ['NLM_table-wrap']:
                    caption = up.find('div', 'NLM_caption')
                else:
                    caption = up.previous_sibling
                if caption == ' ':
                    caption = caption.previous_sibling
                if caption is not None:
                    caption, ref = self._search_for_reference(caption, format)
                    caption = unidecode.unidecode(HTMLParser().unescape(caption.text)).strip()
                    return caption, ref
                else:
                    return '', None
            elif '10.1007' in doi:
                up = table.parent
                caption = up.previous_sibling
                caption = caption.find('p')
                caption, ref = self._search_for_reference(caption, format)
                caption = unidecode.unidecode(HTMLParser().unescape(caption.text)).strip()
                return caption, ref
            else:
                return '', []
        elif format == 'xml':
            if '10.1016' in doi:
                try:
                    caption = table.find('caption')
                    caption, ref = self._search_for_reference(caption, format)
                    caption = unidecode.unidecode(HTMLParser().unescape(caption.text)).strip()
                except Exception as e:
                    self.log_wp.print_log(str(e))
                return caption, ref
            elif '10.1021' in doi:
                caption = table.find('title')
                if caption is None:
                    up = table.parent
                    caption = table.find('title')
                    if caption is None:
                        caption = up.find('caption')
                caption, ref = self._search_for_reference(caption, format)
                caption = unidecode.unidecode(HTMLParser().unescape(caption.text)).strip()
                return caption, ref
        return '', []

    def get_footer(self, table, format):
        footer_dict = dict()
        if format == 'html':
            if '10.1016' in doi:
                up = table.parent
                table_root = up.parent
                footer = table_root.find_all('dl')
                if len(footer) > 0:
                    for f in footer:
                        dds = f.find('dd')
                        dts = f.find('dt')
                        if dds is None or dts is None:
                            self.log_wp.print_log('Problem in Footer: Keys and paragraphs len dont match')
                            return None
                        else:
                            footer_dict[dts.text.strip()] = unidecode.unidecode(HTMLParser().unescape(dds.text)).strip()
                else:
                    return None
            elif '10.1039' in doi:
                footer = table.find('tfoot')
                if footer is None:
                    return None
                else:
                    dts = footer.find_all('span', 'tfootnote')
                    dds = footer.find_all('span', 'sup_inf')
                    if len(dds) != len(dts):
                        self.log_wp.print_log('Problem in Footer: Keys and paragraphs len dont match')
                        return None
                    else:
                        for d, t in zip(dds, dts):
                            footer_dict[t.text.strip()] = unidecode.unidecode(HTMLParser().unescape(d.text)).strip()
            elif '10.1002' in doi:
                up = table.parent
                next = up.next_sibling
                next = next.next_sibling
                if next is None:
                    return None
                else:
                    footer = next.find('li').text
                    if footer is None:
                        return None
                    else:
                        regrex = re.compile('\[\D\]')
                        dts = regrex.findall(footer)
                        inter = regrex.split(footer)
                        dds = inter[1:]
                        if len(dts) != len(dds):
                            self.log_wp.print_log('Problem in Footer: Keys and paragraphs len dont match')
                            return None
                        else:
                            for d, t in zip(dds, dts):
                                footer_dict[t.strip()] = unidecode.unidecode(HTMLParser().unescape(d)).strip()
            elif '10.1007' in doi:
                up = table.parent
                next = up.next_sibling
                if next is None:
                    return None
                else:
                    if next.get('class') == ['TableFooter']:
                        footer = next.find_all('p')
                        if len(footer) > 0:
                            for f in footer:
                                sup = f.find('sup')
                                if sup is not None:
                                    dt = sup.text
                                    f.sup.decompose()
                                else:
                                    dt = 'NA'
                                footer_dict[dt.strip()] = unidecode.unidecode(HTMLParser().unescape(f.text)).strip()
                        else:
                            return None
            elif '10.1021' in doi:
                up = table.parent
                next = up.next_sibling
                if next == ' ':
                    next = next.next_sibling
                if next is None:
                    next = up
                    if next is None:
                        return None
                footer = next.find_all('div', 'footnote')
                if len(footer) > 0:
                    for f in footer:
                        sup = f.find('sup')
                        if sup is not None:
                            dt = sup.text
                            f.sup.decompose()
                        else:
                            p = f.find('p')
                            if p.text != f.text:
                                p = f.p.extract()
                                dt = f.text
                                f = p
                            else:
                                dt = 'NA'
                        footer_dict[dt.strip()] = unidecode.unidecode(HTMLParser().unescape(f.text)).strip()
                else:
                    return None
        elif format == 'xml':
            if '10.1016' in doi:
                footer = table.find_all('table-footnote')
                if len(footer) > 0:
                    for f in footer:
                        sup = f.find('label')
                        if sup is not None:
                            dt = sup.text
                            f.label.decompose()
                        else:
                            dt = 'NA'
                        footer_dict[dt.strip()] = unidecode.unidecode(HTMLParser().unescape(f.text)).strip()
                else:
                    footer = table.find('legend')
                    if footer is None:
                        return None
                    else:
                        all = footer.find_all('simple-para')
                        for a in all:
                            sup = a.find('sup')
                            if sup is not None:
                                dt = sup.text
                                a.sup.decompose()
                            else:
                                dt = 'NA'
                            footer_dict[dt.strip()] = unidecode.unidecode(HTMLParser().unescape(a.text)).strip()
            elif '10.1021' in doi:
                up = table.parent
                footer = up.find('table-wrap-foot')
                if footer is not None:
                    dts = footer.find_all('label')
                    dds = footer.find_all('p')
                    if len(dts) != len(dds):
                        ts = footer.find_all('sup')
                        dts = []
                        for t in ts:
                            if t.text != '':
                                dts.append(t)
                        if len(dds) == 1 and len(dts) > 1:
                            para = dds[0]
                            cont = para.contents
                            c = []
                            for co in cont:
                                try:
                                    c.append(co.text)
                                except:
                                    c.append(co)
                            ind = [i for i, x in enumerate(c) if x == '']
                            dts = []
                            dds = []
                            curr = ind[0]
                            for i in ind[1:]:
                                dts.append(c[curr - 1])
                                dds.append(''.join(c[(curr + 1):(i - 1)]))
                                curr = i
                            dts.append(c[curr - 1])
                            dds.append(''.join(c[(curr + 1):]))
                            for d, t in zip(dds, dts):
                                footer_dict[t.strip()] = unidecode.unidecode(HTMLParser().unescape(d)).strip().replace('\n',' ')
                        elif len(dts) != len(dds):
                            self.log_wp.print_log('Problem in Footer: Keys and paragraphs len dont match')
                            return None
                        else:
                            for d, t in zip(dds, dts):
                                footer_dict[t.text.strip()] = unidecode.unidecode(
                                    HTMLParser().unescape(d.text)).strip().replace('\n', ' ')
                    else:
                        for d, t in zip(dds, dts):
                            footer_dict[t.text.strip()] = unidecode.unidecode(
                                HTMLParser().unescape(d.text)).strip().replace('\n', ' ')
                else:
                    return None
        return footer_dict

    def get_xml_tables(self, doi, xml):
        all_tables = []
        all_captions = []
        soup = BeautifulSoup(open((xml), 'r+',encoding='utf-8'), 'xml')
        tables = soup.find_all('table')
        if len(tables) == 0:
            soup = BeautifulSoup(open(xml, 'r+',encoding='utf-8'), 'lxml')
            tables = soup.find_all('table-wrap')
        for w, table in enumerate(tables):
            try:
                try:
                    caption, ref = self.get_caption(doi,table, format='xml')
                except Exception as e:
                    self.log_wp.print_log(str(e))
                all_captions.append(caption)
                tab = []
                sup_tab = []
                for t in range(150):
                    tab.append([None] * 150)
                    sup_tab.append([None] * 150)
                rows = table.find_all('row')
                if len(rows) == 0:
                    rows = table.find_all('oasis:row')
                num_rows = len(rows)
                for i, row in enumerate(rows):
                    counter = 0
                    for ent in row:
                        curr_col = 0
                        beg = 0
                        end = 0
                        more_row = 0
                        if type(ent) == type(row):
                            if ent.has_attr('colname'):
                                try:
                                    curr_col = int(ent['colname'])
                                except:
                                    curr = list(ent['colname'])
                                    for c in curr:
                                        try:
                                            curr_col = int(c)
                                        except:
                                            continue
                            if ent.has_attr('namest'):
                                try:
                                    beg = int(ent['namest'])
                                except:
                                    curr = list(ent['namest'])
                                    for c in curr:
                                        try:
                                            beg = int(c)
                                        except:
                                            continue
                            if ent.has_attr('nameend'):
                                try:
                                    end = int(ent['nameend'])
                                except:
                                    curr = list(ent['nameend'])
                                    for c in curr:
                                        try:
                                            end = int(c)
                                        except:
                                            continue
                            if ent.has_attr('morerows'):
                                try:
                                    more_row = int(ent['morerows'])
                                except:
                                    curr = list(ent['morerows'])
                                    for c in curr:
                                        try:
                                            more_row = int(c)
                                        except:
                                            continue
                            ent, curr_ref = self._search_for_reference(ent, 'xml')
                            if beg != 0 and end != 0 and more_row != 0:
                                for j in range(beg, end + 1):
                                    for k in range(more_row + 1):
                                        tab[i + k][j - 1] = unidecode.unidecode(
                                            HTMLParser().unescape(ent.get_text())).strip().replace('\n', ' ')
                                        sup_tab[i + k][j - 1] = curr_ref
                            elif beg != 0 and end != 0:
                                for j in range(beg, end + 1):
                                    tab[i][j - 1] = unidecode.unidecode(
                                        HTMLParser().unescape(ent.get_text())).strip().replace('\n', ' ')
                                    sup_tab[i][j - 1] = curr_ref
                            elif more_row != 0:
                                for j in range(more_row + 1):
                                    tab[i + j][counter] = unidecode.unidecode(
                                        HTMLParser().unescape(ent.get_text())).strip().replace('\n', ' ')
                                    sup_tab[i + j][counter] = curr_ref
                            elif curr_col != 0:
                                tab[i][curr_col - 1] = unidecode.unidecode(
                                    HTMLParser().unescape(ent.get_text())).strip().replace('\n', ' ')
                                sup_tab[i][curr_col - 1] = curr_ref
                            else:
                                counter_ent = counter
                                found = False
                                while not found:
                                    if tab[i][counter_ent] is None:
                                        tab[i][counter_ent] = unidecode.unidecode(
                                            HTMLParser().unescape(ent.get_text())).strip().replace('\n', ' ')
                                        sup_tab[i][counter_ent] = curr_ref
                                        found = True
                                    else:
                                        counter_ent += 1
                                counter = counter_ent
                            counter = counter + 1 + (end - beg)
                for t, s in zip(tab, sup_tab):
                    for j, k in zip(reversed(t), reversed(s)):
                        if j is None:
                            t.remove(j)
                            s.remove(k)
                for t, s in zip(reversed(tab), reversed(sup_tab)):
                    if len(t) == 0:
                        tab.remove(t)
                        sup_tab.remove(s)
                lens = []
                for t in tab:
                    lens.append(len(t))
                size = stats.mode(lens)[0][0]
                for t, s in zip(tab, sup_tab):
                    if len(t) != size:
                        for j in range(len(t), size):
                            t.append('')
                            s.append([])
                all_tables.append(tab)
            except Exception as e:
                self.log_wp.print_log('Failed to extract XML table')
                table = [[0]]
                self.log_wp.print_log(str(e))
                sup_table = [[None]]
                all_tables.append(table)
                tb = sys.exc_info()[-1]
                self.log_wp.print_log(str(traceback.extract_tb(tb, limit=1)[-1][1]))
        return all_tables,all_captions

    def get_headers(self, tables):
        all_col_headers = []
        all_row_headers = []
        all_col_indexes = []
        all_row_indexes = []
        for num, table in enumerate(tables):
            try:
                curr = table[0]
                col_index = 0
                for i in range(len(table) - 1):
                    next = table[i + 1]
                    count_curr = 0
                    count_next = 0
                    for cell in curr:
                        try:
                            cell, _ = self.value_extractor(cell)
                            fixed = float(cell)
                        except:
                            if cell != '':
                                count_curr += 1
                    for cell in next:
                        try:
                            cell, _ = self.value_extractor(cell)
                            fixed = float(cell)
                        except:
                            if cell != '':
                                count_next += 1
                    if count_next > count_curr:
                        curr = next
                    else:
                        col_index = 0
                        break
                trans_table = list(map(list, zip(*table)))
                curr_row = trans_table[0]
                row_index = 0
                for i in range(len(trans_table) - 1):
                    next = trans_table[i + 1]
                    count_curr = 0
                    count_next = 0
                    for cell in curr_row:
                        try:
                            cell, _ = self.value_extractor(cell)
                            fixed = float(cell)
                        except:
                            if cell != '':
                                count_curr += 1
                    for cell in next:
                        try:
                            cell, _ = self.value_extractor(cell)
                            fixed = float(cell)
                        except:
                            if cell != '':
                                count_next += 1
                    if count_next > count_curr:
                        curr = next
                    else:
                        row_index = 0
                        break
                row_header = []
                col_header = []
                for i in range(col_index + 1):
                    col_header.extend(table[i])
                for i in range(row_index + 1):
                    row_header.extend(trans_table[i])
                indexes = []
                curr = col_header[0]
                for i in range(len(col_header) - 1):
                    next = col_header[i + 1]
                    if curr == next:
                        indexes.append(i)
                        curr = next
                    else:
                        curr = next
                for i in reversed(indexes):
                    col_header.pop(i)
                indexes = []
                curr = row_header[0]
                for i in range(len(row_header) - 1):
                    next = row_header[i + 1]
                    if curr == next:
                        indexes.append(i)
                        curr = next
                    else:
                        curr = next
                for i in reversed(indexes):
                    row_header.pop(i)
                all_col_headers.append(col_header)
                all_row_headers.append(row_header)
                all_col_indexes.append(col_index)
                all_row_indexes.append(row_index)
            except IndexError as e:
                self.log_wp.print_log("FAILURE: Index self.get_headers table #" + str(num) + " from paper " + str(doi))
                self.log_wp.print_log('IndexError in get headers')
                self.log_wp.print_log(str(e))
                tb = sys.exc_info()[-1]
                self.log_wp.print_log(str(traceback.extract_tb(tb, limit=1)[-1][1]))
        return all_col_headers, all_row_headers, all_col_indexes, all_row_indexes


    def load_embeddings(self, file_loc=None):
        if file_loc == None:
            self.log_wp.print_log('Need to specify path to word embedding model')
            self.log_wp.print_log('Materials science training word2vec and fasttext are available for download')
            self.log_wp.print_log('Check the read-me')
        else:
            embeddings = keyedvectors.KeyedVectors.load(file_loc)
            # embeddings.bucket = 2000000
            emb_vocab_ft = dict([('<null>', 0), ('<oov>', 1)] +
                                     [(k, v.index + 2) for k, v in embeddings.vocab.items()])
            emb_weights_ft = np.vstack([np.zeros((1, 100)), np.ones((1, 100)), np.array(embeddings.syn0)])


    def _normalize_string(self, string):
        ret_string = ''
        for char in string:
            if re.match(u'[Α-Ωα-ωÅ]', char) is not None:
                ret_string += str(char)
            else:
                ret_string += str(unidecode_expect_nonascii(str(char)))
        return ret_string


    def vectorize_words(self, words, labels):
        emb_vector = []
        label_vector = []
        for word, label in zip(words, labels):
            if word in emb_vocab_ft:
                ind = emb_vocab_ft[word]
                emb_vector.append(emb_weights_ft[ind])
                label_vector.append(label)
            else:
                label_vector.append(label)
                emb_vector.append(np.zeros(100, dtype=np.float32))
        emb_vector = np.array(emb_vector)
        return emb_vector, label_vector


    def classify_table_headers(self, cols, rows):
        vect_cols = []
        vect_rows = []
        for col, row in zip(cols, rows):
            vect_c, label = self.vectorize_words(col, [0] * len(col))
            vect_r, label = self.vectorize_words(row, [0] * len(row))
            vect_cols.append(clf.predict(vect_c))
            vect_rows.append(clf.predict(vect_r))
        return vect_cols, vect_rows


    def determine_table_orientation(self, pred_cols, pred_rows, cols, rows):
        # True- entities are row labels
        pred_cols = list(pred_cols)
        pred_rows = list(pred_rows)
        cols = list(cols)
        rows = list(rows)
        constituent_counter = 0
        for c in cols:
            if c in material_constituents:
                constituent_counter += 1
        if constituent_counter >= constituent_threshold:
            return True, True
        constituent_counter = 0
        for r in rows:
            if r in material_constituents:
                constituent_counter += 1
        if constituent_counter >= constituent_threshold:
            return False, True
        if stats.mode(pred_cols)[0][0] == 4 and pred_cols.count(4) >= (len(pred_cols) / 2):
            return False, False
        if stats.mode(pred_rows)[0][0] == 4 and pred_rows.count(4) >= (len(pred_rows) / 2):
            return True, False
        if stats.mode(pred_cols)[0][0] == 1 and pred_cols.count(1) >= (len(pred_cols) / 2):
            return True, False
        if stats.mode(pred_rows)[0][0] == 1 and pred_rows.count(1) >= (len(pred_rows) / 2):
            return False, False
        if stats.mode(pred_cols)[0][0] == 2 and pred_cols.count(2) >= (len(pred_cols) / 2) and 2 in pred_rows:
            return True, False
        if stats.mode(pred_rows)[0][0] == 2 and pred_rows.count(2) >= (len(pred_rows) / 2) and 2 in pred_cols:
            return False, False
        return True, False

    def construct_table_object(self, doi, table, row_ind, col_ind):
        new_table = Table()
        new_table['act_table'] = table
        mat_trans_table = np.array(table).T.tolist()
        mat_table = np.array(table).tolist()
        error_file = []
        try:
            for i, c in enumerate(mat_table[col_ind][(row_ind + 1):]):
                entity = Entity()
                entity['name'] = str(c)
                entity['descriptor'] = str(mat_table[col_ind][row_ind])
                if col_ind > 0:
                    for j in range(col_ind):
                        link = Link()
                        link['name'] = str(mat_table[col_ind - j - 1][i + 1])
                        if link['name'] != entity['name']:
                            entity['links']
                for j, r in enumerate(mat_trans_table[row_ind][(col_ind + 1):]):
                    attr = Attribute()
                    try:
                        potential_unit = unit_regex.search(r).group(0)[1:-1]
                        found_units = [u for u in self.list_of_units if u in potential_units]
                        if len(found_units) > 0:
                            attr['unit'] = unit
                    except:
                        pass
                    attr['name'] = str(r)
                    if row_ind > 0:
                        for k in range(row_ind):
                            link = Link()
                            link['name'] = str(mat_trans_table[row_ind - k - 1][j + 1])
                            if link['name'] != attr['name']:
                                attr['links'].append(link)
                    val, unit = self.value_extractor(str(mat_table[row_ind + j + 1][i + 1]))
                    if type(val) == float:
                        attr['value'] = val
                    else:
                        attr['string_value'] = val
                    if unit is not None:  # overwrites previous unit
                        attr['unit'] = unit
                    entity['attributes'].append(attr)
                new_table['entities'].append(entity)
            return new_table,set(error_file)
        except IndexError as e:
            self.log_wp.print_log("FAILURE: Index construct_table table from paper " + str(doi))
            self.log_wp.print_log('IndexError in construct object')
            self.log_wp.print_log(str(e))
            error_file.append(str(doi))
            return new_table, set(error_file)

    def print_table_object(self, table):
        for ent in table['entities']:
            self.log_wp.print_log('Ent:', ent['name'])
            self.log_wp.print_log('Links:')
            for link in ent['links']:
                self.log_wp.print_log(link['name'])
            self.log_wp.print_log('Attr:')
            for att in ent['attributes']:
                self.log_wp.print_log(att['name'])
                self.log_wp.print_log(att['value'])
                for link in att['links']:
                    self.log_wp.print_log(link['name'])
            self.log_wp.print_log('-------')
        self.log_wp.print_log('--------------')

    def value_extractor(self, string):
        original_string = string[:]
        extracted_unit = None
        balance_syn = ['balance', 'bal', 'bal.', 'other.', 'other']
        if string.lower() in balance_syn:
            return 'balance', extracted_unit

        units = [u for u in self.list_of_units if u in string]
        if units:
            extracted_unit = max(units)
            string = string.replace(extracted_unit, '')

        # e.g. already in int or float form: 12.5 -> 12.5
        try:
            return float(string), extracted_unit
        except:
            pass

        # e.g. 12.5 - 13.5 -> 13.0
        range_regex = re.compile('\d+\.?\d*\s*-\s*\d+\.?\d*')
        try:
            ranges = range_regex.search(string).group().split('-')
            average = (float(ranges[0]) + float(ranges[1])) / 2.0
            return average, extracted_unit
        except:
            pass

        # e.g. 12.2 (5.2) -> 12.2
        bracket_regex = re.compile('(\d+\.?\d*)\s*\(\d*.?\d*\)')
        try:
            extracted_value = float(bracket_regex.search(string).group(1))
            return float(extracted_value), extracted_unit
        except:
            pass

        # e.g. 12.3 ± 0.5 -> 12.3
        plusmin_regex = re.compile('(\d+\.?\d*)(\s*[±+-]+\s*\d+\.?\d*)')
        try:
            extracted_value = float(plusmin_regex.search(string).group(1))
            return extracted_value, extracted_unit
        except AttributeError:
            pass

        # e.g. <0.05 -> 0.05  |  >72.0 -> 72.0    | ~12 -> 12
        lessthan_roughly_regex = re.compile('([<]|[~]|[>])=?\s*\d+\.*\d*')
        try:
            extracted_value = lessthan_roughly_regex.search(string).group()
            num_regex = re.compile('\d+\.*\d*')
            extracted_value = num_regex.search(extracted_value).group()
            return float(extracted_value), extracted_unit
        except:
            pass

        # e.g. 0.4:0.6 (ratios)
        if ':' in string:
            split = string.split(":")
            try:
                extracted_value = round(float(split[0]) / float(split[1]), 3)
                return extracted_value, extracted_unit
            except:
                pass
        return original_string, None

    def load_composition_elements(self, domain=None):
        # Compositional elements to help in correclty identifiying the orientation of tables in specific domains
        if domain == 'geopolymers':
            material_constituents = ['Al2O3', 'SiO2']
            constituent_threshold = 2
            remaining = None
        elif domain == 'steel':
            material_constituents = ['Fe', 'Cr', 'Cu', 'C', 'Ti', 'Ni', 'Mo', 'Mn']
            constituent_threshold = 4
            remaining = ['Fe']
        elif domain == 'titanium':
            material_constituents = ['Ti', 'Fe', 'C']
            constituent_threshold = 2
            remaining = ['Fe']
        elif domain == 'zeolites':
            material_constituents = (
            ['Si/Ge', 'DMAP/T', 'HF/T', 'H2O/T', '(Si + Ge)/Al', 'SiO2', 'GeO2', 'SDA', 'HF', 'H2O', 'Ge', 'Si',
             'SiO2/Al2O3', 'Si/Al',
             'R(OH)2/Si', 'F-/Si', '(Si + Ge)/Zr', 'Al', 'SDA/Si', 'H2O/Si', 'OH/Si', 'Si/H2O', 'Si/OH', 'Ge/Si', 'Si/Ti',
             'MeO',
             'SiO2/GeO2', 'TMHDA', 'TMEDA', 'TEOS', 'NH4F', 'Al/T', 'N,N-Diethylethylenediamine', 'NaGaGeO4', 'NaGaO2',
             'Na2GeO3*H2O',
             'SOD', 'NaNO2', 'NaOH'])
            constituent_threshold = 2
            remaining = None
        elif domain == 'aluminum':
            material_constituents = ['Al', 'Cu', 'Mn', 'Si', 'O', 'Mg']
            constituent_threshold = 2
            remaining = None
        elif domain == 'alloys':
            material_constituents = ['Ag', 'Al', 'Ar', 'As', 'Au', 'B', 'Ba', 'Be', 'Bi', 'Br', 'C', 'Ca', 'Cd', 'Ce',
                                          'Cl', 'Co', 'Cr', 'Cs', 'Cu', 'Dy',
                                          'Er', 'Eu', 'F', 'Fe', 'Ga', 'Gd', 'Ge', 'H', 'Hf', 'Hg', 'Ho', 'I', 'In', 'Ir',
                                          'K', 'La', 'Li', 'Lu', 'Md', 'Mg',
                                          'Mn', 'Mo', 'N', 'Na', 'Nb', 'Nd', 'Ni', 'O', 'Os', 'P', 'Pb', 'Pd', 'Pr', 'Pt',
                                          'Rb', 'Re', 'Rh', 'Ru', 'S', 'Sb',
                                          'Sc', 'Se', 'Si', 'Sm', 'Sn', 'Sr', 'Ta', 'Tb', 'Te', 'Th', 'Ti', 'Tl', 'Tm', 'U',
                                          'V', 'W', 'Y', 'Yb', 'Zn', 'Zr']
            constituent_threshold = 2
            remaining = ['Fe', 'Al', 'Ti']


    def clean_composition_table(self, table, remaining=None):
        entities_to_remove = []
        for entity_num, entity in enumerate(table['entities']):
            # self.get_links(entity)
            cumsum, balance_pos, elements_in_entity = self.get_balance(entity)
            remaining_in_entity = None
            try:
                for check_element in remaining:
                    if check_element not in elements_in_entity:
                        remaining_in_entity = check_element
                        break
            except:
                pass
            # if 'balance' in a cell, it finds the balance and enters this under the 'value' key under the right attributes.
            # if no 'balance' but the total doesnt add up to 1.00 or 100, then there may be an implicit element missing.
            # we try to impute this by adding the 'remaining'
            if balance_pos:
                self.set_balance(entity, balance_pos, cumsum)
                continue
            elif (not balance_pos
                  and not self.check_if_balanced(cumsum)
                  and type(remaining_in_entity) == str):

                new_attr = Attribute()
                new_attr['name'] = str(remaining_in_entity)
                if cumsum < 1:
                    new_attr['value'] = 1.0 - cumsum
                else:
                    new_attr['value'] = 100.0 - cumsum
                new_attr['string_value'] = 'added by us'
                table['entities'][entity_num]['attributes'].append(new_attr)
            # if the cumsum == 0, it means that we can discard
            # this entire entity out as it holds no useful information
            if cumsum == 0:
                entities_to_remove.append(entity_num)

        for i in sorted(entities_to_remove, reverse=True):
            del (table['entities'][i])

        return table


    def get_balance(self, entity):
        cumsum = 0
        elements_in_entity = []
        balance_pos = None
        if entity['descriptor'] in material_constituents:
            attr = Attribute()
            attr['name'] = entity['descriptor']
            val, unit = self.value_extractor(entity['name'])
            if str(val).isnumeric():
                attr['value'] = float(val)
            elif type(val) == str:
                attr['string_value'] = val
            entity['attributes'].append(attr)
        for counter, attr in enumerate(entity['attributes']):
            if attr['name'] in material_constituents:
                cumsum += attr['value']
            elements_in_entity.append(attr['name'])
            if type(attr['string_value']) == str:
                if attr['string_value'].lower() in ['balance', 'bal', 'bal.']:
                    balance_pos = counter
                    self.log_wp.print_log('found a balance')
        return cumsum, balance_pos, elements_in_entity


    def set_balance(self, entity, balance_pos, cumsum):
        if cumsum < 1:
            entity['attributes'][balance_pos]['value'] = 1.0 - cumsum
        else:
            entity['attributes'][balance_pos]['value'] = 100.0 - cumsum


    def get_links(self, entity):
        list_of_names = []
        for attr in entity['attributes']:
            list_of_names.append(attr['name'])
        if len(set(list_of_names)) < 3:
            for attr in entity['attributes']:
                if len(attr['links']) > 0:
                    swapped = attr['name']
                    attr['name'] = attr['links'][0]['name']
                    attr['links'][0]['name'] = swapped


    def check_if_balanced(self, cumsum):
        if cumsum > 1:
            if 100 - cumsum < 1.5:
                return True
            else:
                return False
        else:
            if 1 - cumsum < 0.015:
                return True
            else:
                return False


    def _search_for_reference(self, soup, format):
        if format == 'html':
            ref = soup.find_all('a')
            tags = []
            if len(ref) == 0:
                text = soup.text
                refs = re.findall('\[\D\]', text)
                if len(refs) == 0:
                    return soup, tags
                else:
                    text = re.split('\[\D\]', text)
                    text = ''.join(text)
                    soup.string = text
                    return soup, refs
            else:
                for r in ref:
                    tag = soup.a.extract()
                    tags.append(tag.text)
                return soup, tags
        elif format == 'xml':
            ref = soup.find_all('xref')
            tags = []
            if len(ref) == 0:
                if soup.name == 'caption':
                    return soup, tags
                ref = soup.find_all('sup')
                for r in ref:
                    text = r.text.split(',')
                    for t in text:
                        if len(t) == 1 and t.isalpha():
                            tags.append(t)
                            soup.sup.decompose()
                return soup, tags
            else:
                for r in ref:
                    if len(r.text) < 4:
                        tag = soup.xref.extract()
                        tags.append(tag.text)
                return soup, tags

def get_extraction_outcome(xml_path,save_path,config_path):
    TableExtractor_m = TableExtractor_modifiedtoalloy(xml_path,save_path,config_path)
    all_error_file = []
    xml_name = os.listdir(xml_path)
    log_wp = Log_wp()
    for file_i in range(len(os.listdir(xml_path))):
        tables = None
        all_tables = []
        doi = xml_name[file_i].replace(".xml","")
        doi = doi.replace("-","/",1)
        xml_n = xml_name[file_i]
        file = xml_path+'/'+str(xml_n)
        try:
            tables,captions = TableExtractor_m.get_xml_tables(doi, file)
        except:
            all_error_file.append(doi)
        if tables:
            cols, rows, col_inds, row_inds = TableExtractor_m.get_headers(tables)
            tab = []

            for table, row_ind, col_ind in zip(tables, row_inds, col_inds):
                curr,error_file = (TableExtractor_m.construct_table_object(doi, table, row_ind, col_ind))
                if curr:
                    tab.append(curr)
                if error_file:
                    all_error_file.append(str(doi))
            for i, (t, caption) in enumerate(zip(tab, captions)):
                if t is not None:
                    t['order'] = i
                    t['_id'] = ObjectId()
                    t['caption'] = caption
                    t['paper_doi'] = doi
                    all_tables.append(t)
                    log_wp.print_log('Success: Extracted Tables from : %s', doi)
            xls = openpyxl.Workbook()
            sheet_id = 1
            if all_tables:
                for table in all_tables:
                    sht_new = xls.create_sheet(str(sheet_id))
                    act_table = table['act_table']
                    caption = table['caption']
                    row_len = len(act_table[0])
                    doi = table['paper_doi']

                    sht_new.cell(1,1,str(doi))
                    sht_new.cell(2,1,str(caption))
                    start_row = 3
                    for row in act_table:
                        len_row = len(row)
                        for index in range(len_row):
                            sht_new.cell(start_row,index+1,row[index])
                        start_row += 1
                    sheet_id += 1
                del xls['Sheet']
                log_wp.excel_save(xls, save_path+'/'+str(file_i)+"end.xlsx")
    return all_error_file,len(all_error_file)


