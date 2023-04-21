# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division, print_function, unicode_literals

from sumy.parsers.html import HtmlParser
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer as Summarizer
from sumy.nlp.stemmers import Stemmer
from sumy.utils import get_stop_words
    
def summarize(url, lang="en"):
    
    if lang == "en":
        LANGUAGE = "english"
    elif lang == "de":
        LANGUAGE = "german"
    else:
        raise ValueError("Language not supported")

    SENTENCES_COUNT = 10

    url = url
    parser = HtmlParser.from_url(url, Tokenizer(LANGUAGE))
    # or for plain text files
    # parser = PlaintextParser.from_file("document.txt", Tokenizer(LANGUAGE))
    # parser = PlaintextParser.from_string("Check this out.", Tokenizer(LANGUAGE))
    stemmer = Stemmer(LANGUAGE)

    summarizer = Summarizer(stemmer)
    summarizer.stop_words = get_stop_words(LANGUAGE)
    
    summary = summarizer(parser.document, SENTENCES_COUNT)
    text = ""
    for sentence in summary:
        text += str(sentence)

    return text

 
print(summarize(url="https://de.wikipedia.org/wiki/Mainzer_Republik", lang="de"))