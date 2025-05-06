import requests
import os
import argparse

def dois_read(path):
    with open(path, "rb") as file:
        dois = file.readlines()
    return dois

class File_Download:
    def __init__(self, api_path, dois, arformat, corpus_type, output_path):
        """
        param api_path: r"...\APIkeys.txt"
        param dois:
        param arformat: text/xml, text/plain
        param corpus_type: article/abstract
        param output_path: r"...\txts"
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

    def data_totxt(self, sample, path):
        f = open(path, 'w', encoding='utf-8')
        f.write(sample)
        f.close()

    def run(self, key_id, dois, i):
        key = self.apikeys[key_id]
        key = key.replace("\n","")
        APIKey = "APIKey=" + key
        doi_ = str(dois[i].decode())
        doi_ = doi_.replace("\n", "")
        doi_ = doi_.replace("/", "-",1)
        doi_ = doi_.replace("\r", "")
        if not doi_.startswith("10.1002") or not "www.scientific.net" in doi_:
            url = self.url_publisher + doi_ + "?" + APIKey + "&httpAccept=" + self.arformat
            r = requests.get(url, verify=False, headers=self.header)
            path = os.path.join(self.output_path, doi_ + self.end)
            if "RESOURCE_NOT_FOUND" not in r.content.decode()and "AUTHENTICATION_ERROR" not in r.content.decode() and "Bad Request"  not in r.content.decode():# 无法获取资源
                try:
                    self.data_totxt(r.content.decode(), path)
                except (OSError) as e:
                    print("Error is " + str(e))
                    path = os.path.join(self.output_path, str(doi_)+ self.end)
                    self.data_totxt(r.content.decode(), path)
                size = os.path.getsize(path)
                if size//1024 <3:
                    key_id += 1
                    doi = self.run(key_id, dois, i)
                    print("Download file is small for" + doi)
        return doi_


def main(api_path, doi_path, output_path):
    print(f"参数api_txt_path: {api_path}")
    print(f"参数doi_txt_path: {doi_path}")
    print(f"参数output_path: {output_path}")

    arformat = "text/xml"
    corpus_type = "article"
    dois = dois_read(doi_path)
    fd = File_Download(api_path, dois, arformat, corpus_type, output_path)
    count = len(dois)
    key_id = 0
    for i in range(0,count):  # When the code terminates, replace the index (start_id) in the dois where the latest generated doi is located with the 0 here
        doi = fd.run(key_id, dois, i)
        print(doi)

    # 在这里写你的主逻辑

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="命令行参数示例")
    parser.add_argument("param1", nargs='?', help="第一个参数")
    parser.add_argument("param2", nargs='?', help="第二个参数")
    parser.add_argument("param3", nargs='?', help="第三个参数")

    args = parser.parse_args()

    # 如果命令行未传入，则提示用户输入
    param1 = args.param1 if args.param1 is not None else input("请输入参数api_txt_path：")
    param2 = args.param2 if args.param2 is not None else input("请输入参数doi_txt_path：")
    param3 = args.param3 if args.param3 is not None else input("请输入参数output_path：")

    main(param1, param2, param3)



