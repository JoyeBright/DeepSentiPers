from hazm import *
from stopwords_guilannlp import stopwords_output

# Get stop words
stop_words = stopwords_output("Persian", "nar")
stop_list = ['سلام', '!', 'باشه', 'می\u200cکند', 'بگم', 'میکنه', 'می\u200cباشد', 'شده_است', 'آن', 'این']
normalizer = Normalizer()
for s in stop_words:
    stop_list.append(normalizer.normalize(s[0]))
stop_set = set(stop_list)


def get_stop_set():
    return stop_set
