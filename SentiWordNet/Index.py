import nltk
from nltk.corpus import sentiwordnet as swn
from SentiWordNet import InputTxt

sentences = nltk.sent_tokenize(InputTxt.text1)
print(sentences)
sentences_tokens = [nltk.word_tokenize(s) for s in sentences]
print(sentences_tokens)
tagged_list = []
for i in sentences_tokens:
    tagged_list.append(nltk.pos_tag(i))
print(tagged_list)
wordNetLemmatizer = nltk.WordNetLemmatizer()

score_list = []
for i, j in enumerate(tagged_list):
    score_list.append([])
    for m, n in enumerate(j):
        new_tag = ''
        lemmatized = wordNetLemmatizer.lemmatize(n[0])
        if n[1].startswith('NN'):
            new_tag = 'n'
        elif n[1].startswith('JJ'):
            new_tag = 'a'
        elif n[1].startswith('V'):
            new_tag = 'v'
        elif n[1].startswith('R'):
            new_tag = 'r'
        else:
            new_tag = ''
        if new_tag != '':
            synsets = list(swn.senti_synsets(lemmatized, new_tag))
            score = 0
            if len(synsets) > 0:
                for s in synsets:
                    score += s.pos_score() - s.neg_score()
                score_list[i].append(score/len(synsets))

print(score_list)
sentences_sentiment = []

for s in score_list:
    sentences_sentiment.append(sum([w for w in s])/len(s))
print("Final Sentiment Analysis for each sentences in Input text: .........")
print(sentences_sentiment)






