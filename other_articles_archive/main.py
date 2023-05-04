# -*- coding: utf-8 -*-


from html_parser import Html_parser


if __name__ == '__main__':
    
    #journal_list = ["Springer", "ASME", "NaturePublishingGroup", "Tandfonline", "WileyBlackwell", "MDPI"]
    journal = "ASME"
    html_path = r".../ASME_html"
    out_path = r"E.../ASME_txt"
    html_p = Html_parser(journal, html_path, out_path)
    html_p.paragraph_extract()