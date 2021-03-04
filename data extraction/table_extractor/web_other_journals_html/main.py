# -*- coding: utf-8 -*-
"""
Created on Mon May 18 09:13:02 2020

@author: 35732
"""

from get_tifo_from_html import Get_tinfo_from_html


if __name__ == '__main__':
    # the path of excel file contains Dois information
    doi = "10.1115-1.2836743"

    # the path of folder to store the output excel files
    output_path = r"C:\Users\win\Desktop\springer_out_test"

    G_t = Get_tinfo_from_html(doi_path, output_path)
    G_t.run()
