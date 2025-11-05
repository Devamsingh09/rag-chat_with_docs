from langchain_community.document_loaders import WebBaseLoader, TextLoader, PyPDFLoader

def load_documents(files, urls=None):
    docs=[]
    for file in files:
        if file.endswith('.pdf'):
            docs.extend(PyPDFLoader(file).load())
        else:
            docs.extend(TextLoader(file, encoding='utf-8').load())
    if urls:
        for url in urls:
            docs.extend(WebBaseLoader(url).load())
    return docs
    