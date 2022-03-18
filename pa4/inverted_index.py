from typing import List, Tuple, Dict, Iterable
from utils import timer
from collections import defaultdict, Counter
import heapq

from nltk.tokenize import word_tokenize

from text_processing import TextProcessing
from mongo_db import insert_vs_index, insert_doc_len_index, query_vs_index, query_doc_len_index

text_processor = TextProcessing.from_nltk()


def get_doc_vec_norm(term_tfs: List[float]) -> float:
    """
    helper function, should be called in build_inverted_index
    compute the length of a document vector
    :param term_tfs: a list of term weights (log tf) for one document
    :return:
    """
    return sum(tf_weight ** 2 for tf_weight in term_tfs) ** (1 / 2)


@timer
def build_inverted_index(
        wapo_docs: Iterable,
) -> None:
    """
    load wapo_pa4.jl to build two indices:
        - "vs_index": for each normalized term as a key, the value should be a list of tuples; each tuple stores the doc id this term appear in and the term weight (log tf)
        [{"term": "earlier", "term_tf": [[0, 1], [4, 1], ...]}, ...]
        - "doc_len_index": for each doc id as a key, the value should be the "length" of that document vector
        [{"doc_id": 0, "length": 39.53}, ...]
    insert the indices by using mongo_db.insert_vs_index and mongo_db.insert_doc_len_index method
    """

    vs_index = defaultdict(list)
    doc_tf_raw = defaultdict(lambda: defaultdict(int))  # doc_id: {"word1": cnt1, "word2": cnt2 .. }
    doc_len_index = defaultdict(float)

    num_doc = 0
    for doc in wapo_docs:
        num_doc += 1
        doc_id = doc["id"]
        title = doc["title"] if "title" in doc and doc['title'] != None else ""
        content_str = doc["content_str"] if "content_str" in doc and doc['content_str'] != None else ""
        tokens = text_processor.get_normalized_tokens(title, content_str)
        term_freq = Counter(tokens)
        for term, freq in term_freq.items():
            # update vs_index
            vs_index[term].append((doc_id, text_processor.tf(freq)))

            # update doc_tf_raw
            doc_tf_raw[doc_id][term] += freq

    # convert a list of tf into length normalization score
    for doc_id in doc_tf_raw:
        doc_len_index[doc_id] = get_doc_vec_norm(
            [text_processor.tf(doc_tf_raw[doc_id][term]) for term in doc_tf_raw[doc_id]])

    # insert vs_index into moingo_db
    insert_vs_index([{"term": term, "term_tf": vs_index[term]} for term in vs_index])

    # insert insert_doc_len_index into moingo_db
    insert_doc_len_index([{"doc_id": doc_id, "length": doc_len_index[doc_id]} for doc_id in doc_len_index])


# def parse_query(query: str) -> Tuple[List[str], List[str], List[str]]:
#     """
#     helper function, should be called in query_inverted_index
#     given each query, return a list of normalized terms, a list of stop words and a list of unknown words separately
#     """
#     # TODO:
#     raise NotImplementedError


def top_k_docs(doc_scores: Dict[int, float], k: int) -> List[Tuple[float, int]]:
    """
    helper function, should be called in query_inverted_index method
    given the doc_scores, return top k doc ids and corresponding scores using a heap
    :param doc_scores: a dictionary where doc id is the key and cosine similarity score is the value
    :param k:
    :return: a list of tuples, each tuple contains (score, doc_id)
    """
    min_heap = []
    for doc in doc_scores:
        if k > 0:
            heapq.heappush(min_heap, (doc_scores[doc], doc))
            k -= 1
        else:
            heapq.heappushpop(min_heap, (doc_scores[doc], doc))
    return min_heap


def query_inverted_index(
        query: str, k: int, N:int
) -> Tuple[List[Tuple[float, int]], List[str], List[str]]:
    """
    disjunctive query over the vs_index with the help of mongo_db.query_vs_index, mongo_db.query_doc_len_index methods
    return a list of matched documents (output from the function top_k_docs), a list of stop words and a list of unknown words separately
    """
    stop_words = []
    unknown_words = []

    scores = defaultdict(float)
    query_tokens = word_tokenize(query)

    query = Counter()
    for token in query_tokens:
        if token in text_processor.stopwords:  # check stop words
            stop_words.append(token)
        normalized_token = text_processor.normalize(token)
        if normalized_token:
            term_tf = query_vs_index(normalized_token)
            if not term_tf:  # check unknown words
                unknown_words.append(token)
            else:
                query[normalized_token] += 1

    for term in query:
        tf_raw = query[term]
        tf_weight = text_processor.tf(tf_raw)
        term_tf = query_vs_index(term)
        df = len(term_tf["term_tf"])
        idf = text_processor.idf(N, df)
        wtq = tf_weight * idf

        for d, wtd in term_tf["term_tf"]:
            scores[d] += wtq * wtd

    for d in scores:
        scores[d] /= query_doc_len_index(d)['length']

    matched_documents = top_k_docs(scores, k)

    return matched_documents, list(query.keys()), stop_words, unknown_words


if __name__ == "__main__":
    pass
