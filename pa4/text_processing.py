from typing import Any, List
import math

from nltk.tokenize import word_tokenize  # type: ignore
from nltk.stem.porter import PorterStemmer  # type: ignore
from nltk.corpus import stopwords  # type: ignore


class TextProcessing:
    def __init__(self, stemmer, stop_words, *args):
        """
        class TextProcessing is used to tokenize and normalize tokens that will be further used to build inverted index.
        :param stemmer:
        :param stop_words:
        :param args:
        """
        self.stemmer = stemmer
        self.stopwords = stop_words

    @classmethod
    def from_nltk(
        cls,
        stemmer: Any = PorterStemmer().stem,
        stop_words: List[str] = stopwords.words("english"),
    ) -> "TextProcessing":
        """
        initialize from nltk
        :param stemmer:
        :param stop_words:
        :return:
        """
        return cls(stemmer, set(stop_words))

    def normalize(self, token: str) -> str:
        """
        A. convert uppercase into lowercase
        B. remove stopwords
        C. clean punctuations except:
            1) "-"
            2) ":" when it represents time (previous token and next token are numeric
            3) "." when it represents decimal numbers
        :param token:
        :return:
        """
        # TODO:
        token = token.lower()
        if token in self.stopwords:
            return ""

        # clean up punctuations
        chars = []
        for i in range(len(token)):
            if token[i].isalpha() or token[i].isnumeric() or token[i] == "-" \
                    or (token[i] in [":", "."] and 0 <= i < len(token) - 1 and token[i - 1].isnumeric() and token[
                i + 1].isnumeric()):
                chars.append(token[i].lower())
        token = "".join(chars)

        print(f"token:{token}")
        print(f"token:{self.stemmer(token)}")
        return self.stemmer(token)

    def get_normalized_tokens(self, title: str, content: str) -> List[str]:
        """
        pass in the title and content_str of each document, and return a list of normalized tokens (exclude the empty string)
        you may want to apply word_tokenize first to get un-normalized tokens first.
        Note that you don't want to remove duplicate tokens as what you did in HW3, because it will later be used to compute term frequency
        :param title:
        :param content:
        :return:
        """
        # TODO:
        return [tkn for token in word_tokenize(title + " " + content) if (tkn := self.normalize(token)) != ""]

    @staticmethod
    def idf(N: int, df: int) -> float:
        """
        compute the logarithmic (base 2) idf score
        :param N: document count N
        :param df: document frequency
        :return:
        """
        # TODO:
        # raise NotImplementedError
        assert df != 0
        return math.log(N/df, 2)

    @staticmethod
    def tf(freq: int) -> float:
        """
        compute the logarithmic tf (base 2) score
        :param freq: raw term frequency
        :return:
        """
        # TODO:
        # raise NotImplementedError
        assert freq != 0
        return 1 + math.log(freq, 2)


if __name__ == "__main__":
    pass
    # content = "car insurance auto insurance"
    # text_processor = TextProcessing.from_nltk()
    # tokens = text_processor.get_normalized_tokens("", content)
    # print(tokens)