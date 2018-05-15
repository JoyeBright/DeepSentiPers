import nltk
import InputTxt


class PreProcess(object):
    def __init__(self):
        self.sentence_splitter = nltk.data.load('tokenizers/punkt/english.pickle')
        self.tokenizer = nltk.tokenize.TreebankWordTokenizer()

    def split(self, txt):
        sentences = self.sentence_splitter.tokenize(txt)
        # The following line says: tokenize each of the sentences
        # Deeply it means iterate each sentence and make its words into tokens
        # It calls List Comprehension
        tokenized_sentences = [self.tokenizer.tokenize(s) for s in sentences]
        return tokenized_sentences


pre = PreProcess()
print(pre.split(InputTxt.text))