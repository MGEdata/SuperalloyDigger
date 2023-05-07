import requests
import xlrd
import pickle
import os

def dois_read(path):
    with open(path, "rb") as file:
        dois = file.readlines()
    return dois


class File_Download:
    def __init__(self, api_path, dois, arformat, corpus_type, output_path):
        """

        :param api_path: r"...\APIkeys.txt"
        :param dois:
        :param arformat: text/xml,text/plain
        :param corpus_type: article/abstract
        :param output_path: r"...\txts"
        """
        with open(api_path, "r", encoding="utf-8") as api_f:
            self.apikeys = api_f.readlines()
        self.dois = dois
        self.arformat = arformat
        self.corpus_type = corpus_type
        self.header = {'Accept': 'text/xml', 'CR-TDM-Rate-Limit': '4000', 'CR-TDM-Rate-Limit-Remaining': '76',
          'CR-TDM-Rate-Limit-Reset': '1378072800'}
        self.url_publisher = "https://api.elsevier.com/content/" + self.corpus_type + "/doi/"

        self.output_path = output_path
        if self.arformat == "text/xml":
            self.end = ".xml"
        elif self.arformat == "text/plain":
            self.end = ".txt"


    def data_totxt(self,sample, path):
        f = open(path, 'w', encoding='utf-8')
        f.write(sample)
        f.close()

    def run(self,key_id,dois,i):
        key = self.apikeys[key_id]
        key = key.replace("\n","")
        APIKey = "APIKey=" + key
        doi = str(dois[i])
        doi_ = doi.replace("\n", "")
        url = self.url_publisher + doi_ + "?" + APIKey + "&httpAccept=" + self.arformat
        r = requests.get(url, verify=False, headers=self.header)
        doi = str(dois[i].decode()) # if error, change it to "doi = str(dois[i])"
        doi_ = doi_.replace("/", "-")
        path = os.path.join(self.output_path, doi_ + self.end)
        if "RESOURCE_NOT_FOUND" not in r.content.decode()and "AUTHENTICATION_ERROR" not in r.content.decode() and "Bad Request"  not in r.content.decode():# 无法获取资源
            try:
                self.data_totxt(r.content.decode(), path)
            except (OSError) as e:
                path = os.path.join(self.output_path, str(i)+ self.end)
                self.data_totxt(r.content.decode(), path)
            size = os.path.getsize(path)
            if size//1024 <3:
                key_id += 1
                doi = self.run(key_id, dois, i)
        return doi



if __name__ == '__main__':
    path = r".\dois.txt"
    dois = dois_read(path)
    api_path = r"...\APIkeys.txt"#保存APIkey的文本，APIkey从https://dev.elsevier.com/进行申请
    arformat = "text/xml"  # text/xml,text/plain
    corpus_type = "article" # article/abstract
    output_path = r"...\xmls"
    fd = File_Download(api_path, dois, arformat, corpus_type, output_path)

#     count = len(dois)
#     articles = []
#     doi_error = dict()
#     start_id = dois.index('10.1002/cssc.201600516')#为了防止网络问题断开下载，可以从这个DOI开始继续往下下载
#     batch_id = 1
#     key_id = 0
#     for i in range(0, count):# 当代码终止，将最新生成的doi所在dois中的索引（start_id）换掉这里的0
#         doi = fd.run(key_id,dois,i)
#         print(doi)

