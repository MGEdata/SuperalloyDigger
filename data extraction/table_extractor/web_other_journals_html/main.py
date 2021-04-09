# -*- coding: utf-8 -*-
"""
Created on Mon May 18 09:13:02 2020

@author: 35732
"""

from get_tifo_from_html import GetTableHtml


if __name__ == '__main__':
    # the path of excel file contains Dois information
    doi = "10.1115-1.2836743"

    # the path of folder to store the output excel files
    output_path = r"...\output_folder"

    g_t = GetTableHtml(doi_path, output_path)
    g_t.run()
