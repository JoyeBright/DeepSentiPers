import nltk
from SentiWordNet import InputTxt
import yaml



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


class DictionaryTagger(object):
    def __init__(self, dictionaries_path):
        # Open the path of Dictionary folder
        files = [open(path, 'r') for path in dictionaries_path]
        # load each of one dictionary into the solo dictionaries
        dictionaries = [yaml.load(dictionary_file) for dictionary_file in files]
        # Close all of the open files
        # print("#debug of Dictionaries: ", dictionaries)
        map(lambda z: z.close(), files)
        self.dictionary = {}
        self.max_key_size = 0
        for current_dict in dictionaries:
            for key in current_dict:
                if key in self.dictionary:
                    self.dictionary[key].extend(current_dict[key])
                else:
                    self.dictionary[key] = current_dict[key]
                    self.max_key_size = max(self.max_key_size, len(key))
        # print("#debug of discovered dictionary:", self.dictionary)
        # print("#debug of max length of keys: ", len(key))

    def tag(self, pos):
        return [self.tag_sentence(sentence) for sentence in pos]

    def tag_sentence(self, sentence, tag_lemma=False):
        tag_sentence = []
        # N returns num of items in the list
        N = len(sentence)
        if self.max_key_size == 0:
            self.max_key_size = N
        i = 0
        while i < N:
            j = min(i + self.max_key_size, N)
            tagged = False
            while j > i:
                expression_form = ' '.join([word[0] for word in sentence[i:j]]).lower()
                expression_lemma = ' '.join([word[1] for word in sentence[i:j]]).lower()
                if tag_lemma:
                    literal = expression_lemma
                else:
                    literal = expression_form
                if literal in self.dictionary:
                    is_single_token = j - i == 1
                    original_position = i
                    i = j
                    taggings = [tag for tag in self.dictionary[literal]]
                    tagged_expression = (expression_form, expression_lemma, taggings)
                    if is_single_token:
                        original_token_tagging = sentence[original_position][2]
                        tagged_expression[2].extend(original_token_tagging)
                    tag_sentence.append(tagged_expression)
                    tagged = True
                else:
                    j = j - 1
            if not tagged:
                tag_sentence.append(sentence[i])
                i += 1
        return tag_sentence


class SaScore(object):
    def __init__(self):
        pass

    def value_of(self, sentiment):
        if sentiment == 'positive':
            return 1
        if sentiment == 'negative':
            return -1
        return 0

    def sa_score(self, dictionary_tagged_sentence):
        return sum([self.value_of(tag) for sentence in dictionary_tagged_sentence for token in sentence for tag in token[2]])


pre = PreProcess()
SplittedSentences = pre.split(InputTxt.text)
POS = pre.pos_tagger(SplittedSentences)
Adjust = pre.adjust(POS)
DicTagger = DictionaryTagger(['Dictionary/positive.yml', 'Dictionary/negative.yml'])
dict_tagged_sentences = DicTagger.tag(Adjust)
SentimentScore = SaScore()
Score = SentimentScore.sa_score(dict_tagged_sentences)

print("Splitting the Sentences ......")
print(SplittedSentences)
print("Part of Speech ......")
print(POS)
print("Adjust with the Text Structure ......")
print(Adjust)
print("Tagging the tokens with Dictionaries ......")
print(dict_tagged_sentences)
print("..... Sentiment Analysing .....")
print("AVG:", Score)

