# -*- coding: utf-8 -*-
"""
Created on Mon May 18 09:13:02 2020

@author: wwr
"""
from .class_modified import get_extraction_outcome
from .html_parser import Html_parser
from .other_journals import OtherJ
from .get_tifo_from_html import GetTableHtml
from .text_with_table import AcquireAllTargetInfo
import os


class AllCase:

    def __init__(self, config, prop, dependency, path):
        self.config_path = config
        self.prop_name = prop
        self.dependency_out_path = dependency
        self.table_save_path = path
        self.AcquireAllTargetInfo = AcquireAllTargetInfo

    def case_1(self, txt_path, m_path):
        prop_list = [self.prop_name]
        acquire_all_target_info = self.AcquireAllTargetInfo(self.config_path, txt_path, prop_list,
                                                            self.table_save_path, self.dependency_out_path, m_path)
        acquire_all_target_info.run()

    def case_2(self, xml_path, origin_text_path, xml_out_path, m_path):
        oj = OtherJ()
        all_error_file, length = get_extraction_outcome(xml_path, self.table_save_path, self.config_path)
        triple_path = os.path.join(m_path, "out-triple.xls")
        oj.relation_extraction(self.config_path, origin_text_path, self.prop_name, triple_path, xml_out_path, m_path)
        prop_list = [self.prop_name]
        # the path of folder to store excels files that have been output
        acquire_all_target_info = self.AcquireAllTargetInfo(self.config_path, origin_text_path, prop_list,
                                                            self.table_save_path, self.dependency_out_path, m_path)
        acquire_all_target_info.run()

    def case_3(self, doi, html_path, journal, out_path_txt, out_path, m_path):
        oj = OtherJ()
        get_table = GetTableHtml(doi, self.table_save_path)
        get_table.run()
        html_p = Html_parser(journal, html_path, out_path_txt)
        html_p.paragraph_extract()
        triple_path = os.path.join(m_path, "out-triple.xls")
        oj.relation_extraction(self.config_path, out_path_txt, self.prop_name, triple_path, out_path, m_path)

        # target property
        prop_list = [self.prop_name]
        # the path of folder contains excel files
        excels_path = self.table_save_path
        # the path of folder to store excels files that have been output
        acquire_all_target_info = self.AcquireAllTargetInfo(self.config_path, out_path_txt, prop_list, excels_path,
                                                            self.dependency_out_path, m_path)
        acquire_all_target_info.run()


if __name__ == '__main__':

    pass
     # When user uploads the XML and TXT files from Elsevier journals
    # config_path = r"dictionary.ini"
    # prop_name = "solvus"
    # m_path = r"…\superalloydigger\web_output\m_output"
    # table_save_path = r"…\superalloydigger\web_output\table_output"
    # xml_out_path = r"…\superalloydigger\web_output\RE_outcome\all-attributes.xls"
    # dependency_out_path = r"…\superalloydigger\web_output\dependency_parser"
    # xml_path = r"…\superalloydigger\user_input\input_xml"
    # origin_text_path = r"…\superalloydigger\user_input\input_txt"
    # ac = AllCase(config_path, prop_name, dependency_out_path, table_save_path)
    # ac.case_2(xml_path, origin_text_path, xml_out_path, m_path)

    #  When user uploads an HTML file from a journal other than Elsevier
    # config_path = r"dictionary.ini"
    # prop_name = "solvus"
    # m_path = r"…\superalloydigger\web_output\m_output"
    # table_save_path = r"…\superalloydigger\web_output\table_output"
    # dependency_out_path = r"…\superalloydigger\web_output\dependency_parser"
    # html_path = r'…\superalloydigger\user_input\input_html'
    # journal = "WileyBlackwell"
    # out_path_txt = r"…\superalloydigger\web_output\txt_from_html"
    # out_path = r"…\superalloydigger\web_output\RE_outcome\all-attributes.xls"
    # ac = AllCase(config_path, prop_name, dependency_out_path, table_save_path)
    # ac.case_3(html_path, journal, out_path_txt, out_path, m_path)
