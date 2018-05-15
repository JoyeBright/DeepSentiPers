import nltk
import InputTxt


class PreProcess(object):
    def __init__(self):
        self.sentence_splitter = nltk.data.load('tokenizers/punkt/english.pickle')
        self.tokenizer = nltk.tokenize.TreebankWordTokenizer()

    def split(self, txt):
        # Spliting and finding sentences
        sentences = self.sentence_splitter.tokenize(txt)
        # The following line says: tokenize each of the sentences
        # Deeply it means iterate each sentence and make its words into tokens
        # It calls List Comprehension
        tokenized_sentences = [self.tokenizer.tokenize(s) for s in sentences]
        return tokenized_sentences

    def pos_tagger(self, sentences):
        # POS tagger will attach the associated POS to the tokens
        pos = [nltk.pos_tag(s) for s in sentences]
        return pos

    def adjust(self, pos):
        # Adjust with the defined text structure
        adjust = [[(word, word, [postag]) for (word, postag) in i] for i in pos]
        return adjust


pre = PreProcess()
tokenized = pre.split(InputTxt.text)
pos = pre.pos_tagger(tokenized)
print(pre.adjust(pos))
