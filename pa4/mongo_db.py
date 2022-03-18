from typing import Dict, List, Iterable

import pymongo

client = pymongo.MongoClient("localhost", 27017)
db = client["ir_2022_wapo"]


def insert_docs(docs: Iterable) -> None:
    """
    - create a collection called "wapo_docs"
    - add a unique ascending index on the key "id"
    - insert documents into the "wapo_docs" collection
    :param docs: WAPO docs iterator (utils.load_wapo(...))
    :return:
    """
    wapo_docs = db['wapo_docs']
    wapo_docs.create_index("id")
    for doc in docs:
        wapo_docs.insert_one(doc)


def insert_vs_index(index_list: List[Dict]) -> None:
    """
    - create a collection called "vs_index"
    - add a unique ascending index on the key "term"
    - insert posting lists (index_list) into the "inverted_index" collection
    :param index_list: posting lists in the format of [{"term": "earlier", "term_tf": [[0, 1], [4, 1], ...]}, ...]
    :return:
    """
    vs_index = db["vs_index"]
    vs_index.create_index("term")
    for index in index_list:
        vs_index.insert_one(index)



def insert_doc_len_index(index_list: List[Dict]) -> None:
    """
    - create a collection called "doc_len_index"
    - add a unique ascending index on the key "doc_id"
    - insert list of document vector length (index_list) into the "doc_len_index" collection
    :param index_list: document vector length list in the format of [{"doc_id": 0, "length": 39.53}, ...]
    :return:
    """
    doc_len_index = db["doc_len_index"]
    doc_len_index.create_index("doc_id")
    for index in index_list:
        doc_len_index.insert_one(index)


def query_doc(doc_id: int) -> Dict:
    """
    query the document from "wapo_docs" collection based on the doc_id
    :param doc_id:
    :return:
    """
    return db['wapo_docs'].find_one({"id": doc_id})


def query_vs_index(term: str) -> Dict:
    """
    query the vs_index collection by term
    :param term:
    :return:
    """
    # print(db['vs_index'].find_one({"term": term}))
    return db['vs_index'].find_one({"term": term})


def query_doc_len_index(doc_id: int) -> Dict:
    """
    query the doc_len_index by doc_id
    :param doc_id:
    :return:
    """
    return db['doc_len_index'].find_one({"doc_id": doc_id})


# def query_doc_cnt() -> int:
#     return db['doc_len_index'].count()


if __name__ == "__main__":
    pass
