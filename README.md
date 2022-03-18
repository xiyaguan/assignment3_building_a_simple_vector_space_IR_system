# assignment4_building_a_simple_vector_space_IR_system

Implement a simple vector space information retreval system supporting "OR" queries over terms and apply it to the TREC corpus. Users of your application should be able to: (1) type in a text query and system will show all the relevant documents; (2) click the article title to view the whole document information (title, full content, etc.).

## Basic Information
- Title: Building a vector space information retrieval system
- Author: Xiya Guan
- Date: March 17th, 2022
- Description: implement a vector space information retrieval system that support conjunctive queries over terms.

## Dependency
- Flask==2.0.2
- Jinja2==3.0.3
- pymongo
- nltk==3.5

## Directory Structure
This is our current application structure looks:
```
pa4/
├── __init__.py
├── hw4.py
├── inverted_index.py
├── mongo_db.py
├── pa3_data
│   ├── test_corpus.jl
│   └── wapo_pa3.jl
├── requirements.txt
├── templates
│   ├── doc.html
│   ├── home.html
│   └── results.html
├── text_processing.py
└── utils.py


```
## What's new in implementation?
In the file utils.py, besides two provided functions (timer and load_wapo), a new function, cleanhtml, is implemented to help to remove HTML tags from text. \
The file customized_text_processing.py contains customized approaches to normalize the text to build inverted index:
- created a more thorough stopword list.
- cleaned up punctuations but took care of two special cases 1) the colon (:) between digits representing time 2) the period (.) between digits representing decimal numbers. In the two scenarios, the punctuations will be kept.
- Rather than the given text processor, all the numbers are ignored, in the customized approch, the numbers are kelp. Furthermore, the numbers present in word form in an input passage are converted to the traditional numeric (digits) form. For example, "a distance of one hundred and ten meters" will be converted into "a distance of 110 meters".


The logic in this web app is:
- we will first enter query text in the search box in the browser
- and then we will navigate to the web page shows the matched documents
- each page contains 2 results, you can use the next botton to turn to next page
- in the result page, the retreved document is displayed as a short snippet and a title with a link to its full content.


## Run Instructions
First, in the terminal, first run 
```bash
python hw3.py --build
```
to create the inverted index
Then run
```bash
python hw3.py --run
```
open up a new browser tab and head to the following URL:
http://127.0.0.1:5000/
You will see the search page where you can type a query and search!\


### What is the input and output produced?
In our system, a text query is treated as an input; The output are the matched documents.
### How to use the user interface?
Simply enter your text query in the search box.
### The legal input?
Since our corpus is in English, the legal input should be English terms. Note: this is a very simple web app, to find the matched documents, "query_inverted_index" function is implemented to support conjucntive queries over terms and outputs the doc ids, unknown words and ignored words.
### Boundry conditions?
- empty search: No matched documents.
- multiple empty spaces: No matched documents.
- terms in other languages: No matched documents.
- numerical terms or punctuations: Results depends on the titles and content of docs
- more then two spaces between two terms: Converted into only one space and then do the matching between the query and the document's title.

## Testing on "test_corpus"
1. input "state news"
![Screen Shot 2022-03-17 at 8 57 33 PM](https://user-images.githubusercontent.com/79282489/158917451-263c2697-e691-4e89-87d8-dc0c4b6d722c.png)

2. input "news"
![Screen Shot 2022-03-17 at 8 58 26 PM](https://user-images.githubusercontent.com/79282489/158917515-b18a6ffa-ff54-4409-9b1b-84909ef2cb51.png)

