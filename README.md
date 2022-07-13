[![Website](https://raw.githubusercontent.com/MGEdata/SuperalloyDigger/master/pic_folder/b96627c3f326953fce3452fd175f718.png)](http:superalloydigger.mgedata.cn)

[![SuperalloyDigger.org](https://shields.mitmproxy.org/badge/https%3A%2F%2F-superalloydigger.mgedata.cn-green)](http:superalloydigger.mgedata.cn)

[![Website](https://badge.fury.io/py/SuperalloyDigger.svg)](https://pypi.org/project/SuperalloyDigger)
[![Supported Python versions](https://shields.mitmproxy.org/badge/python-3.6%20%7C%203.7%20%7C%203.8-blue)](https://pypi.org/project/SuperalloyDigger)
----------------------
Automatic extraction of chemical compositions and properties from the scientific literature of superalloy, covering specific chemical composition, density, γ' solvus temperature, solidus temperature, and liquidus temperature. Starting with a corpus of scientific articles scraped in XML, HTML or plain text format, NLP techniques are used to preprocess the raw archived corpus, followed by text classifier and table parser, named entity recognition, relation extraction of text and table, and dependency parser automatically. Finally, the extracted tuple entities containing article doi, alloy named entity, property specifier, property value, element and fraction, are compiled into a highly structured format for materials database.

This package is released under MIT License, please see the LICENSE file for details.

This code and data is a companion to the paper, "Automated pipeline for superalloy data by text mining."

**Features**
----------------------
- An automated chemical composition and property data extraction pipeline for superalloy.
- Rule-based named entity recognition for superalloy.
- Algorithm based on distance and number of entities, processing multiple relationship extraction for text without labeling samples.
- Table parser and table relation extraction algorithms to mine data from tables in documents
- An interdependency parser to extract the information contain composition and property data simultaneous.

**Function**
----------------------
**Articles archive**

Automatically archive relevant articles mainly from Elsevier and some other publishers.  Combined with the CrossRef search Application Programming Interface (APIs) and Elsevier’s Scopus and Science Direct application programming interfaces (APIs), full text or abstract of corresponding field can be easily obtained. The premise is you have already got the copyright of the Elsevier database and applied for the APIkey of Elsevier. Users can find our source code at GitHub to use this function locally.

**Superalloy word embedding**

The word embedding model for superalloy corpus was pre-trained on ~9000 unlabeled full-text superalloy articles by Word2Vec continuous bag of words (CBOW) in gensim(https://radimrehurek.com/gensim/), which use information about the co-occurrences of words by assigning high-dimensional vectors (embeddings) to words in a text corpus, to preserve their syntactic and semantic relationships.

**Superalloy property extractor**

Automatic extraction of properties from the scientific literature of superalloy, covering density, γ' solvus temperature, solidus temperature, and liquidus temperature.
Starting with a corpus of scientific articles scraped in XML (Extensible Markup Language), HTML (Hyper Text Mark-up Language) or plain text format, NLP techniques are used to preprocess the raw archived corpus to produce a complete document record and filter out irrelevant information. Text classification aims to determine which sentence contains the target property information to be extracted. Table parsing transforms complete table caption and body into structural format and then classifies which table contains the chemical composition and target property information to be extracted. NER technology recognizes alloy named entity, property specifier, and property value from English-language text and table, followed by relation extraction. Relation extraction of text and table give the specific tuple relations for concrete element content and property, and dependency parsing resolves the linkage to chemical composition and property data fragments for one specific material. Finally, the extracted tuple entities containing article DOI, alloy named entity, chemical element, content, property specifier and property value are automatically compiled into a highly structured format for materials database.

- The files in input_xml/html/txt folder are used for code testing.
- The code in table_extractor folder is used for parsing tables in xml and html files.
- The code in text_extractor folder is used for extracting information in txt files.
- The code in pipeline folder directly realize the transformation from literature to structured database. 

**Usage**
----------------------
Use the code in your own project.

Please see the API documentation for specific details on how to use code for different situations. If you want to apply the code to other fields than superalloy, please modify the rule in configuration file(.\pipeline\dictionary.ini).

Note:The xlrd library version needs to be 1.2.0, run
```
pip install xlrd==1.2.0
```

**Citing**
----------------------
If you use this work (data or code), please cite the following work as appropriate:
```
Wang W, Jiang X, Tian S, et al. Automated pipeline for superalloy data by text mining[J]. npj Computational Materials, 2022, 8(1): 1-12.
```

**License**
----------------------
All source code is licensed under the MIT license.
