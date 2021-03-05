# -*- coding: utf-8 -*-
"""
Created on Mon May 18 09:13:02 2020

@author: 35732
"""
from class_modified import TableExtractor_modifiedtoalloy,get_extraction_outcome
from dictionary import Dictionary

if __name__ == '__main__':
    # extract the table information from xml files

    # the path of configuration file
    config_path = "dictionary.ini"

    # the path of document contains xml files
    xml_path = r'...\all_xml_folder'

    # the path of folder include excels that have been output
    save_path = r'...\xml_output_folder'

    all_error_file, length = get_extraction_outcome(xml_path, save_path, config_path)
