from typing import Dict, Union, Generator
import functools
import os
import time
import re
import json
from datetime import datetime

CLEANR = re.compile('<.*?>')

def cleanhtml(raw_html):
    cleantext = re.sub(CLEANR, '', raw_html)
    return cleantext


def timer(func):
    @functools.wraps(func)
    def wrapper_timer(*args, **kwargs):
        start_t = time.perf_counter()
        f_value = func(*args, **kwargs)
        elapsed_t = time.perf_counter() - start_t
        mins = elapsed_t // 60
        print(
            f"'{func.__name__}' elapsed time: {mins} minutes, {elapsed_t - mins * 60:0.2f} seconds"
        )
        return f_value

    return wrapper_timer


def load_wapo(wapo_jl_path: Union[str, os.PathLike]) -> Generator[Dict, None, None]:
    """
    It's same with the load_wapo in HW3
    """
    with open(wapo_jl_path, 'r') as f:
        for i, line in enumerate(f):
            line = json.loads(line)
            doc = {"id": i,
                   "title": line["title"],
                   "author": line["author"],
                   "published_date": datetime.fromtimestamp(line["published_date"] / 1000.0)}

            # concatenate content_str
            content_str = " ".join([content["content"] for content in line["contents"] if
                                    content and content["type"] == 'sanitized_html' and content["content"]])
            # remove html tags
            doc['content_str'] = cleanhtml(content_str)

            yield doc


if __name__ == "__main__":
    pass
