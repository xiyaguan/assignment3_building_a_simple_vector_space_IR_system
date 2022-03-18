from pathlib import Path
import argparse
import re

from flask import Flask, render_template, request, session
from flask_session import Session
from utils import load_wapo
from inverted_index import build_inverted_index, query_inverted_index
from mongo_db import db, insert_docs, query_doc
from text_processing import TextProcessing

# stem
# query 结果
# contract不删掉，train vec


app = Flask(__name__)

N = 10
K = 3
NUM_DISPKAY = 2
TRUNCATE_LENGTH = 150
data_dir = Path(__file__).parent.joinpath("pa4_data")
wapo_path = data_dir.joinpath("test_corpus.jl")


app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


# home page
@app.route("/")
def home():
    return render_template("home.html")


# result page
@app.route("/results", methods=["POST"])
def results():
    """
    result page
    :return:
    """
    query_text = request.form["query"]  # Get the raw user query from home page
    query_text = re.sub(' +', ' ', query_text.strip())  # trimming the ending and starting empty epaces and turn multiple spaces into one
    session["query_text"] = query_text  # Get the raw user query from home page
    stopwords = []
    unknown = []
    validwords = []
    if query_text:
        score_docID, validwords, stopwords, unknown = query_inverted_index(query_text, K, N)


    session["score_docID"] = score_docID
    session["validwords"] = validwords

    # calculate the total number of pages that matched docs can be converted to
    div, mod = divmod(len(score_docID), NUM_DISPKAY)
    session["max_pages"] = div if mod == 0 else div + 1

    if div == 0:
        if mod == 0:
            curr_page = 0
        else:
            curr_page = 1
        end = True
    elif div == 1:
        if mod == 0:
            end = True
        else:
            end = False
        curr_page = 1
    else:
        end = False
        curr_page = 1

    if not score_docID:
        return render_template("results.html",
                               query=query_text,
                               curr_page=0,
                               unknown=unknown,
                               end=True,
                               max_pages=0,
                               num_hits=0,
                               truncate_length=TRUNCATE_LENGTH)

    return render_template("results.html",
                           query=query_text,
                           curr_page=curr_page,
                           output=[(round(score, 4), query_doc(id)) for score, id in score_docID[:NUM_DISPKAY]],
                           stopwords=stopwords,
                           unknown=unknown,
                           validwords=validwords,
                           end=end,
                           max_pages=session["max_pages"],
                           num_hits=len(score_docID),
                           truncate_length=TRUNCATE_LENGTH)


# "next page" to show more results
@app.route("/results/<int:page_id>", methods=["GET"])
def next_page(page_id):
    """
    "next page" to show more results
    :param page_id:
    :return:
    """
    end = False
    if page_id == session["max_pages"]:
        end = True
    return render_template("results.html",
                           query=session["query_text"],
                           curr_page=page_id,
                           output=[(round(score, 4), query_doc(id))for score, id in session["score_docID"][(page_id-1) * NUM_DISPKAY: min(len(session["score_docID"]), page_id*NUM_DISPKAY)]],
                           validwords=session["validwords"],
                           end=end,
                           max_pages=session["max_pages"],
                           num_hits=len(session["score_docID"]),
                           truncate_length=TRUNCATE_LENGTH)


# document page
@app.route("/doc_data/<int:doc_id>")
def doc_data(doc_id):
    return render_template("doc.html",
                           title=query_doc(doc_id)['title'],
                           author=query_doc(doc_id)['author'],
                           date=query_doc(doc_id)['published_date'],
                           content=query_doc(doc_id)['content_str'])


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Boolean IR system")
    parser.add_argument("--build", action="store_true")
    parser.add_argument("--run", action="store_true")
    args = parser.parse_args()

    if args.build:
        if "inverted_index" in db.list_collection_names():
            db.inverted_index.drop()
        if "wapo_docs" in db.list_collection_names():
            db.wapo_docs.drop()
        if "vs_index" in db.list_collection_names():
            db.vs_index.drop()
        if "doc_len_index" in db.list_collection_names():
            db.doc_len_index.drop()
        insert_docs(load_wapo(wapo_path))
        build_inverted_index(load_wapo(wapo_path))

    if args.run:
        app.run(debug=True, port=5000)
